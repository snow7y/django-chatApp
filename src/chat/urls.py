from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create_session/', views.create_session, name='create_session'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
]