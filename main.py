import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import User
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WaterBallWaterRock'

login_manager = LoginManager()
login_manager.login_view = 'coachlogin'
login_manager.init_app(app)

def getTSNow():
  return datetime.utcnow()
  
@login_manager.user_loader
def load_user(user_id):
  conn = get_db_connection()
  conn.execute("UPDATE coaches SET last_accessed = ? WHERE coach_id = ?", (getTSNow(),user_id,))
  conn.commit()
  user = conn.execute('SELECT * FROM coaches WHERE coach_id = ?', (user_id,)).fetchone()
  conn.close()
  if user is None:
    abort(404)
  else:
    return User(user['coach_id'],user['first_name'],user['last_name'],user['email'], user['status'], user['password'], user['last_accessed'], user['access_level'], user['offset'])

def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

def retrieveALLUsers():
  conn = get_db_connection()
  cursor = conn.execute("SELECT * FROM coaches")
  users = cursor.fetchall()
  conn.close()
  return users
  
def retrieveUser(id):
  conn = get_db_connection()
  user = conn.execute("SELECT * FROM coaches WHERE coach_id = ?",(id,)).fetchone()
  conn.close()
  if user is None:
      abort(404)
  return user

@app.route('/')
def index():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  conn.close()

  conn = get_db_connection()
  standings = conn.execute(
    'SELECT teams.team_id AS id, teams.logo AS logo, teams.name AS name, teams.division as division, standings.wins AS wins, standings.losses AS losses FROM teams INNER JOIN standings ON teams.team_id = standings.team_id ORDER BY(standings.wins) desc').fetchall()
  conn.close()
  return render_template('index.html',title="Home",teams=teams, standings=standings)

@app.route('/standings/')
def standings():
  conn = get_db_connection()
  stand = conn.execute("SELECT * FROM teams").fetchall()
  conn.close()
  return render_template('standings.html', title="Standing", stand=stand)
@app.route('/stats/')
def stats():
  return render_template('statistics.html', title="Statistics")

def getTeam(team_id):
    conn = get_db_connection()
    team = conn.execute('SELECT * FROM teams WHERE team_id = ?',(team_id,)).fetchone()
    conn.close()
    if team is None:
        abort(404)
    return team
  
def getCoach(coach_id):
  conn = get_db_connection()
  coach = conn.execute('SELECT * FROM coaches WHERE coach_id = ?',(coach_id,)).fetchone()
  conn.close()
  if coach is None:
    abort(404)
  return coach

@app.route('/<int:id>/team/', methods=('GET', 'POST'))
def displayTeam(id):
  team = getTeam(id)
  coach = getCoach(team['coach_id'])
  return render_template('team.html', title='team', team=team, coach=coach)
  

def checkExisting(email,password, users):
  for user in users:
    if user['email'] == email:
      if user['password'] == password:
        return True, user['coach_id']
      else:
        return False, 0
  return False, 0
  
def checkValidEmail(email):
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
  if(re.fullmatch(regex, email)):
    return True
  else:
    return False
    
def checkExistingEmail(email,users):  
  for user in users:
    if user['email'] == email:
      return True
  return False
  
def insertNewUser(first_name, last_name, email, password):
  conn = get_db_connection()
  conn.execute('INSERT INTO coaches (first_name, last_name, email, password) VALUES (? , ?, ?, ?)', (first_name, last_name, email, password,))
  conn.commit()
  user = conn.execute('SELECT * FROM coaches WHERE email = ?', (email,)).fetchone()
  conn.close()
  return user['coach_id']
  

