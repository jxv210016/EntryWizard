from flask import Flask, redirect, request, jsonify, Blueprint
from .utils.oauth import get_discord_login_url, exchange_code

app = Flask(__name__)

main = Blueprint('main', __name__)

@app.route('/login/discord')
def discord_login():
    return redirect(get_discord_login_url())


@app.route('/login/discord/callback')
def discord_callback():
    code = request.args.get('code')
    user_info = exchange_code(code)
    # Handle user_info as needed (e.g., creating a user session)
    return jsonify(user_info)


if __name__ == '__main__':
    app.run(debug=True)
