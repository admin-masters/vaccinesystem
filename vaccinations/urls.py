# vaccinations/urls.py
from django.urls import path
from .views import (
    HomeView, AddRecordView, UpdateLookupView,
    VaccinationCardDueView, VaccinationCardAllView,
    ChildCardAPI,
)

app_name = "vaccinations"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add/", AddRecordView.as_view(), name="add"),
    path("update/", UpdateLookupView.as_view(), name="update"),

    # Existing due-only card (unchanged behavior)
    path("card/<int:child_id>/", VaccinationCardDueView.as_view(), name="card"),

    # NEW: Full schedule card (past + today + future)
    path("card-all/<int:child_id>/", VaccinationCardAllView.as_view(), name="card-all"),

    # Optional API
    path("api/children/<int:pk>/card/", ChildCardAPI.as_view(), name="card-api"),
]
