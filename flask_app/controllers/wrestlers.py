from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models import wrestler, bio
from flask_app.controllers import promoters

@app.route('/')
def registration_page():
    return render_template('wrestler_index.html')

# POST wrestler registration
@app.route('/wrestler/register', methods=['POST'])
def register_wrestler():
    if wrestler.Wrestler.create_wrestler(request.form):
        return redirect('/wrestler/bio')
    return render_template('wrestler_index.html')

@app.route('/wrestler/bio')
def wrestler_bio():
    if not 'wrestler_id' in session:
        return redirect ('/')
    return render_template('bio.html')

# POST wrestler login
@app.route('/wrestler/login', methods = ['POST'])
def wrestler_login():
    if wrestler.Wrestler.login_wrestler(request.form):
        return redirect('/wrestler/complete')
    return render_template('wrestler_index.html')

# POST bio form
@app.route('/wrestler/register_bio', methods = ['POST'])
def register_wrestler_bio():
    if bio.Bio.create_bio(request.form):
        return redirect('/wrestler/complete')
    return render_template('bio.html')

# POST edit bio form
@app.route('/wrestler/edit_bio', methods = ['POST'])
def change_wrestler_bio():
    bio.Bio.change_bio(request.form)
    return redirect('/wrestler/complete')

@app.route('/wrestler/complete')
def wrestler_registration_complete():
    if not 'wrestler_id' in session:
        return redirect ('/')
    return render_template('complete.html')

@app.route('/wrestler/<int:id>')
def wrestler_information(id):
    if not 'promoter_id' in session:
        return redirect ('/promoter')
    data={
        'id' : id
    }
    one_bio=bio.Bio.get_one_bio_with_creator(data)
    return render_template('wrestler_information.html', one_bio=one_bio)

@app.route('/wrestler/bio/edit/<int:id>')
def change_bio(id):
    if not 'wrestler_id' in session:
        return redirect('/')
    data = {
        'id' : id
    }
    one_bio=bio.Bio.get_bio_by_wrestler_id(data)
    return render_template('editbio.html', one_bio=one_bio)

@app.route('/logout')
def logout_wrestler():
    session.clear()
    return redirect('/')