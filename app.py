from flask import Flask, render_template, redirect
import requests

app = Flask(__name__)


# index page
@app.route("/")
def index():
    return render_template("index.html")


# games generation from db
def show_games(html_page):
    groups = requests.get("https://98913jvwib.execute-api.eu-central-1.amazonaws.com/prod/groups/").json()
    group_names = []
    for group_name_index in range(int(groups["Count"])):
        group_names.append(groups["Items"][group_name_index]["group_name"]["S"])
    
    games = requests.get("https://98913jvwib.execute-api.eu-central-1.amazonaws.com/prod/games/").json()["Items"]
    games_by_group_name = []
    for game_group in group_names:
        first = True
        for game in games:
            if game['group_name']['S'] == game_group:
                if first == True:
                    games_by_group_name.append([game])
                else:
                    games_by_group_name[group_names.index(game_group)].insert(-1, game)

                first = False

    return render_template(f"{html_page}.html", group_names=group_names, games_by_group_name=games_by_group_name)


# games page
@app.route("/games")
def games():
    return show_games("games")


# specific game page
@app.route("/games/<string:game_id>")
def game(game_id):
    for game_in_db in requests.get("https://98913jvwib.execute-api.eu-central-1.amazonaws.com/prod/games/").json()["Items"]:
        if game_in_db["game_id"]["S"] == game_id:
            game = game_in_db

    return render_template("game.html", game=game)


# tutorials page
@app.route("/tutorials")
def tutorials():
    return show_games("tutorials")


@app.route("/tutorial/<string:game_id>")
def tutorial(game_id):
    for game_in_db in requests.get("https://98913jvwib.execute-api.eu-central-1.amazonaws.com/prod/games/").json()["Items"]:
        if game_in_db["game_id"]["S"] == game_id:
            tutorial = game_in_db["tutorial_link"]["S"]

    return redirect(tutorial)


if __name__ == "__main__":
    app.run(debug=True)