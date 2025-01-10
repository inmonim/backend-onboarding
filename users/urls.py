from django.urls import path

from users.views import (user_view_set,
                         login_view,
                         logout_view,
                         protect_view,
                         refresh_view,
                         user_password_change_view_set)

app_name = "users"

urlpatterns = [
    path("", user_view_set),
    path("login/", login_view),
    path("logout/", logout_view),
    path("change-password/", user_password_change_view_set),
    path("refresh/", refresh_view),
    path("protect/", protect_view)
]