from flask import Flask, redirect, request, session, render_template, url_for
import urllib.parse

app = Flask(__name__)
app.secret_key = "секретний_ключ_сюди" 

STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"

@app.route('/')
def home():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route('/login')
def login():
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": url_for("authorize", _external=True),
        "openid.realm": request.url_root,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
    }
    query_string = urllib.parse.urlencode(params)
    return redirect(f"{STEAM_OPENID_URL}?{query_string}")

@app.route('/authorize')
def authorize():
    claimed_id = request.args.get("openid.claimed_id")
    if claimed_id and "steamcommunity.com/openid/id/" in claimed_id:
        steam_id = claimed_id.split("/")[-1]
        session["user"] = {"steamid": steam_id}
        return redirect(url_for("home"))
    return "Помилка авторизації!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
