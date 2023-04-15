from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, SelectField, Form, SelectMultipleField
from wtforms.validators import DataRequired
from db import connection
import json
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'super_secret'
bootstrap = Bootstrap(app)
moment = Moment(app)
conn = connection(host = 'cmsc508.com', database = '22FA_team32', user = 'shieldsn', password = 'V01000930')



# |--------------------------------------------------------------------------------------------|
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Classes ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |--------------------------------------------------------------------------------------------|

# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Home and Login Classes ~ * ~ * ~ * ~ * ~ * ~ * ~
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
class User(UserMixin):
    def __init__(self, id):
        self.id = id

class LoginForm(FlaskForm):
    user = StringField('VID:', validators=[DataRequired()])
    password = StringField('PASSWORD:', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cond = False
    
class AdminSelectionForm(FlaskForm):
    insert = SubmitField('Insert')
    delete = SubmitField('Delete')
    view = SubmitField('view')
    update = SubmitField('update')

# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Delete Classes ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
class DeleteForm(FlaskForm):
    table = StringField('Table', validators=[DataRequired()]) #drop down of all tables
    data = StringField('Data', validators=[DataRequired()]) # Where blank = blank
    submit = SubmitField('Submit')


# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Select Classes ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 


# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Insert Classes ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
class TutorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    vnumber = StringField('Vnumber', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CourseForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    submit = SubmitField('Submit')

# class ExpertiseForm(FlaskForm):
#     name = SelectField('Name', choices = [], validators=[DataRequired()])
#     course_codes = SelectMultipleField('course code', choices = [], validators=[DataRequired()])
#     submit = SubmitField('Submit')

class AvailabilityForm(FlaskForm):
    name = SelectField('Name', choices = [], validators=[DataRequired()])
    course_codes = SelectMultipleField('course code', choices = [], validators=[DataRequired()])
    days = SelectMultipleField('Days', choices = [], validators=[DataRequired()])
    times = SelectMultipleField('Times', choices = [], validators=[DataRequired()])
    submit = SubmitField('Submit')

# class SessionForm(FlaskForm):
#     course_code = SelectField('Course Code', choices = [], validators=[DataRequired()])
#     time_slots = SelectMultipleField('Times', choices = [], validators=[DataRequired()])
#     submit = SubmitField('Submit')

# class SessionNameForm(FlaskForm):
#     name = SelectField('Name', choices = [], validators=[DataRequired()])
#     submit = SubmitField('Submit')

# class SelectSessionForm(FlaskForm):
#     name = SelectField('Name', choices = [], validators=[DataRequired()])
#     course_code = SelectField('Course Code', choices = [], validators=[DataRequired()])
#     time = SelectField('Times', choices = [], validators=[DataRequired()])
#     day = SelectField('Times', choices = [], validators=[DataRequired()])
#     submit = SubmitField('Submit')


# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Update Classes ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
class UpdateForm(FlaskForm):
    table = StringField('Table', validators=[DataRequired()]) #drop down of all tables
    data = StringField('Data', validators=[DataRequired()]) # set (drop down) = (text box) where (drop down) = (text box)
    updates = StringField('Updates', validators=[DataRequired()])
    submit = SubmitField('Submit')





# |--------------------------------------------------------------------------------------------|
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Routing ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |--------------------------------------------------------------------------------------------|

# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Error Handling ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Login Manager ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# Load user
@login_manager.user_loader
def load_user(user_id):
    users = getUsers()
    if user_id in users:
        return User(user_id)
    return None

# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Login and Home Pages ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# Login home
@app.route('/login', methods=['GET', 'POST'])
def login():
    vid = None
    password = None
    form = LoginForm()
    #cond = True
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        users = getUsers()
        if user in users and users[user] == password:
            user = User(user)
            login_user(user)
            return redirect(url_for('selections'))
        #cond = False
        # if vid == "V12345678" and password == "password123": #this needs to be a part of the users table in the db, check that
        #     return render_template('user.html')
        # elif vid == "V00000000" and password == "password000":
        #     return render_template('admin.html')
        # else:
        #     return render_template('login.html', form = form, vid = vid, password = password, cond = True)
    return render_template('login.html', form = form)

@app.route('/selections', methods=['GET', 'POST'])
@login_required
def selections():
    return render_template("admin.html")

# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Delete Pages ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    table = None
    data = None
    form = DeleteForm()
    if form.validate_on_submit():
        table = form.table.data
        data = json.loads(form.data.data)

        # dict that contains a table, and a data dict. In data dict, key = column, value = value
        key = conn.delete({"table":table,"data":data})

    return render_template('delete.html', form = form)

# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Update Pages ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    table = None
    data = None
    updates = None
    form = UpdateForm()
    if form.validate_on_submit():
        table = form.table.data
        data = json.loads(form.data.data)       
        updates = json.loads(form.updates.data)

        # dict that contains a table, and a data dict. In data dict, key = column, value = value
        result = conn.update({"table":table,"data":data,"updates":updates})

    return render_template('update.html', form = form)


# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Insert Pages ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
@app.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    return render_template('insert.html')

@app.route('/insert_tutor', methods=['GET', 'POST'])
@login_required
def insert_tutor():
    name = None
    vnumber = None
    form = TutorForm()

    if form.validate_on_submit():
        name = form.name.data
        vnumber = form.vnumber.data
        conn.insert({"table":"tutor","data":{"tutor_name":name,"tutor_vnumber":vnumber}})

    return render_template('insert_tutor.html', form = form)

@app.route('/insert_user', methods=['GET', 'POST'])
@login_required
def insert_user():
    user = None
    password = None
    form = UserForm()

    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        conn.insert({"table":"user","data":{"user":user,"password":password}})

    return render_template('insert_user.html', form = form)

@app.route('/insert_course', methods=['GET', 'POST'])
@login_required
def insert_course():
    courseID = None
    form = CourseForm()

    if form.validate_on_submit():
        course_code = form.course_code.data
        conn.insert({"table":"course","data":{"course_code":course_code}})

    return render_template('insert_tutor.html', form = form)

@app.route('/insert_expertise', methods=['GET', 'POST'])
@login_required
def insert_expertise():

    name = None
    names = None
    course_codes = None
    all_course_codes = None
    form = ExpertiseForm()

    names = conn.select({"table":"tutor","data":{},"columns":["tutor_vnumber, tutor_name"]})
    all_course_codes = conn.select({"table":"course","data":{},"columns":["course_code"]})
    all_course_codes = [(code[0],code[0]) for code in all_course_codes]
    
    form.course_codes.choices = all_course_codes
    form.name.choices = names

    if form.validate_on_submit():
        course_codes = form.course_codes.data
        name = form.name.data
        for code in course_codes:
            conn.insert({"table":"expertise","data":{"expertise_code":code,"expertise_vnumber":name}})
    
    return render_template('insert_expertise.html', form = form)

@app.route('/insert_availability', methods=['GET', 'POST'])
@login_required
def insert_availability():
    name = None
    course_codes = None
    times = None
    days = None
    form = AvailabilityForm()

    names = conn.select({"table":"tutor","data":{},"columns":["tutor_vnumber, tutor_name"]})
    all_course_codes = conn.select({"table":"course","data":{},"columns":["course_code"]})
    all_course_codes = [(code[0],code[0]) for code in all_course_codes]


    form.name.choices = names
    form.course_codes.choices = all_course_codes
    form.days.choices = [('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday'), ('saturday', 'saturday')]
    form.times.choices = [('100', '100'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500'), ('600', '600'), ('700', '700')]

    if form.validate_on_submit():
        name = form.name.data
        course_codes = form.course_codes.choices
        days = form.days.data
        times = form.times.data
        for day in days:
            for time in times:
                for code in course_codes:
                    conn.insert({"table":"availability","data":{"availability_vnumber":name, "availability_day":day,"availability_time":time, "availability_code":code}})
    
    return render_template('insert_availability.html', form = form)


@app.route('/insert_sessionName', methods=['GET', 'POST'])
@login_required
def insert_sessionName():
    name = None
    form = SessionNameForm()

    names = conn.select({"table":"tutor","data":{},"columns":["tutor_vnumber, tutor_name"]})

    form.name.choices = names

    if form.validate_on_submit():
        name = form.name.data
        url = f"insert_session/{name}"
        return redirect(url)
        #redirect to insert_session and pass the name

    return render_template('insert_sessionName.html', form = form)

@app.route('/insert_session/<name>', methods=['GET', 'POST'])
@login_required
def insert_session(name):
    all_time_slots = None
    course_codes = None
    form = SessionForm()

    course_codes =  conn.select({"table":"expertise","data":{"expertise_vnumber":name}, "columns":["expertise_code"]})
    course_codes = [(code[0],code[0]) for code in course_codes]
    form.course_code.choices = course_codes

    all_time_slots = conn.select({"table":"availability","data":{"availability_vnumber":name}, "columns":["availability_day, availability_time"]})
    for time_slot in all_time_slots:
        day = time_slot[0]
        time = time_slot[1]
        form.time_slots.choices.append((f"{time_slot[0]},{time_slot[1]}", f"{time_slot[0]} - {time_slot[1]}"))

    if form.validate_on_submit():
        time_slots = form.time_slots.data
        course_code = form.course_code.data
        for time_slot in time_slots:
            day, time = time_slot.split(',')
            conn.insert({"table":"session","data":{"session_vnumber":name, "session_day":day,"session_time":time, "session_code":course_code}})
    
    return render_template('insert_session.html', form = form)


# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Select Pages ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
# ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ 
@app.route('/select', methods=['GET', 'POST'])
@login_required
def select():
    return render_template('select.html')


@app.route('/select_tutor', methods=['GET', 'POST'])
@login_required
def select_tutor():
    headers = ('Name','V-Number')
    data = conn.select({"table":"tutor","data":{}, "columns":["tutor_name", "tutor_vnumber"]})
    return render_template('select_table.html', headers = headers, data = data)


@app.route('/select_course', methods=['GET', 'POST'])
@login_required
def select_course():
    headers = ('Course ID',)
    data = conn.select({"table":"course","data":{}, "columns":["*"]})
    return render_template('select_table.html', headers = headers, data = data)

@app.route('/select_expertise', methods=['GET', 'POST'])
@login_required
def select_expertise():
    name = None
    names = None
    course_codes = None
    all_course_codes = None
    headers = ("Name", "Course ID")
    form = ExpertiseForm()

    names = conn.select({"table":"tutor","data":{},"columns":["tutor_vnumber, tutor_name"]})
    all_course_codes = conn.select({"table":"course","data":{},"columns":["course_code"]})
    all_course_codes = [(code[0],code[0]) for code in all_course_codes]
    
    form.course_codes.choices = all_course_codes
    form.name.choices = names
    form.course_codes.choices.insert(0,('*','any'))
    form.name.choices.insert(0,('*','any'))

    if form.validate_on_submit():
        course_code = form.course_codes.data[0]
        name = form.name.data

        conditions = {}
        if course_code != '*':
            conditions['expertise_code'] = course_code
        if name != '*':
            conditions["expertise_vnumber"] = name
        data = conn.select({"table":"expertise","data":conditions, "columns":["*"]})
        return render_template('select_table.html', headers = headers, data = data)
            
    
    return render_template('select_expertise.html', form = form)


@app.route('/select_availability', methods=['GET', 'POST'])
@login_required
def select_availability():
    name = None
    day = None
    time = None
    headers = ("Name", "Day", "Time")
    form = AvailabilityForm()

    names = conn.select({"table":"tutor","data":{},"columns":["tutor_vnumber, tutor_name"]})

    form.name.choices = names
    form.days.choices = [('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday'), ('saturday', 'saturday')]
    form.times.choices = [('100', '100'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500'), ('600', '600'), ('700', '700')]
    form.name.choices.insert(0,('*','any'))
    form.days.choices.insert(0,('*','any'))
    form.times.choices.insert(0,('*','any'))

    if form.validate_on_submit():
        day = form.days.data[0]
        time = form.times.data[0]
        name = form.name.data

        conditions = {}
        if day != '*':
            conditions['availability_day'] = day
        if time != '*':
            conditions['availability_time'] = time
        if name != '*':
            conditions["availability_vnumber"] = name

        data = conn.select({"table":"availability","data":conditions, "columns":["*"]})
        return render_template('select_table.html', headers = headers, data = data)
            
    
    return render_template('select_availability.html', form = form)


@app.route('/select_session', methods=['GET', 'POST'])
@login_required
def select_session():
    name = None
    course_code = None
    time = None
    day = None
    headers = ("Name", "Course ID", "Day", "Time")
    form = SelectSessionForm()

    names = conn.select({"table":"tutor","data":{},"columns":["tutor_vnumber, tutor_name"]})
    course_codes =  conn.select({"table":"course","data":{}, "columns":["*"]})
    course_codes = [(code[0],code[0]) for code in course_codes]

    form.name.choices = names
    form.course_code.choices = course_codes
    form.day.choices = [('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday'), ('saturday', 'saturday')]
    form.time.choices = [('100', '100'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500'), ('600', '600'), ('700', '700')]
    form.name.choices.insert(0,('*','any'))
    form.day.choices.insert(0,('*','any'))
    form.time.choices.insert(0,('*','any'))
    form.course_code.choices.insert(0,('*','any'))

    if form.validate_on_submit():
        name = form.name.data
        course_code = form.course_code.data
        day = form.day.data
        time = form.time.data

        conditions = {}
        if name != '*':
            conditions["session_vnumber"] = name
        if course_code != '*':
            conditions["session_code"] = name
        if day != '*':
            conditions['session_day'] = day
        if time != '*':
            conditions['session_time'] = time

        data = conn.select({"table":"session","data":conditions, "columns":["*"]})
        return render_template('select_table.html', headers = headers, data = data)
            
    
    return render_template('select_session.html', form = form)




# |--------------------------------------------------------------------------------------------|
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ Helper Methods and Routes * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |--------------------------------------------------------------------------------------------|

@app.route('/reset')
def reset():
    conn.reset()
    return redirect('/selections')

def getUsers():
    users = {'admin':'123'}
    # users = conn.select({"table":"user","data":{},"columns":["*"]})
    # users = {user[0]:user[1] for user in users}
    return users


