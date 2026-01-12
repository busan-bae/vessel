from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

def login_route():
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


def register_route():
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

def logout_route():
    logout_user()
    return redirect(url_for('login'))
          