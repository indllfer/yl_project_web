from flask import Flask, render_template, request
from data import db_session
from data.users import User
from data.administrators import Admin
from data.games import Game
from sql_engine import check_cmd_amd_name_correct

import json
import random
import os
import asyncio
import time
import sql_engine


class Holding_game: 
    def __init__(self):
        self.id_game = None

    def initialising_game(self, name_game: str, info_game: str, amd_id_game: int, initial_amount_game: float, 
                          steps_game: int, step_time_game: int, other_rules_game: list):
        with open("game_template.json", "r") as template_file_game:
            dict_game = json.load(template_file_game)

        if check_cmd_amd_name_correct(name_game):
            dict_game["name_game"] = name_game
        else:
            return False

        db_sess = db_session.create_session()
        sp = [0]
        sp.extend([game.id for game in db_sess.query(Game).all()])
        last_id = max(sp)
        del sp
        self.id_game = last_id + 1
    
        dict_game["id_game"] = self.id_game
        dict_game["info_game"] = info_game
        dict_game["amd_id_game"] = amd_id_game
        dict_game["rules_game"] = {"initial_amount_game": initial_amount_game, "steps_game": steps_game, 
                                   "step_time_game": step_time_game, "other_rules_game": other_rules_game}
        dict_game["curr_step"] = 0
        dict_game["start_time"] = 0
        game = Game()
        passcode_game = random.randrange(1000, 9999)
        game.passcode = passcode_game
        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.add(game)
        db_sess.commit()

        return True
    
    def start(self):
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)
        dict_game["current_step"] = 1
        dict_game["start_time"] = time.time()
        
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.timer())
    
    #TODO протестить
    def adding_assets_game(self, asset_type, asset_listing, asset_name, asset_values):
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)
        assets_game = {"asset_type": asset_type, "asset_listing": asset_listing,
                     "asset_name": asset_name, "asset_values": asset_values}
        dict_game["assets_game"].extend(assets_game)
        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.commit()
    #TODO протестить
    def adding_news_game(self, related_asset, news_text, news_values): 
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)
        news_game = {"related_asset": related_asset, "news_text":news_text, "news_values" :news_values}
        dict_game["news_game"].extend(news_game)
        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.commit()

    #TODO протестить
    def adding_players_game(self, player_id):
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)
        players_game = {"player_id": player_id, "amount": dict_game["rules_game"]["initial_amount_game"], "amount_changing": 0, "players_assets": []}
        dict_game["players_game"].extend(players_game)
        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.commit()

    def buying_asset(self, player_id, asset_listing, asset_volume):
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)
        #TODO повеситься...
        players = dict_game["players"] 
        for i in range(len(players)):
            if dict_game["players_game"][i]["player_id"] == player_id:
                for k in range(len(dict_game["assets"])):
                    if asset_listing == dict_game["assets"][k]:
                        if dict_game["players_game"][i]["balance"] - dict_game["assets"][k]["asset_values"][0] * asset_volume >= 0:
                            dict_game["players_game"][i]["balance"] -= dict_game["assets"][k]["asset_values"][0] * asset_volume

                        else:
                            print("нельзя")

                for j in range(len(dict_game["players_game"][i]["players_assets"])):
                    if dict_game["players_game"][i]["players_assets"][j] == asset_listing:
                        dict_game["players_game"][i]["players_assets"][j]["players_asset_values"] += asset_volume
                        return

                dict_game["players_game"][i]["players_assets"].append({
                    "asset_listing": asset_listing,
                    "players_asset_values": [asset_volume]
                    })
                return

        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.commit()
        
    def prodavaying_asset(self, player_id, asset_listing, asset_volume):
        self.buying_asset(self, player_id, asset_listing, 0 - asset_volume)

    def step(self):
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)
        sl = {}
        for i in range(len(dict_game["assets_game"])):
            for j in range(len(dict_game["news_game"])):
                if dict_game["assets_game"][i]["asset_listing"] in dict_game["news_game"][j]["related_asset"]:
                    if dict_game["assets_game"][i]["asset_listing"] not in sl:
                        sl[dict_game["assets_game"][i]["asset_listing"]] = [dict_game["news_game"][j]]

                    else:
                        sl[dict_game["assets_game"][i]["asset_listing"]].append(dict_game["news_game"][j])

        for i, v in sl.items():
            v = v[random.randint(0, len(v))]
            if dict_game["assets_game"][i]["asset_type"] == "share":
                dict_game["assets_game"][i]["asset_values"][0] *= 1 + (random.uniform(*v["news_values"]) / 100)
                
            elif dict_game["assets_game"][i]["asset_type"] == "deposit":
                dict_game["assets_game"][i]["asset_values"][0] += random.uniform(*v["news_values"][:2])
        
        for i in range(len(dict_game["players_game"])):
            amount = dict_game["players_game"][i]["amount"]
            for j in range(len(dict_game["players_game"][i]["players_assets"])):
                if dict_game["players_game"][i]["players_assets"][j]["asset_listing"] in [i["asset_listing"] for i in dict_game["assets"] if i["asset_type"] == "share"]:
                    amount += dict_game["players_game"][i]["players_assets"]["players_asset_values"]
                    [0] * [i["asset_values"][0] for i in dict_game["assets"] if i["asset_listing"] == dict_game["players_game"][i]["players_assets"][j]["asset_listing"]][0]

                else:
                    amount += dict_game["players_game"][i]["players_assets"][j]["players_asset_values"][1]

            dict_game["players_game"][i]["amount_changing"] = amount - dict_game["players_game"][i]["amount"]
            dict_game["players_game"][i]["amount"] = amount

        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.commit()

    async def timer(self):
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        db_sess.commit()
        dict_game = json.loads(game.gameinfo)
        
        while True:
            db_sess = db_session.create_session()
            game = db_sess.query(Game).filter(Game.id == self.id_game).first()
            dict_game = json.loads(game.gameinfo)
            await asyncio.sleep(dict_game["rules_game"]["step_time_game"]) 
            if dict_game["curr_step"] >= dict_game["rules_game"]["steps_game"]:
                break

            self.step()
            dict_game["curr_step"] += 1
            game.gameinfo = bytes(json.dumps(dict_game), "utf8")
            db_sess.commit()
            print(dict_game["curr_step"])

        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == self.id_game).first()
        dict_game = json.loads(game.gameinfo)

        game.gameinfo = bytes(json.dumps(dict_game), "utf8")
        db_sess.commit()

    def anekdot(self):
        os.mkdir("/system")


db_session.global_init("db/invexgame.db")
ex = Holding_game()


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        print(f'Логин: {login}. Пароль: {password}')
        sql_engine.player_authorization(login, password)

    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        team_name = request.form.get('team_name')
        team_info = request.form.get('team_info')
        team_team = request.form.get('team_team')
        print(f'Логин: {login}. Пароль: {password}')
        sql_engine.player_registration(login, password, team_name, team_info, team_team)
 
    return render_template('reg.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def adm_log():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        print(f'Логин: {login}. Пароль: {password}')
        sql_engine.admin_authorization(login, password)

    return render_template('admin_login.html')


@app.route('/admin_registration', methods=['GET', 'POST'])
def adm_reg():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        amd_name = request.form.get('adm_name')
        amd_info = request.form.get('adm_info')
        print(f'Логин: {login}. Пароль: {password}')
        sql_engine.admin_registration(login, password, amd_name, amd_info)
    
    return render_template('admin_reg.html')


app.run(port=8080, host='127.0.0.1')