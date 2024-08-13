from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tracked", views.tracked, name="tracked"), 
    path("track_untrack", views.track_untrack, name="track_untrack"),
    path("check_tracked", views.check_tracked, name="check_tracked"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]