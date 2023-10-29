from django.urls import path
from . import views

urlpatterns = [
    # Name - optional arguments to let us refer to this route elsewhere in the app.
    path("", views.home, name="catalogue_home")
]
