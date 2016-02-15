from json import loads

from flask import current_app, redirect, url_for, request
from rauth import OAuth2Service


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('frontend.oauth_callback',
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


def _google_decoder(data):
    result = data.decode('utf-8')
    if result:
        json = loads(result)
        return json
    return {}


class GoogleSignIn(OAuthSignIn):

    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            base_url='https://www.googleapis.com/oauth2/v1/',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='profile email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=_google_decoder,
            method='POST'
        )
        me = oauth_session.get('https://www.googleapis.com/plus/v1/people/me').json()
        return {
            'social_id': me['id'],
            'first_name': me['name']['givenName'],
            'last_name': me['name']['familyName'],
            'gender': me['gender'],
            'email': me['emails'][0]['value'],
            'avatar_url': me['image']['url']
        }
