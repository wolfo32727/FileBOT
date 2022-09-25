from itertools import permutations
from xmlrpc.client import ServerProxy
from flask import Flask, render_template, request, redirect, session, jsonify
import stepboard as step


app = Flask(__name__)

link = "https://discord.com/api/oauth2/authorize?client_id=1021830174905475102&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fzaloguj&response_type=code&scope=identify%20guilds"

app.config["SECRET_KEY"] = "xyz"

step.configdb["CLIENT_ID"] = "1021830174905475102"
step.configdb["CLIENT_SECRET"] = "GjZt3yawmH-DOcWcufQDh70Y_WU8vikN"
step.configdb["REDIRECT_URI"] = "http://127.0.0.1:5000/zaloguj"
step.configdb["BOT_TOKEN"] = "MTAyMTgzMDE3NDkwNTQ3NTEwMg.GS6865.4Exf9rrww1IzJSkd-oPzlWI7m_kxGO9QSJWsik"

@app.route("/")
def strona():
    return render_template("index.html", link=link)

@app.route("/zaloguj")
def zaloguj():
    code = request.args.get("code")
    token = step.authorization_token(code)
    session["token"] = token
    return render_template("index.html")


@app.route("/wyloguj")
def wyloguj():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dash():
    x = session.get("token")
    if x == None:
        return redirect("/")
    user = step.user_data(x)
    bot_servers = step.bot_guilds()
    you_servery = step.user_guilds(session.get("token"))
    list_server = step.common_guilds(you_servery, bot_servers)
    #return jsonify(list_server)
    return render_template("dash.html", user=user, servers=list_server, permission=0x8)

@app.route("/panel/<idserver>")
def panel(idserver):
    info = step.guild_data(idserver)
    #return jsonify(info)
    return render_template("panel.html", info=info)





if __name__ == "__main__":
    app.run(debug=True)