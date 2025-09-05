from django.urls import path
from .views import HomeView, AddRecordView, UpdateLookupView, VaccinationCardView, ChildCardAPI

app_name = "vaccinations"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add/", AddRecordView.as_view(), name="add"),
    path("update/", UpdateLookupView.as_view(), name="update"),
    path("card/<int:child_id>/", VaccinationCardView.as_view(), name="card"),

    # Optional JSON endpoint
    path("api/children/<int:pk>/card/", ChildCardAPI.as_view(), name="card-api"),
]
