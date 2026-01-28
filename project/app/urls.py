from django.urls import path
from .views import (
    home,
    upload_word,
    predict,
    college_predictor,
    admin_login,
    admin_dashboard,
    admin_logout
)

urlpatterns = [
    path("", home, name="home"),
    path("upload-word/", upload_word, name="upload_word"),
    path("predict/", predict, name="predict"),
    path("college-predictor/", college_predictor, name="college_predictor"),

    path("admin-login/", admin_login, name="admin_login"),
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
    path("logout/", admin_logout, name="admin_logout"),
]
