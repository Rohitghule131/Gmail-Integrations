import requests
from os import getenv
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from Utilities.constant import SCOPES
from .models import GoogleRequestModel


class GoogleOAuth2LoginAPIView(RetrieveAPIView):
    """
    Class for create api view for login by gmail.
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        """
        GET function for request for google login.
        """
        client_id = getenv("GOOGLE_CLIENT_ID")
        client_secrete = getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = getenv("GOOGLE_REDIRECT_URI")

        if 'code' not in request.GET:
            auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                        '&client_id={}&redirect_uri={}&scope={}').format(client_id, redirect_uri, SCOPES)
            return redirect(auth_uri)
        else:
            auth_code = request.GET['code']
            data = {'code': auth_code,
                    'client_id': client_id,
                    'client_secret': client_secrete,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code',
                    }
            r = requests.post('https://oauth2.googleapis.com/token', data=data)
            request.session['credentials'] = r.text
            access_token_response = r.json()

            headers = {'Authorization': f'Bearer {access_token_response["access_token"]}'}
            personal_info_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
            personal_info_response = personal_info_response.json()

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
        GET function revoke the google access token.
        """
        email = request.GET.get("email", None)
        if email:
            google_info = GoogleRequestModel.objects.filter(email=email).last()
            if google_info:
                revoke_url = 'https://accounts.google.com/o/oauth2/revoke'

                # Construct the token revocation request
                revoke_params = {
                    'token': google_info.access_token
                }

                response = requests.post(revoke_url, params=revoke_params)

                if response.status_code == 200:
                    return Response({"message": "Access token revoked successfully."})
                else:
                    return Response({"message": "Failed to revoke the access token."})

        else:
            return Response({"message": "email address is required!"})

