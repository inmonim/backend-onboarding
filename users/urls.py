from django.urls import path, include

from users.views import user_view_api, user_detail_view_api

app_name = "users"

urlpatterns = [
    path("", user_view_api),
    path("<int:user_id>", user_detail_view_api),
]