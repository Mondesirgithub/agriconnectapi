from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from . import views


urlpatterns = [
    path('register/user/', views.registerUser, name='registerUser'),
    path('update/user/<int:id>', views.updateUser, name='updateUser'),
    path('user/<int:id>/photo/', views.get_user_photo, name='get_user_photo'),
    path('user/<int:id>/photo/update/', views.update_user_photo, name='update_user_photo'),
    path('users/login/', views.MyTokenObtainPairViews.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/change-password/', views.change_password, name='change-password'),
    path('users/envoyer_mail/', views.envoyer_mail, name='envoyer_mail'),
]