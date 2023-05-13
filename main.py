import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import User
from datetime import datetime
from hashlib import md5

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WaterBallWaterRock'

login_manager = LoginManager()
login_manager.login_view = 'coachlogin'
login_manager.init_app(app)


def avatar(email, size):
  digest = md5(email.lower().encode('utf-8')).hexdigest()
  return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)


def updateAvatar(id):
  conn = get_db_connection()
  user = conn.execute('SELECT * FROM coaches WHERE coach_id = ?',
                      (id, )).fetchone()
  avtr = avatar(user['email'], 200)
  conn.execute('UPDATE coaches SET avatar = ? WHERE coach_id = ?', (
    avtr,
    user['coach_id'],
  ))
  conn.commit()
  conn.close()


def getTSNow():
  return datetime.utcnow()


@login_manager.user_loader
def load_user(user_id):
  conn = get_db_connection()
  conn.execute("UPDATE coaches SET last_accessed = ? WHERE coach_id = ?", (
    getTSNow(),
    user_id,
  ))
  conn.commit()
  user = conn.execute('SELECT * FROM coaches WHERE coach_id = ?',
                      (user_id, )).fetchone()
  if user['avatar'] == '':
    updateAvatar(user_id)
    user = conn.execute('SELECT * FROM coaches WHERE coach_id = ?',
                        (user_id, )).fetchone()
  conn.close()
  if user is None:
    abort(404)
  else:
    return User(user['coach_id'], user['first_name'], user['last_name'],
                user['email'], user['status'], user['password'],
                user['last_accessed'].split()[0], user['access_level'],
                user['offset'], user['avatar'])


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
  user = conn.execute("SELECT * FROM coaches WHERE coach_id = ?",
                      (id, )).fetchone()
  conn.close()
  if user is None:
    abort(404)
  return user


@app.errorhandler(404)
def not_found(e):
  flash(e, 'error')
  return render_template('404.html', title="Error")


@app.route('/')
def index():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  conn.close()

  conn = get_db_connection()
  standings = conn.execute(
    'SELECT teams.team_id AS id, teams.logo AS logo, teams.name AS name, teams.division as division, standings.wins AS wins, standings.ties AS ties, standings.losses AS losses, standings.goals_scored AS scored, standings.goals_against AS against FROM teams INNER JOIN standings ON teams.team_id = standings.team_id WHERE standings.competition_type = "L" ORDER BY(standings.wins) desc'
  ).fetchall()
  conn = get_db_connection()
  schedule = conn.execute(
    'SELECT * FROM schedule where played = "N" LIMIT 8').fetchall()
  conn.close()
  conn = get_db_connection()
  homeschedule = conn.execute(
    'SELECT teams.* FROM schedule INNER JOIN teams ON teams.team_id = schedule.home_id'
  ).fetchall()
  conn.close()
  conn = get_db_connection()
  awayschedule = conn.execute(
    'SELECT teams.* FROM schedule INNER JOIN teams ON teams.team_id = schedule.away_id'
  ).fetchall()
  conn.close()

  return render_template('index.html',
                         title="Home",
                         teams=teams,
                         standings=standings,
                         schedule=schedule,
                         homeschedule=homeschedule,
                         awayschedule=awayschedule)


@app.route('/standings/')
def standings():
  conn = get_db_connection()
  stand = conn.execute("SELECT * FROM teams").fetchall()
  conn.close()
  return render_template('standings.html', title="Standing", stand=stand)


@app.route('/stats/')
def stats():

  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  conn.close()
  conn = get_db_connection()
  player_stats = conn.execute(
    'SELECT p.player_id AS id, p.last_name AS last, p.first_name AS first, p.team_id AS team_id, p.age AS year, ps.position AS position, p.overall AS overall, ps.game_played AS game_played, ps.shots as shots, ps.goals AS goals, ps.shot_percentage AS shot_percentage, ps.assists AS assists, ps.points AS points, ps.steals AS steals FROM players_stats AS ps INNER JOIN players AS p ON p.player_id = ps.player_id'
  ).fetchall()
  conn.close()
  return render_template('statistics.html',
                         title="Statistics",
                         player_stats=player_stats,
                         teams=teams)


def getTeam(team_id):
  conn = get_db_connection()
  team = conn.execute('SELECT * FROM teams WHERE team_id = ?',
                      (team_id, )).fetchone()
  conn.close()
  if team is None:
    abort(404)
  return team


