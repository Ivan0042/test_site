from Class.Application import Application as app
from Models.Sound import Sound
from flask import jsonify, make_response, url_for, redirect
from Class.Interfase.IController import IController
from flask_login import current_user
from Class.MakeResponse import MakeResponse
import pickle


class AddLikeController(IController):
    def __call__(self, massed, *args, **kwargs):
        req = massed.get_json()
        sound = app().context.query(Sound).filter(Sound.id == req['id']).first()
        users = pickle.loads(sound.like)
        users2 = pickle.loads(sound.dislike)
        if current_user.id in users:
            users.remove(current_user.id)
        else:
            users.append(current_user.id)
        if current_user.id in users2:
            users2.remove(current_user.id)
        sound.like = pickle.dumps(users)
        sound.dislike = pickle.dumps(users2)
        app().context.commit()
        res = make_response(jsonify({"data": "succesfull"}), 200)
        return res
