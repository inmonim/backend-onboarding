from django.urls import path, include

from users.views import user_detail_view_set, user_view_set, login_view_set

app_name = "users"

urlpatterns = [
    path("", user_view_set),
    path("<int:user_id>", user_detail_view_set),
    path("login", login_view_set),
]