def getPlayer(player_id):
  conn = get_db_connection()
  player = conn.execute(
    'SELECT p.*, t.logo FROM players AS p INNER JOIN teams AS t ON p.team_id = t.team_id WHERE p.player_id = ?',
    (player_id, )).fetchone()
  conn.close()
  if player is None:
    abort(404)
  return player


def getCoach(coach_id):
  conn = get_db_connection()
  coach = conn.execute('SELECT * FROM coaches WHERE coach_id = ?',
                       (coach_id, )).fetchone()
  conn.close()
  if coach is None:
    abort(404)
  return coach


@app.route('/<int:id>/player/delete', methods=('POST', ))
def deletePlayer(id):
  if request.method == 'POST':
    player = getPlayer(id)
    conn = get_db_connection()
    teams = conn.execute(
      'SELECT DISTINCT t.team_id, t.name FROM lineups AS l INNER JOIN teams AS t ON l.team_id == t.team_id WHERE (l.cf_player == ? OR l.cd_player == ? OR l.lw_player == ? OR l.rw_player == ? OR l.ld_player == ? OR l.rd_player == ? OR l.gk_player == ?)',
      (id, id, id, id, id, id, id)).fetchall()
    if len(teams) > 0:
      flash(
        'Please remove them before removing the player out of your roster.',
        'error')
      for team in teams:
        flash(
          f"{player['first_name']} {player['last_name']} is already in {team['name']}'s lineups.",
          'error')
      return redirect(url_for('editPlayer', id=id))
    else:
      conn.execute('DELETE FROM players WHERE player_id = ?', (id, ))
      flash(
        f"{player['first_name']} {player['last_name']} has been removed from your team's roster",
        'correct')
      conn.commit()
      conn.close()
      return redirect(url_for('profile_players'))
    return redirect(url_for('profile_players'))


@app.route('/<int:id>/player/edit', methods=('GET', 'POST'))
@login_required
def editPlayer(id):
  player = getPlayer(id)
  coach = get_db_connection().execute(
    "SELECT coach_id FROM players AS p INNER JOIN teams as t ON p.team_id = t.team_id WHERE p.player_id = ?",
    (id, )).fetchone()
  title = player['first_name'] + " " + player['last_name']
  if request.method == "POST":
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    jersey = request.form['jersey']

    if first_name == "":
      first_name = player['first_name']
    if last_name == "":
      last_name = player['last_name']
    if age == "":
      age = player['age']
    if jersey == "":
      jersey = player['jersey']
    conn = get_db_connection()

    conn.execute(
      'UPDATE players SET first_name = ?, last_name = ?, age = ?, jersey = ? WHERE player_id = ?',
      (first_name, last_name, age, jersey, id))
    conn.commit()
    flash('Player updated successfully!', 'correct')
    return (redirect(url_for('profile_players')))
  return render_template('player_edit.html',
                         title=title,
                         player=player,
                         coach=coach)


@app.route('/<int:id>/team/', methods=('GET', 'POST'))
def displayTeam(id):
  team = getTeam(id)
  coach = getCoach(team['coach_id'])
  return render_template('team.html', title='team', team=team, coach=coach)


@app.route('/<int:id>/player/', methods=('GET', 'POST'))
def displayPlayer(id):
  player = getPlayer(id)
  title = player['first_name'] + " " + player['last_name']
  return render_template('player.html', title=title, player=player)


def checkExisting(email, password, users):
  for user in users:
    if user['email'] == email:
      if user['password'] == password:
        return True, user['coach_id']
      else:
        return False, 0
  return False, 0


def checkValidEmail(email):
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
  if (re.fullmatch(regex, email)):
    return True
  else:
    return False


def checkExistingEmail(email, users):
  for user in users:
    if user['email'] == email:
      return True
  return False


def insertNewUser(first_name, last_name, email, password):
  conn = get_db_connection()
  conn.execute(
    'INSERT INTO coaches (first_name, last_name, email, password) VALUES (? , ?, ?, ?)',
    (
      first_name,
      last_name,
      email,
      password,
    ))
  conn.commit()
  user = conn.execute('SELECT * FROM coaches WHERE email = ?',
                      (email, )).fetchone()
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


