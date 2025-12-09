# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("member/summary/", views.member_summary, name="member-summary"),
    path("member/add-points/", views.admin_add_points, name="member-add-points"),
]
