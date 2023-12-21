from django.urls import path

from .views import (
    GmailWatchAPIView,
    GoogleOAuth2LoginAPIView,
    RevokeGoogleAccessTokenAPIView
)

urlpatterns = [
    path("googleLogin/", GoogleOAuth2LoginAPIView.as_view(), name="google-login"),
    path("revokeToken/", RevokeGoogleAccessTokenAPIView.as_view(), name="revoke-token"),
    path("gmailWatch/", GmailWatchAPIView.as_view(), name="gmail-watch")
]
