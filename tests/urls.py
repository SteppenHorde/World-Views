from django.urls import path
from . import views


urlpatterns = [
    path('', views.tests, name='tests'),
    path('<int:test_id>', views.show_test, name='show_test'),
    path('<int:test_id>/quiz', views.quiz_test, name='quiz_test'),
    path('<int:test_id>/results', views.tests_results, name='tests_results'),
    ]
