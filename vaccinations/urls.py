# vaccinations/urls.py
from django.urls import path
from .views import (
    HomeView, AddRecordView, UpdateLookupView,
    VaccinationCardDueView, VaccinationCardAllView,
    ChildCardAPI,
    PartnerCreateUploadView,
    DoctorRegisterSelfView, DoctorRegisterPartnerView,
    DoctorPortalHomeView, DoctorPortalAddRecordView, DoctorPortalUpdateLookupView,
    DoctorPortalCardDueView, DoctorPortalCardAllView, DoctorPortalEditProfileView,
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

    # Admin publishing
    path("partners/new/", PartnerCreateUploadView.as_view(), name="partner-create"),
    # Doctor registration
    path("doctor/register/", DoctorRegisterSelfView.as_view(), name="doctor-register-self"),
    path("doctor/register/<str:token>/", DoctorRegisterPartnerView.as_view(), name="doctor-register-partner"),
    # Doctor portal (token)
    path("d/<str:token>/", DoctorPortalHomeView.as_view(), name="doc-home"),
    path("d/<str:token>/add/", DoctorPortalAddRecordView.as_view(), name="doc-add"),
    path("d/<str:token>/update/", DoctorPortalUpdateLookupView.as_view(), name="doc-update"),
    path("d/<str:token>/card/<int:child_id>/", DoctorPortalCardDueView.as_view(), name="doc-card"),
    path("d/<str:token>/card-all/<int:child_id>/", DoctorPortalCardAllView.as_view(), name="doc-card-all"),
    path("d/<str:token>/profile/", DoctorPortalEditProfileView.as_view(), name="doc-profile"),
]
