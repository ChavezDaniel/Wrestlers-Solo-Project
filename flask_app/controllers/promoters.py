from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models import promoter, bio, job_post
from flask_app.models.promoter import Promoter

@app.route('/promoter')
def start_promoter():
    return render_template('promoter_index.html')

# POST promoter registration
@app.route('/promoter/register', methods=['POST'])
def register_promoter():
    if promoter.Promoter.create_promoter(request.form):
        return redirect(f'/promoter/home/{session["promoter_id"]}')
    return render_template('promoter_index.html')

@app.route('/promoter/home/<int:id>')
def promoter_home(id):
    if not 'promoter_id' in session:
        return redirect ('/promoter')
    data = {
        'id' : id
    }
    this_promoter = Promoter.get_promoter_with_positions(data)
    return render_template('home.html', all_wrestlers=bio.Bio.get_all_bios_with_creator(), this_promoter=this_promoter)

@app.route('/position/view/<int:id>')
def view_position(id):
    if not 'promoter_id' in session:
        return redirect ('/promoter')
    data = {
        'id' : id
    }
    this_position=job_post.Job.get_position_by_id(data)
    return render_template('viewposition.html', this_position=this_position, all_wrestlers=bio.Bio.get_all_bios_with_creator())

# POST promoter login
@app.route('/promoter/login', methods = ['POST'])
def promoter_login():
    if promoter.Promoter.login_promoter(request.form):
        return redirect(f'/promoter/home/{session["promoter_id"]}')
    return render_template('promoter_index.html')

@app.route('/position')
def position():
    if not 'promoter_id' in session:
        return redirect('/promoter')
    return render_template('position.html')

@app.route('/position/delete/<int:id>')
def trash_position(id):
    job_post.Job.throw_away_position(id)
    return redirect(f'/promoter/home/{session["promoter_id"]}')

# POST position registration info
@app.route('/position/create', methods = ['POST'])
def register_position():
    if job_post.Job.create_job(request.form):
        return redirect(f'/promoter/home/{session["promoter_id"]}')
    render_template('position.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')