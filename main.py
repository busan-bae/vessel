from flask import Flask,render_template
from flask_wtf.csrf import CSRFProtect  # CSRF 추가
from flask_login import current_user,login_required
from flask_login import LoginManager
from functools import wraps
from flask import abort
from models import db, User
from config import Config
from auth import login_route, register_route,logout_route
from vessels import vessel_list, vessel_add 


# 플라스크 기본 세팅
app = Flask (__name__)

# login manager 초기화
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 필요 시 리다이렉트
login_manager.login_message = '로그인이 필요합니다.'  # 한글 메시지
app.config.from_object(Config)

# SQL 연결
db.init_app(app)
# CSRF 사용
csrf = CSRFProtect(app)

# db 생성
with app.app_context():
    db.create_all()

# home page render 로그인 되어 있지 않으면 자동으로 login 페이지로  8리다이렉트 한다.
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)        
    return decorated_function

# User 로더 함수 (필수!)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 로그인 
@app.route('/login', methods = ["GET", "POST"])
def login():
    return login_route()


#회원가입
@app.route("/register", methods =['GET','POST'])
def register():
    return register_route()  


#로그아웃
@app.route('/logout')
@login_required
def logout():
    return logout_route()


#홈화면
@app.route('/')
@login_required
def home():
    return render_template('index.html',logged_in = current_user.is_authenticated)


# ---- 선박관련 ----
@app.route('/vessels')
@login_required
def vessels():
    return vessel_list()

@app.route('/vessels/add' ,methods=["GET", "POST"])
@login_required
def add_vessel():
    return vessel_add()


if __name__ == "__main__":
    app.run(debug=True)