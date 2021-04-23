from Class.Application import Application

from Controller.ListSoundLoadController import ListSoundLoadController
from Controller.LoadMusicController import LoadMusicController
from Controller.LoginController import LoginController
from Controller.ReqistrationController import ReqistrationController
from Controller.UploadMusicController import UploadMusicController
from Controller.ProfileController import MyProfileController
from Controller.GetMusicController import GetMusicController
from Controller.AddListMusicController import AddListMusicController
from Controller.AddLikeController import AddLikeController
from Controller.AddDislikeController import AddDislikeController
from Controller.AddListeningController import AddListeningController

from forms.LoginForm import LoginForm
from forms.ReqistrationForm import RegisterForm
from forms.UploadMusicForm import UploadMusicForm
from forms.ProfileForm import ProfileForm

from Models.User import User
from Models.Sound import Sound

import os
import pickle

from flask import Flask, render_template, redirect, request, abort, session, make_response, jsonify
from flask_login import login_user, logout_user, login_required
from sqlalchemy import desc
from forms.comment import Comment

Application().app = Flask(__name__)
app = Application().app

app.config["FILE_DIR"] = os.path.dirname(os.path.abspath(__file__))

login_manager = Application().login_manager
state = 'Новые треки'

@login_manager.user_loader
def load_user(user_id):
    db_sess = Application().context
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    global state
    state = 'Новые треки'
    if request.method == 'POST':
        if "new" in request.form:
            state = 'Новые треки'
        elif 'views' in request.form:
            state = 'По прослушиваниям'
        elif 'likes' in request.form:
            state = 'По лайкам/дизлайкам'
        elif 'my' in request.form:
            state = 'Мои треки'
        elif 'search' in request.form:
            state = f'Найденные треки по запросу: {request.form.get("text")}'
    return render_template("index.html", title='Musical Wind', state=state)


@app.route("/upload_music",  methods=['GET', 'POST'])
@login_required
def upload_music():
    controller = UploadMusicController(model=UploadMusicForm())
    return controller()


@app.route("/load_music_view",  methods=['GET', 'POST'])
def load_music_view():
    global state
    controller = LoadMusicController()
    return controller(request, state)


@app.route("/list_sound_view",  methods=['GET', 'POST'])
@login_required
def list_sound_view():
    controller = ListSoundLoadController()
    return controller(request)


@app.route("/get_music",  methods=['GET', 'POST'])
def get_music():
    controller = GetMusicController()
    return make_response(jsonify({"data": controller(request.get_json())}), 200)

@app.route("/add_listening",  methods=['GET', 'POST'])
def add_listening():
    snd = Application().context.query(Sound).filter(Sound.id == request.get_json()["id"]).first()
    if f'{snd.id}viewed' not in session:
        listn = pickle.loads(snd.listening)
        listn.append(0)
        snd.listening = pickle.dumps(listn)
        session[f'{snd.id}viewed'] = 1            
        Application().context.commit()
    return 'a'

@app.route("/add_list_music",  methods=['GET', 'POST'])
@login_required
def add_list_music():
    controller = AddListMusicController()
    return controller(request)

@app.route("/add_like",  methods=['GET', 'POST'])
@login_required
def add_like_music():
    controller = AddLikeController()
    return controller(request)

@app.route("/add_dislike",  methods=['GET', 'POST'])
@login_required
def add_dislike_music():
    controller = AddDislikeController()
    return controller(request)

@app.route("/my_profile",  methods=['GET', 'POST'])
@login_required
def my_profile():
    model = ProfileForm()
    controller = MyProfileController(model=model)
    return controller()


@app.route('/login', methods=['GET', 'POST'])
def login():
    controller = LoginController(model=LoginForm(), login_user=login_user)
    return controller()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    controller = ReqistrationController(model=RegisterForm(), login_user=login_user)
    return controller()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

def main():
    Application().create_context("db/sound.db")
    
    app.run()


if __name__ == '__main__':
    main()
