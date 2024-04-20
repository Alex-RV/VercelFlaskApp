from flask import Flask, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a random secret in production

oauth = OAuth(app)

google = oauth.register(
    'google',
    client_id='543215093064-ag7aolf3p9pt3b5umnfi8pcff3mhguk2.apps.googleusercontent.com',
    client_secret='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',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def index():
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    # Generate a state token to prevent request forgery.
    # Store it in the session for later validation.
    state = secrets.token_urlsafe(32)
    session['state'] = state
    redirect_uri = url_for('authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, state=state)

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/auth/callback')
def authorized():
    # Specify the state when fetching the token to perform CSRF check
    state = session.get('state')
    token = oauth.google.authorize_access_token(state=state)
    if 'error' in token:
        return 'Access denied: reason={} error={}'.format(
            token.get('error_reason', 'No reason provided'),
            token.get('error_description', 'No error description provided')
        )
    session['google_token'] = (token['access_token'], '')
    
    resp = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    
    # Perform operations with the user's information here
    # ...
    # Redirect the user back to your ChatGPT interface with the necessary info
    return redirect('https://chat.openai.com/aip/g-a47cfb427aedec8f3186a6aa70dd24e981f715d9/oauth/callback')

if __name__ == "__main__":
    app.run(debug=True)