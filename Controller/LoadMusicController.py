from Class.Application import Application as app
from Models.Sound import Sound
from flask_login import current_user
from flask import jsonify, make_response
from Class.Interfase.IController import IController
from Class.MakeResponse import MakeResponse
from Models.Comment import Comment
from sqlalchemy import desc, asc
import pickle


class LoadMusicController(IController):
    def __call__(self, massed, state):
        req = massed.get_json()
        sounds = app().context.query(Sound).order_by(desc(Sound.created_date))
        if state == 'Новые треки':
            sounds = app().context.query(Sound).order_by(desc(Sound.created_date))
        elif state == 'По прослушиваниям':
            sounds = app().context.query(Sound).order_by(asc(Sound.listening))
        elif state == 'По лайкам/дизлайкам':
            sounds = sorted(sounds, key=lambda x: len(pickle.loads(x.like)) - len(pickle.loads(x.dislike)))
            sounds.reverse()
        elif state == 'Мои треки':
            sounds = app().context.query(Sound).filter(Sound.id_user == current_user.id).order_by(desc(Sound.created_date))
        elif 'Найденные треки по запросу:' in state:
            sounds = app().context.query(Sound).filter(Sound.name.like(f'%{state[28:]}%')).order_by(desc(Sound.created_date))
        sounds = list(map(lambda x: MakeResponse.make_response_sound(x.__dict__), sounds))
        for i in sounds:
            i["comments"] = len(app().context.query(Comment).filter(Comment.id_sound == i["id"]).all())        
        res = make_response(jsonify({"data": sounds}), 200)
        return res


