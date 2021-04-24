from Class.Application import Application as app
from Models.Comment import Comment
from flask import jsonify, make_response, url_for
from Class.Interfase.IController import IController
from flask_login import current_user
from Class.MakeResponse import MakeResponse
from Models.Sound import Sound


class UploadCommentController(IController):
    def __call__(self, massed, *args, **kwargs):
        req = massed.get_json()
        comment = Comment(text=req["text"],
                          id_sound=req["id"],
                          id_user=current_user.id)
        sound = app().context.query(Sound).filter(Sound.id == req['id']).first()
        sound.comments += 1
        app().context.add(comment)
        app().context.commit()
        res = make_response(jsonify({"data": "succesfull"}), 200)
        return res
