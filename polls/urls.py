from django.urls import path
from . import views


urlpatterns = [
    path('', views.polls, name='polls'),
    path('<int:poll_id>/vote/', views.polls_vote, name='polls_vote'),
    ]
