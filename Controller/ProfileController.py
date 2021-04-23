import os
from werkzeug.utils import secure_filename
from Class.Application import Application as app
from Models.User import User
from flask import redirect, render_template
from Class.Interfase.IController import IController
from flask_login import current_user


class MyProfileController(IController):
    def __init__(self, view=None, model=None):
        self.__view = view
        self.__model = model

    def __call__(self, *args, **kwargs):
        img = self.__model.img.data
        if img is not None:
            filename_img = secure_filename(img.filename).split(".")
            filename_img = os.path.join('img', os.urandom(15).hex() + "." + filename_img[-1])
            img.save(os.path.join(app().app.config["FILE_DIR"], "static", filename_img))
            filename_img = filename_img.replace('\\', "/")
            if current_user.icon != 'lol.png':
                os.remove(os.path.join(app().app.config["FILE_DIR"], "static", current_user.icon))
        else:
            filename_img = current_user.icon

        now_user = app().context.query(User).filter(User.id == current_user.id).first()
        if self.__model.name.data is not None:
            now_user.name = self.__model.name.data
        if self.__model.email.data is not None:
            now_user.email = self.__model.email.data
        if self.__model.sename.data is not None:
            now_user.sename = self.__model.sename.data
        if self.__model.nickname.data is not None:
            now_user.nickname = self.__model.nickname.data
        if self.__model.phone.data is not None:
            now_user.phone = self.__model.phone.data
        if self.__model.phone.data is not None:
            now_user.birthday = self.__model.birthday.data
        now_user.icon = filename_img
        app().context.commit()
        return render_template('profile.html', title='Профиль', form=self.__model)
