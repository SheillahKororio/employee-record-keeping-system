from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(
        template_name="registration/login.html"
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("staff/register/", views.register_staff, name="register_staff"),
    path("", views.createEmp, name="createEmp"),
    path("show/", views.show, name="show"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("update/<int:id>/", views.update, name="update"),
    path("delete/<int:id>/", views.destroy, name="destroy"),
]