SCOPES = 'https://www.googleapis.com/auth/pubsub https://mail.google.com/ https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'

# Google services urls.
GOOGLE_AUTH_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_REVOKE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/revoke'
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={}&redirect_uri={}&scope={}'

# Gmail services urls.
GMAIL_WATCH_REQUEST_URL = 'https://gmail.googleapis.com/gmail/v1/users/{}/watch'
GMAIL_STOP_REQUEST_URL = 'https://gmail.googleapis.com/gmail/v1/users/{}/stop'
