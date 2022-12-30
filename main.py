import discord
from discord.ext import commands

from asyncio import sleep
import os
import random
from quart import (Quart, Response, abort, redirect, render_template, request,
                   url_for)
from quart_auth import AuthManager, AuthUser, Unauthorized
from quart_auth import login_required as auth_required
from quart_auth import login_user, logout_user
from routes.utils import app
from quart_discord import DiscordOAuth2Session
from werkzeug.exceptions import HTTPException
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Quart(__name__)
app.config["SECRET_KEY"] = "asdfhjklpoiuythrewqasdf"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = 1044131165411483708
app.config["DISCORD_CLIENT_SECRET"] = "tj17lWYfKLtrYO1SbPI1QVvqG3sQ3gw1"
app.config["DISCORD_REDIRECT_URI"] = "https://ProtonWEb-1.lostrao.repl.co/api/callback"
app.config["DISCORD_BOT_TOKEN"] = "MTA0NDEzMTE2NTQxMTQ4MzcwOA.GNALX7.AQQZftVZFgZ_vby0pAaGXZicWvGJlH12tc0q5s"


discordd = DiscordOAuth2Session(app)


# Auth
AuthManager(app)

# Routes


@app.route("/")
async def home():
    user = None
    if await discordd.authorized:
        user = await discordd.fetch_user()
    return await render_template("index.html", user=user)

@app.route("/about")
async def about():
    user = None
    if await discordd.authorized:
        user = await discordd.fetch_user()
    return await render_template("about.html", user=user)

@app.route("/dash")
async def dash():
    user = None
    if await discordd.authorized:
        user = await discordd.fetch_user()
    return await render_template("dashboard.html", user=user)

@app.route("/support")
async def support():
    user = None
    if await discordd.authorized:
        user = await discordd.fetch_user()
    return await render_template("support.html", user=user)

@app.route("/stats")
async def stats():
    user = None
    if await discordd.authorized:
        user = await discordd.fetch_user()
    return await render_template(
        "stats.html",
        users=f"500k+",
        guilds=f"86",
        commands=f"212",
        uptime=f"24h",
        user=user
    )



# API (discord etc)


@app.route("/api/login")
async def login():
    return await discordd.create_session(scopes=["identify", "guilds"])

@app.route("/api/logout")
async def logout():
    discordd.revoke()
    logout_user()
    return redirect(url_for("home"))

@app.route("/api/callback")
async def callback():
    try:
        await discordd.callback()
    except Exception:
        return redirect(url_for("login"))
    user = await discordd.fetch_user()
    login_user(AuthUser(user.id))
    return await render_template("index.html", user=user)

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
  bot.url = request.url
  return redirect(url_for(".login"))

@app.errorhandler(Exception)
async def handle_exception(error):
    name = "Internal Server Error"
    description = "Woops, something went wrong on our side. Sorry for the inconvenience!"

    if isinstance(error, HTTPException):
        name = error.name
        description = error.description

    return await render_template("error.html", error_name=name, error_msg=description)


intents=discord.Intents.all() 

bot = commands.Bot(command_prefix="$",intents = intents)
token = "MTA0NDEzMTE2NTQxMTQ4MzcwOA.GNALX7.AQQZftVZFgZ_vby0pAaGXZicWvGJlH12tc0q5s"

@bot.event
async def on_ready():
  bot.loop.create_task(app.run_task('0.0.0.0'))
  print("I'm in")

def run():  
  bot.run(token)
  

if __name__ == "__main__":
  run()