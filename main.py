from flask import Flask,render_template,redirect, url_for,request,flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf.csrf import CSRFProtect  # CSRF 추가
from flask_login import UserMixin,login_user, current_user,login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
import os
from functools import wraps
from flask import abort

load_dotenv()

# 플라스크 기본 세팅
app = Flask (__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vessel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# login manager 초기화
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 필요 시 리다이렉트
login_manager.login_message = '로그인이 필요합니다.'  # 한글 메시지

# SQL 연결
db = SQLAlchemy(app)
# CSRF 사용
csrf = CSRFProtect(app)

# DB 설계 -> 추후 분리 
class Base(DeclarativeBase):
    pass

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True)   
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

# db 생성
with app.app_context():
    db.create_all()

# home page render 로그인 되어 있지 않으면 자동으로 login 페이지로 리다이렉트 한다.
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

@app.route('/')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("id")
        password = request.form.get("password")
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            flash("아이디가 존재하지 않습니다.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password,password):
            flash("비밀번호가 일치하지 않습니다.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html",logged_in = current_user.is_authenticated)

@app.route("/register", methods =['GET','POST'])
def register():
    if request.method == 'POST':
        existing_user = db.session.query(User).filter_by(user_id=request.form.get('id')).first()
        if existing_user:
            flash('이미 등록된 사용자 입니다.')
            return redirect(url_for('register'))
        else:
            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            
            new_user = User(
                user_id=request.form.get('id'),
                name=request.form.get('name'),
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            flash('회원가입이 완료 되었습니다! 로그인해주세요.')
        return  redirect(url_for('login'))#나중에 login으로 변경
    return render_template("register.html")    
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)