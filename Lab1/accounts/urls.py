from django.urls import path, include
from .views import profile_info, profile_info_by_id, signup, user_list

urlpatterns = [
    path('', user_list, name="user_list"),
    path('', include("django.contrib.auth.urls")),
    path('signup/', signup, name="signup"),
    path('profile/', profile_info),
    path('profile/<int:user_id>/', profile_info_by_id),
]