@app.route('/coachlogin/', methods=('GET', 'POST'))
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
      # url_avatar = ''
      # twitter_username = request.form['twitter_username']
      if first_name == '':
        first_name = current_user.first_name
      if last_name == '':
        last_name = current_user.last_name
      if email == '':
        email = current_user.email
      else:
        emails = get_db_connection().execute(
          'SELECT email FROM coaches').fetchall()
        for existEmail in emails:
          if existEmail['email'] == email:
            flash('Email is not available', 'error')
            return redirect(url_for('edit_profile'))
      # if twitter_username != '':
      #   url_avatar = "https://unavatar.io/twitter/" + twitter_username

      conn = get_db_connection()
      conn.execute(
        'UPDATE coaches SET first_name = ?, last_name = ?, email = ? WHERE coach_id = ?',
        (first_name, last_name, email, coach_id))
      conn.commit()
      conn.close()
      updateAvatar(coach_id)
      flash('Updated Sucessfully', 'correct')
      return redirect(url_for('profile'))
    return render_template("user/edit_profile.html", title="Edit Profile")
  else:
    return redirect(url_for('profile'))


@app.route('/profile/lineups/', methods=('GET', 'POST'))
@login_required
def profile_lineups():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams WHERE coach_id = ?;',
                       (current_user.id, )).fetchall()
  players = conn.execute('SELECT * FROM players').fetchall()
  schedule = conn.execute(
    'SELECT * FROM schedule where played = "N" LIMIT 8').fetchall()
  conn.close()
  return render_template("user/lineups.html",
                         title="Your lineup",
                         teams=teams,
                         players=players, schedule=schedule)


@app.route('/profile/schedule/', methods=('GET', 'POST'))
@login_required
def profile_schedule():
  return render_template("user/schedule.html", title="Your schedule")


@app.route('/schedule/', methods=('GET', 'POST'))
@login_required
def schedule():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  schedule = conn.execute('SELECT * FROM schedule').fetchall()
  homeschedule = conn.execute(
    'SELECT teams.* FROM schedule INNER JOIN teams ON teams.team_id = schedule.home_id'
  ).fetchall()
  awayschedule = conn.execute(
    'SELECT teams.* FROM schedule INNER JOIN teams ON teams.team_id = schedule.away_id'
  ).fetchall()
  conn.close()

  return render_template("schedule.html",
                         title="This Week's schedule",
                         awayschedule=awayschedule,
                         teams=teams,
                         schedule=schedule,
                         homeschedule=homeschedule)


@app.route('/profile/standings/', methods=('GET', 'POST'))
@login_required
def profile_standings():
  return render_template("user/standings.html", title="Customize Standings")


@app.route('/profile/players/add/', methods=('GET', 'POST'))
@login_required
def add_player():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams WHERE coach_id = ?', (current_user.id,)).fetchall()
  conn.close()
  
  if request.method == 'POST':
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    position = request.form['position']
    jersey = request.form['jersey']
    if first_name + last_name + age + position + jersey == '':
      flash('Please fill out at least one information about the player')
    else:
      if first_name == '':
        first_name = 'First'
      if last_name == '':
        last_name = 'Last'
      if age == '':
        age = 'NA'
      if position == '':
        position = 'TBA'
      if jersey == '':
        jersey = 0
      print('OK')
      team_id = request.form['team_id']
      print(team_id)
      conn = get_db_connection()
      conn.execute('INSERT INTO players(team_id, first_name, last_name, age, position, jersey) VALUES (?, ?, ?, ?, ?,?)', (team_id, first_name, last_name, age, position, jersey))
      conn.commit()
      id = conn.execute('SELECT player_id FROM players ORDER BY player_id DESC LIMIT 1').fetchone()
      conn.close()
      flash('New Player added')
      return redirect(url_for('editPlayer', id=id['player_id']))
  return render_template('user/add_player.html', title="Add Player", teams=teams)


@app.route('/profile/players/', methods=('GET', 'POST'))
@login_required
def profile_players():
  if current_user.is_authenticated:
    conn = get_db_connection()
    players = conn.execute(
      'SELECT p.* FROM players AS p INNER JOIN (teams AS t INNER JOIN coaches as c ON c.coach_id = t.coach_id) ON p.team_id = t.team_id WHERE c.coach_id = ? ORDER BY p.team_id, p.last_name;',
      (current_user.id, )).fetchall()
    teams = conn.execute(
      'SELECT DISTINCT t.* FROM players AS p INNER JOIN (teams AS t INNER JOIN coaches as c ON c.coach_id = t.coach_id) ON p.team_id = t.team_id WHERE c.coach_id = ?',
      (current_user.id, )).fetchall()
    conn.close()
  return render_template("user/players.html",
                         title="Customize Your Players",
                         teams=teams,
                         players=players)


@app.route('/logout/')
@login_required
def logout():
  logout_user()
  return redirect(url_for('coachlogin'))


app.run(host='0.0.0.0', port='3000')
