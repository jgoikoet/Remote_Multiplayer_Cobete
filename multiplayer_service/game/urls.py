from django.urls import path
from . import views

urlpatterns = [
	path("matches/", views.match_list, name="match_list")
]