from django.urls import path

from .views import (
    GoogleOAuth2LoginAPIView,
    RevokeGoogleAccessTokenAPIView
)

urlpatterns = [
    path("googleLogin/", GoogleOAuth2LoginAPIView.as_view(), name="google-login"),
    path("revokeToken/", RevokeGoogleAccessTokenAPIView.as_view(), name="revoke-token"),
]
