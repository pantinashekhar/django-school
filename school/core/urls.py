from django.urls import path
from . import views
from .views import ReportsView, DashboardView, IndexView, UniversalDeleteView
# Namespacing is critical for large SaaS apps
app_name = "core"

urlpatterns = [
    # --- Landing & Dashboard ---
    # The public facing landing page (Marketing)
    path("", views.IndexView.as_view(), name="index"),
    
    # The main SaaS application dashboard (Protected)
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

    path("reports/", ReportsView.as_view(), name="reports"),

    # --- Utility / HTMX Routes ---
    # This is a specialized route for the "Adaptable" architecture.
    # It allows deleting ANY object via HTMX without writing a specific View for it.
    # Usage in Template: {% url 'core:universal-delete' 'academics' 'student' student.id %}
    path(
        "action/delete/<str:app_label>/<str:model_name>/<int:pk>/", 
        views.UniversalDeleteView.as_view(), 
        name="universal-delete"
    ),
]