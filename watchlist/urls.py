from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add/", views.item_create, name="item_create"),
    path("watchlist/<int:pk>/", views.item_detail, name="item_detail"),
    path("watchlist/<int:pk>/edit/", views.item_update, name="item_update"),
    path("watchlist/<int:pk>/delete/", views.item_delete, name="item_delete"),
]
