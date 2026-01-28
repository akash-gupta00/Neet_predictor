from django.shortcuts import render
from docx import Document
from .forms import WordUploadForm
from .models import NeetAllotment


def home(request):
    return render(request, "base.html", {"show_dashboard": True})

# -------- HEADER KEYWORDS (STRONG & SAFE) --------
HEADER_KEYS = {
    "rank": ["all india rank", "neet rank", "rank","All India Rank","neet overall rank"],
    "score": ["neet score", "score", "neet_score","neet score"],
    "category": ["category", "cat","Candidate Category"],
    "college": ["institute", "college","name of college","Name of College","Allotted Institute" ],
}


def normalize(text):
    return text.lower().replace("_", " ").strip()


def find_indexes(headers):
    col = {}
    for i, h in enumerate(headers):
        h = normalize(h)
        for field, keys in HEADER_KEYS.items():
            for k in keys:
                if k in h:
                    col[field] = i
    return col

import re

def extract_int(value):
    if not value:
        return None
    nums = re.findall(r"\d+", value)
    if not nums:
        return None
    return int(nums[0])

# ================= MAIN VIEW =================
def upload_word(request):
    if request.method == "POST":
        form = WordUploadForm(request.POST, request.FILES)

        if form.is_valid():
            doc = Document(request.FILES["file"])
            state = form.cleaned_data["state"]

            saved = 0
            skipped = 0

            for table in doc.tables:

                # ---- HEADER ROW ----
                headers = [c.text.strip() for c in table.rows[0].cells]
                col = find_indexes(headers)

                # SCORE & RANK mandatory
                if  "rank" not in col:
                    continue

                # ---- DATA ROWS ----
                for row in table.rows[1:]:
                    cells = [c.text.strip() for c in row.cells]

                    # SAFE READ
                    try:
                        score = int(cells[col["score"]])
                    except:
                        score = None

                    try:
                        rank = int(cells[col["rank"]])
                    except:
                        rank = None

                    category = None
                    if "category" in col:
                        raw_cat = cells[col["category"]].strip()

                        VALID_CATEGORIES = [
                            "SC", "ST", "OBC", "OC", "UR",
                            "BC-A", "BC-B", "BC-C", "BC-D", "BC-E",
                            "EWS", "GENERAL"
                        ]

                        if raw_cat.upper() in VALID_CATEGORIES:
                            category = raw_cat.upper()

                    college = None
                    if "college" in col:
                        raw_college = cells[col["college"]]

                        # multi-line college names ko ek line me laane ke liye
                        raw_college = raw_college.replace("\n", " ").replace("\r", " ")
                        raw_college = " ".join(raw_college.split())

                        if raw_college:
                            college = raw_college
                        else:
                            college = "UNKNOWN"
                    else:
                        college = "UNKNOWN"

                    # ---- VALIDATION ----
                    # rank mandatory hai
                    if rank is None:
                        skipped += 1
                        continue

                    # score optional hai (agar nahi mila to NULL rahe)
                    if score is not None and not (0 <= score <= 720):
                        skipped += 1
                        continue

                    # ---- SAVE ----
                    NeetAllotment.objects.create(
                        state=state,
                        score=score,
                        rank=rank,
                        category=category,
                        college=college,
                    )

                    saved += 1

            return render(request, "upload.html", {
                "form": WordUploadForm(),
                "success": f"{saved} rows saved",
                "skipped": f"{skipped} rows skipped"
            })

    return render(request, "upload.html", {"form": WordUploadForm()})




# ---------------- SCORE → RANK PREDICT ----------------



from django.shortcuts import render
from .models import NeetAllotment

from django.shortcuts import render
from .models import NeetAllotment


def predict(request):
    result = None
    message = None

    if request.method == "POST":
        score = request.POST.get("score")

        if score:
            score = int(score)

            # DB se valid data
            qs = NeetAllotment.objects.filter(
                score__isnull=False,
                rank__isnull=False
            )

            nearest = None
            min_diff = None

            # nearest score find
            for obj in qs:
                diff = abs(obj.score - score)
                if min_diff is None or diff < min_diff:
                    min_diff = diff
                    nearest = obj

            if nearest:
                base_rank = nearest.rank

                if score >= 600:
                    # ✅ sirf exact rank
                    result = f"{base_rank}"
                else:
                    # ✅ +1000 range
                    result = f"{base_rank} – {base_rank + 1000}"
            else:
                message = "Matching data database me nahi mila."

    return render(request, "predict.html", {
        "result": result,
        "message": message
    })


# ---------------- RANK + CATEGORY SE COLLEGE SEARCH ----------------


from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404
from .models import NeetAllotment





# ================= COLLEGE PREDICTOR =================
def college_predictor(request):
    colleges = None
    total_colleges = 0

    rank = request.GET.get("rank")
    category = request.GET.get("category")
    state = request.GET.get("state")  # compulsory

    # ❌ state missing → search hi nahi chale
    if not state:
        return render(request, "college_predictor.html", {
            "error": "Please select All India or a State"
        })

    if rank:
        try:
            rank = int(rank)

            # 🔹 base query: rank ke andar wale colleges
            queryset = NeetAllotment.objects.filter(
                rank__lte=rank
            )

            # 🔹 category optional
            if category:
                queryset = queryset.filter(category__iexact=category)

            # 🔹 STATE LOGIC (IMPORTANT)
            if state != "ALL":
                queryset = queryset.filter(state__iexact=state)
            # agar ALL hai → koi state filter nahi lagega

            queryset = queryset.order_by("rank")

            total_colleges = queryset.count()

            colleges = queryset.values(
                "college",
                "state",
                "rank",
                "category"
            )

        except ValueError:
            pass

    return render(request, "college_predictor.html", {
        "colleges": colleges,
        "total_colleges": total_colleges,
        "rank": rank,
        "category": category,
        "state": state
    })


# ================= ADMIN LOGIN =================
def admin_login(request):
    error = ""

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == settings.ADMIN_EMAIL and password == settings.ADMIN_PASSWORD:
            request.session["admin_logged_in"] = True
            return redirect("admin_dashboard")
        else:
            error = "Invalid Email or Password"

    return render(request, "login.html", {"error": error})


# ================= ADMIN DASHBOARD =================
def admin_dashboard(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    return render(request, "dashboard.html", {
        "show_dashboard": True
    })


# ================= LOGOUT =================
def admin_logout(request):
    request.session.flush()
    return redirect("admin_login")
