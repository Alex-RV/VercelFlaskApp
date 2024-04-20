from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a random secret in production

oauth = OAuth(app)

google = oauth.register(
    'google',
    client_id='543215093064-ag7aolf3p9pt3b5umnfi8pcff3mhguk2.apps.googleusercontent.com',
    client_secret='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',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'email profile'},
)

@app.route('/')
def index():
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/auth/callback')
def authorized():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    # Do something with the user_info
    return redirect('https://your-chatgpt-interface.url/')

if __name__ == "__main__":
    app.run(debug=True)  # Running with HTTP for local testing
