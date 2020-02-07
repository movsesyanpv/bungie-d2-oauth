from flask import Flask, request, session, redirect, url_for
import requests
import json
import time


class BungieOAuth:
    """Class that is used to get auth tokens from Bungie

    Attributes
    -----------

    api_data: :class:`dict`
        Bungie API data. This is set automatically on initialization.
        Contains two keys: 'id' and 'secret'. These are set correspondingly by ``id_number`` and ``secret``.
    redirect_url: :class:`str`
        Redirect url used to get Bungie's auth response.
    token: :class:`dict`
        Bungie authorization token. Contains two keys: 'refresh' and 'expires'.
    """

    api_data = ''
    redirect_url = ''
    token = {}

    def __init__(self, id_number, secret, redirect_url='/redirect'):
        self.api_data = {
            'id': id_number,
            'secret': secret
        }
        self.redirect_url = redirect_url

    def get_oauth(self):
        """Spin up the flask server to OAuth authenticate.

        Navigate to localhost:4200. When you navigate to there,
        you must open the developer console and open to the network tab. Click the link, scroll to the bottom of
        Bungie's page, and click the authorize button. When you do so, nothing will happen, but you'll see a redirect
        network event that is cancelled (You don't need to do anything when using https. You need to copy the link
        that was attempted to direct to, and go there directly. If all is well, the script will proceed to the next
        stage.

        The resulting token will be written to ``self.token`` and file `token.json`"""
        print('No tokens saved, please authorize the app by going to localhost:4200')

        app = Flask(__name__)

        # redirect to the static html page with the link
        @app.route('/')
        def main():
            return '<a href="https://www.bungie.net/en/oauth/authorize?client_id=' + self.api_data[
                'id'] + '&response_type=code&state=asdf">Click me to authorize the script</a>'

        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @app.route('/shutdown')
        def shutdown():
            shutdown_server()
            return 'Server shutting down...'

        # catch the oauth redirect
        @app.route('/redirect')
        def oauth_redirect():
            # get the token/refresh_token/expiration
            code = request.args.get('code')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            params = {
                'grant_type': 'authorization_code',
                'client_id': self.api_data['id'],
                'client_secret': self.api_data['secret'],
                'code': code
            }
            r = requests.post('https://www.bungie.net/platform/app/oauth/token/', data=params, headers=headers)
            resp = r.json()

            # save refresh_token/expiration in token.json
            self.token = {
                'refresh': resp['refresh_token'],
                'expires': time.time() + resp['refresh_expires_in']
            }
            token_file = open('token.json', 'w')
            token_file.write(json.dumps(self.token))
            return '<a href="/shutdown">Click me to continue</a>'

        app.run(port=4200)
