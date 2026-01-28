// sidebar toggle
const body = document.body;
const sidebar = document.querySelector("nav");
const sidebarToggle = document.querySelector(".sidebar-toggle");

// dark mode toggle
const modeToggle = document.querySelector(".mode-toggle");
const modeSwitch = document.querySelector(".mode-toggle .switch");

// restore theme from localStorage
if (localStorage.getItem("neet_theme") === "dark") {
  body.classList.add("dark");
}

// restore sidebar state
if (localStorage.getItem("neet_sidebar") === "close") {
  sidebar.classList.add("close");
}

// sidebar open/close
if (sidebarToggle) {
  sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    localStorage.setItem(
      "neet_sidebar",
      sidebar.classList.contains("close") ? "close" : "open"
    );
  });
}

// dark / light mode
if (modeToggle) {
  modeToggle.addEventListener("click", () => {
    body.classList.toggle("dark");
    localStorage.setItem(
      "neet_theme",
      body.classList.contains("dark") ? "dark" : "light"
    );
  });
}

// ===== CHART.JS CONFIG =====

// helper for gradient
function createGradient(ctx, color1, color2) {
  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, color1);
  gradient.addColorStop(1, color2);
  return gradient;
}

// Rank chart
const rankCanvas = document.getElementById("rankChart");
if (rankCanvas) {
  const rCtx = rankCanvas.getContext("2d");
  new Chart(rCtx, {
    type: "line",
    data: {
      labels: ["2022", "2023", "2024", "2025", "2026"],
      datasets: [
        {
          label: "Average Predicted Rank",
          data: [8200, 7600, 7100, 6650, 6300],
          borderColor: "#10b981",
          backgroundColor: createGradient(rCtx, "rgba(16,185,129,0.4)", "rgba(16,185,129,0.0)"),
          fill: true,
          borderWidth: 3,
          tension: 0.3,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true },
        tooltip: { enabled: true }
      },
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          beginAtZero: false,
          grid: { color: "#e5e7eb" }
        }
      }
    }
  });
}

// Score chart
const scoreCanvas = document.getElementById("scoreChart");
if (scoreCanvas) {
  const sCtx = scoreCanvas.getContext("2d");
  new Chart(sCtx, {
    type: "bar",
    data: {
      labels: ["<500", "500-550", "550-600", "600-650", "650+"],
      datasets: [
        {
          label: "Students",
          data: [320, 540, 730, 610, 290],
          backgroundColor: [
            "#bfdbfe",
            "#93c5fd",
            "#60a5fa",
            "#3b82f6",
            "#2563eb"
          ],
          borderRadius: 10
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true }
      },
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          beginAtZero: true,
          grid: { color: "#e5e7eb" }
        }
      }
    }
  });
}
