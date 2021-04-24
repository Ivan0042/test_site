from Class.Application import Application as app
from Models.Sound import Sound
from Models.Comment import Comment
from flask import jsonify, make_response, url_for
from Class.Interfase.IController import IController
from flask_login import current_user
from Class.MakeResponse import MakeResponse
from Models.User import User
import pickle


class GetMusicController(IController):
    def __call__(self, massed, *args, **kwargs):
        sound = app().context.query(Sound).filter(Sound.id == massed["id"]).first()
        sound = MakeResponse.make_response_sound(sound.__dict__)
        sound['id_user'] = app().context.query(User).filter(User.id == sound['id_user']).first().__dict__['nickname']
        sound["comments"] = len(app().context.query(Comment).filter(Comment.id_sound == sound["id"]).all())
        return sound
