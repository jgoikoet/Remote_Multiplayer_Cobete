from django.urls import path
from . import views

urlpatterns = [
	path("matches/", views.match_list, name="match_list"),
	path('matches/stats_view/<int:user_id>/', views.stats_view, name='stats_view'),
	path('matches/<int:pk>/', views.match_list_id, name='match_list_id'),
]