@app.route('/signup/', methods=('GET', 'POST'))
def signup():
  if current_user.is_authenticated:
     return redirect(url_for('profile'))
  try:
    if request.method == 'POST':
      users = retrieveALLUsers()
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      email = request.form['email']
      password = request.form['password']
      retype_password = request.form['retype_password']
      # flash(f'{first_name} {last_name} {email} {password} {retype_password}')
      if checkValidEmail(email) is False and len(email) > 40:
        flash('Invalid Email', 'error')
      elif checkExistingEmail(email, users):
        flash('Your email is taken', 'error')
      elif password != retype_password:
        flash('Retype password is not the same', 'error')
      elif len(first_name) > 20 and len(last_name) > 20:
        flash('First or Last name is longer than 20 characters')
      else:
        id = insertNewUser(first_name, last_name, email, password)
        # flash(id)
        new_user = load_user(id)
        login_user(new_user, remember=True)
        flash('Account created', 'correct')
        return redirect(url_for('profile'))
    return render_template('signup.html', title="Signup")
  except Exception as e:
    flash(e)
    return render_template('signup.html', title="Signup")

@app.route('/coachlogin/', methods=('GET','POST'))
def coachlogin():
  if current_user.is_authenticated:
     return redirect(url_for('profile'))
  users = retrieveALLUsers()
  try:
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      # users = retrieveALLUsers()
      checkBool, id = checkExisting(email, password, users)
      if (checkBool is False and id == 0):
      # if True:
        flash('Wrong password or username', 'error')
      else:
        user = load_user(id)
        login_user(user, remember=True)
        return redirect(url_for('profile'))
        
    return render_template('coachlogin.html', title="Login")
  except Exception as e:
    flash(e, 'error')
    return render_template('coachlogin.html', title="Login")

@app.route('/profile/dashboard/', methods=('GET', 'POST'))
@login_required
def profile():
  if request.method == 'POST':
    return redirect(url_for('edit_profile'))
  return render_template("user/dashboard.html", title="Welcome")
  
@app.route('/profile/edit-profile/', methods=('GET', 'POST'))
@login_required
def edit_profile():
  if current_user.is_authenticated:
    if request.method == 'POST':
      coach_id = current_user.id
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      email = request.form['email']
      if first_name == '':
        first_name = current_user.first_name
      if last_name == '':
        last_name = current_user.last_name
      if email == '':
        email = current_user.email
      conn = get_db_connection()
      conn.execute('UPDATE coaches SET first_name = ?, last_name = ?, email = ? WHERE coach_id = ?', (first_name, last_name, email, coach_id))
      conn.commit()
      conn.close()
      flash('Updated Sucessfully', 'correct')
      return redirect(url_for('profile'))
    return render_template("user/edit_profile.html", title="Edit Profile")
  else:
    return redirect(url_for('profile'))
  
@app.route('/profile/lineups/', methods=('GET', 'POST'))
@login_required
def profile_lineups():
  if request.method == 'POST':
    return redirect(url_for('edit_profile'))
  return render_template("user/lineups.html", title="Your lineup")
  
@app.route('/profile/schedule/', methods=('GET', 'POST'))
@login_required
def profile_schedule():
  if request.method == 'POST':
    return redirect(url_for('edit_profile'))
  return render_template("user/schedule.html", title="Your schedule")
  
@app.route('/profile/standings/', methods=('GET', 'POST'))
@login_required
def profile_standings():
  if request.method == 'POST':
    return redirect(url_for('edit_profile'))
  return render_template("user/standings.html", title="Customize Standings")

@app.route('/profile/players/', methods=('GET', 'POST'))
@login_required
def profile_players():
  if request.method == 'POST':
    return redirect(url_for('edit_profile'))
  if current_user.is_authenticated:
    conn = get_db_connection()
    players = conn.execute('SELECT p.* FROM players AS p INNER JOIN (teams AS t INNER JOIN coaches as c ON c.coach_id = t.coach_id) ON p.team_id = t.team_id WHERE c.coach_id = ? ORDER BY p.team_id, p.last_name;',(current_user.id,)).fetchall()
    teams = conn.execute('SELECT DISTINCT t.* FROM players AS p INNER JOIN (teams AS t INNER JOIN coaches as c ON c.coach_id = t.coach_id) ON p.team_id = t.team_id WHERE c.coach_id = ?', (current_user.id,)).fetchall()
    conn.close()
  return render_template("user/players.html", title="Customize Your Players", teams=teams, players=players)

@app.route('/logout/')
@login_required
def logout():
  logout_user()
  return redirect(url_for('coachlogin'))

app.run(host='0.0.0.0', port='3000')
