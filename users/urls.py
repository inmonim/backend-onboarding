from django.urls import path

from users.views import (user_view_set,
                         login_view,
                         logout_view,
                         refresh_view,
                         user_password_change_view_set)

app_name = "users"

urlpatterns = [
    path("", user_view_set, name="user_crud"),
    path("login/", login_view, name="user_login"),
    path("logout/", logout_view, name="user_logout"),
    path("change_password/", user_password_change_view_set, name="change_password"),
    path("refresh/", refresh_view, name="token_refresh"),
]