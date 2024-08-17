from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create_session/', views.create_session, name='create_session'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('view_html/<str:file_id>/', views.view_html, name='view_html'),
    path('view_html/iframe/<str:file_id>/', views.view_html_iframe, name='view_html_iframe'),
]