from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import db, Vessel

def vessel_list():
    """선박 목록 조회"""
    vessels = Vessel.query.all()
    return render_template("vessel_list.html", vessels = vessels)


# TODO: 나중에 구현할 내용
# def vessel_detail(vessel_id):
#     """선박 상세 정보"""
#     vessel = Vessel.query.get_or_404(vessel_id)
    

def vessel_add():
    """선박 추가"""
    if request.method == 'POST' : 
        new_vessel = Vessel(
            vessel_name=request.form.get('vessel_name'),
            imo_number=request.form.get('imo_number'),
            vessel_type=request.form.get('vessel_type'),
            flag=request.form.get('flag'),
            build_year=request.form.get('build_year')
        )
        db.session.add(new_vessel)
        db.session.commit()
        return redirect(url_for('vessels'))
    return render_template('vessel_add.html')
