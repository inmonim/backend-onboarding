from django.urls import path

from users.views import user_detail_view_set, user_view_set, login_view, logout_view, protect_view, refresh_view

app_name = "users"

urlpatterns = [
    path("", user_view_set),
    path("<int:user_id>", user_detail_view_set),
    path("login", login_view),
    path("logout", logout_view),
    path("refresh", refresh_view),
    path("protect", protect_view)
]