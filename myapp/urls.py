from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'home/', views.home, name='home'),
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'order_response/', views.place_order, name='order_response'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'courses/<cour_id>/', views.course_detail, name='course_detail'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myaccount/', views.myaccount, name='my_account'),
    path(r'test_cookie/', views.test_cookie, name='test_cookie'),
    path(r'register/', views.register, name='register'),
    path(r'registerResponse/', views.registerResponse, name='registerResponse'),

    path(r'reset_pwd/', views.reset_pwd, name='reset_pwd'),
]
