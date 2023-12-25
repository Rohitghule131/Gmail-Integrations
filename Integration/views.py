import base64
import requests
from os import getenv
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)

from Utilities.constant import (
    SCOPES,
    GOOGLE_AUTH_URL,
    GOOGLE_USER_INFO_URL,
    GOOGLE_AUTH_TOKEN_URL,
    GMAIL_STOP_REQUEST_URL,
    GOOGLE_REVOKE_TOKEN_URL,
    GMAIL_WATCH_REQUEST_URL,
)
from .models import GoogleRequestModel
from .serializers import GmailWatchSerializer


class GoogleOAuth2LoginAPIView(RetrieveAPIView):
    """
    Class for create api view for login by gmail.
    """
    permission_classes = ()
    authentication_classes = ()
    throttle_classes = ()

    def get(self, request, *args, **kwargs):
        """
        GET function for request for google login.
        """
        client_id = getenv("GOOGLE_CLIENT_ID")
        client_secrete = getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = getenv("GOOGLE_REDIRECT_URI")

        if 'code' not in request.GET:
            auth_uri = GOOGLE_AUTH_URL.format(client_id, redirect_uri, SCOPES)
            return redirect(auth_uri)
        else:
            auth_code = request.GET['code']
            data = {
                'code': auth_code,
                'client_id': client_id,
                'client_secret': client_secrete,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            }
            response = requests.post(GOOGLE_AUTH_TOKEN_URL, data=data)
            request.session['credentials'] = response.text
            access_token_response = response.json()

            headers = {'Authorization': f'Bearer {access_token_response["access_token"]}'}
            personal_info_response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
            personal_info_response = personal_info_response.json()

            watch_request_url = GMAIL_WATCH_REQUEST_URL.format(personal_info_response["email"])

            watch_request_data = {
                'labelIds': ['INBOX'],
                'topicName': getenv('PUB_SUB_TOPIC'),
                'labelFilterBehavior': 'INCLUDE'
            }
            requests.post(watch_request_url, headers=headers, data=watch_request_data)

            GoogleRequestModel.objects.create(
                email=personal_info_response["email"],
                access_token=access_token_response["access_token"],
                profile_picture=personal_info_response["picture"],
            )

            return Response({"message": "Successfully"})


class RevokeGoogleAccessTokenAPIView(RetrieveAPIView):
    """
    Class for creation a revoke google access token api.
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        """
        GET function revoke the Google access token.
        """
        email = request.GET.get("email", None)
        if email:
            google_info = GoogleRequestModel.objects.filter(email=email).last()
            if google_info:

                headers = {
                    'Authorization': f'Bearer {google_info.access_token}'
                }

                stop_request_response = requests.post(GMAIL_STOP_REQUEST_URL.format(email), headers=headers)

                revoke_url = GOOGLE_REVOKE_TOKEN_URL

                # Construct the token revocation request
                revoke_params = {
                    'token': google_info.access_token
                }

                response = requests.post(revoke_url, params=revoke_params)

                if response.status_code == 200 and stop_request_response.status_code == 204:
                    google_info.delete()
                    return Response({"message": "Access token revoked and watch request stopped successfully."})
                else:
                    return Response({"message": "Failed to revoke the access token."})

        else:
            return Response({"message": "email address is required!"})


class GmailWatchAPIView(CreateAPIView):
    """
    Class for creation a gmail watch api.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = GmailWatchSerializer
    throttle_classes = ()

    def post(self, request, *args, **kwargs):
        """
        POST method used for gmail watch.
        """
        data = request.data.get("message")
        encoded_data = data.get("data")

        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        print("DECODED <><><><>", decoded_data)

        return Response({"SUCCESS": "SUCCESS"})
