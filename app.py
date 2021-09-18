from os import error
import functools
from sqlalchemy import desc
from flask import Flask, jsonify, request,render_template,session,g,redirect,url_for
from werkzeug.security import check_password_hash, generate_password_hash
from models import db,Forms,Users,Formdata
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/myforms'

with app.app_context():
   db.init_app(app)
   db.create_all()

#login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')



@app.route('/' , methods=['GET','POST'])
def adminLogin():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('adminLogin.html', form=form)
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Locate user
        #email is used as username
       
        user = Users.query.filter_by(email=username).first()
   
        if user and check_password_hash(user.password, password):        
            session.clear()
            #storing user_id in the session
            #it will be used to check if admin is logged in
            session['user_id'] = user.id
            return  redirect(url_for('dashboard'))
        
        return render_template( 'adminLogin.html', msg='Wrong user or password', form=form)


#Logout feature

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('adminLogin'))


# checks if a user id is stored in the session

@app.before_request
def load_logged_in_user():
    user = session.get('user_id')
    if user is None:
        g.user = None
    else:
        username =  Users.query.filter_by(id=user).first()
        g.user = username.id

# This function will check if user is logged in or not

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('adminLogin'))

        return view(**kwargs)

    return wrapped_view

@login_required
@app.route('/home',methods = ['GET'])
def dashboard():
    forms = Forms.query.filter_by(user_id=g.user).order_by(desc(Forms.creation_date)).all() 
    return render_template('dashboard.html',forms=forms)


# @login_required
# @app.route('/newform/<int:fid>',methods = ['GET'])
# def newform(fid):    
#     return render_template('index.html',fid = fid)


@login_required
@app.route('/newform',methods = ['GET'])
def newform():
    try:
        newForm = Forms()
        newForm.user_id = g.user 
        db.session.add(newForm)
        db.session.commit()

    except Exception as e:
        print(e)

    return redirect(url_for('edit_f',fid=newForm.id))



@login_required
@app.route('/editForm/<int:fid>',methods = ['GET'])
def edit_f(fid):
    form = Forms.query.filter(Forms.id==fid).first()
    
    if not form.edit_form:
        return render_template('index.html')
    
    return render_template('edit_form.html',form_data=form.edit_form,fid=fid)


@login_required
@app.route('/editForm/<int:fid>/save',methods = ['POST'])
def save(fid):
    form = Forms.query.filter(Forms.id==fid).first()
    
    if form.user_id != g.user:
        return "error"

    form_content = request.form['javascript_data']
    edit_form =  request.form['edit_data']
    user_id = g.user

    try:
        form.form_content = form_content
        form.edit_form = edit_form
        form.user_id = user_id
         
        db.session.commit()

    except Exception as e:
        print(e)
        return "error"
    
    return "success"


@app.route('/form/<int:fid>',methods = ['GET','POST'])
def render_f(fid):
    form = Forms.query.filter(Forms.id==fid).first()
    if request.method == 'POST':
        print(request.form)
        print(request.files.items())
        return render_template('thankyoupage.html')
    return render_template('render_form.html',form_data=form.form_content)




if __name__ == '__main__':
    app.run(debug=True ,port=8000)
