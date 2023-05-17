import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import User
from datetime import datetime
from hashlib import md5
import random

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
                user['offset'], user['avatar'], user['admin'])

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
  standings = conn.execute('SELECT teams.team_id AS id, teams.logo AS logo, teams.name AS name, teams.division as division, standings.wins AS wins, standings.ties AS ties, standings.losses AS losses, standings.goals_scored AS scored, standings.goals_against AS against FROM teams INNER JOIN standings ON teams.team_id = standings.team_id WHERE standings.competition_type = "L" ORDER BY(standings.wins) desc'
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
  standings = conn.execute(
    'SELECT teams.team_id AS id, teams.logo AS logo, teams.name AS name, teams.division as division, standings.wins AS wins, standings.ties AS ties, standings.losses AS losses, standings.goals_scored AS scored, standings.goals_against AS against FROM teams INNER JOIN standings ON teams.team_id = standings.team_id WHERE standings.competition_type = "L" ORDER BY(standings.wins) desc'
  ).fetchall()
  conn.close()
  return render_template('standings.html',
                         title="Standing",
                         standings=standings)


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
    position = request.form['position']
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
      'UPDATE players SET first_name = ?, last_name = ?, age = ?, jersey = ?, position = ? WHERE player_id = ?',
      (first_name, last_name, age, jersey,position, id))
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
  conn = get_db_connection()
  players = conn.execute(
    'SELECT * FROM players WHERE team_id = ? ORDER BY jersey',
    (id, )).fetchall()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  nextgames = conn.execute(
    'SELECT * FROM schedule WHERE (home_id = ? OR away_id = ?) AND played = "N"',
    (
      id,
      id,
    )).fetchall()
  pastgames = conn.execute(
    'SELECT * FROM schedule WHERE (home_id = ? OR away_id = ?) AND played = "Y"',
    (
      id,
      id,
    )).fetchall()
  print(f'Played {len(nextgames)}')
  return render_template('team.html',
                         title='team',
                         team=team,
                         teams=teams,
                         coach=coach,
                         players=players,
                         pastgames=pastgames,
                         nextgames=nextgames)


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

@app.route('/admin/', methods=('GET', 'POST'))
@login_required
def admin():
  if current_user.admin == 'Y':
    conn = get_db_connection()
    coaches = conn.execute('SELECT * FROM coaches').fetchall()
    players = conn.execute('SELECT * FROM players ORDER BY team_id').fetchall()
    teams = conn.execute('SELECT * FROM teams').fetchall()
    
    if request.method == 'POST':
      print(len(teams))
      boolChange = False
      for team in teams:
        team_id = team['team_id']
        coach_id = team['coach_id']
        request_team_id = f'team{team_id}'
        request_coach_id = int(request.form[request_team_id])
        print(f'{team_id}: {type(coach_id)} -> {type(request_coach_id)}')
        if request_coach_id != coach_id:
          boolChange = True
          old_coach = conn.execute('SELECT first_name, last_name FROM coaches WHERE coach_id = ?',(coach_id,)).fetchone()
          new_coach = conn.execute('SELECT first_name, last_name FROM coaches WHERE coach_id = ?',(request_coach_id,)).fetchone()
          flash(f"Coach of {team['name'].upper()} changed from {old_coach['first_name']} {old_coach['last_name']} -> {new_coach['first_name']} {new_coach['last_name']}", 'correct')
          conn.execute('UPDATE teams SET coach_id = ? WHERE team_id = ?',(request_coach_id, team_id))
          conn.commit()
      if boolChange == False:
        flash('Nothing changed')
      return redirect(url_for('admin'))
      print('TRUE SAVE')
    conn.close()
    return render_template('admin.html', title="Admin", coaches=coaches, players=players, teams=teams)
  else:
    return redirect(url_for('index'))

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


@app.route('/profile/edit-profile/delete/<int:id>/', methods=('GET', 'POST'))
@login_required
def delete_profile(id):
  coach = getCoach(id)
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams WHERE coach_id = ?',
                       (coach['coach_id'], )).fetchall()
  if len(teams) <= 0:
    if int(current_user.id) == int(id):
      logout_user()
    conn.execute('DELETE FROM coaches WHERE coach_id = ?',
                 (coach['coach_id'], ))
    conn.commit()
    if int(current_user.id) == 1:
      flash('User deleted', 'correct')
      return redirect(url_for('admin'))
    else: 
      flash('Your Profile is deleted', 'correct')
      return redirect(url_for('coachlogin'))
  else:
    if int(current_user.id != 1):
      flash('You have to remove your team from your profile', 'error')
      return redirect(url_for('edit_profile'))
    else:
      flash('Remove the team associate with that user before delete', 'error')
      return redirect(url_for('admin'))


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
    
@app.route('/profile/lineups/reset/<int:team_id>/<int:match_number>/', methods=('GET', 'POST'))
@login_required
def reset_lineups(team_id, match_number):
  conn = get_db_connection()
  conn.execute('UPDATE lineups SET cf_player = 0, cd_player = 0, lw_player = 0, rw_player = 0, ld_player = 0, rd_player = 0, gk_player = 0 WHERE team_id = ? AND match_number = ?', (team_id, match_number))
  conn.commit()
  conn.close()
  return redirect(url_for('profile_lineups'))

@app.route('/profile/lineups/', methods=('GET', 'POST'))
@login_required
def profile_lineups():

  conn = get_db_connection()
  players = conn.execute(
      'SELECT p.* FROM players AS p INNER JOIN (teams AS t INNER JOIN coaches as c ON c.coach_id = t.coach_id) ON p.team_id = t.team_id WHERE c.coach_id = ?',
      (current_user.id, )).fetchall()
  teams = conn.execute(
      'SELECT DISTINCT t.* FROM players AS p INNER JOIN (teams AS t INNER JOIN coaches as c ON c.coach_id = t.coach_id) ON p.team_id = t.team_id WHERE c.coach_id = ?',
      (current_user.id, )).fetchall()
  schedule = conn.execute('SELECT * FROM schedule where played = "N" LIMIT 8').fetchall()
  lineups = conn.execute('SELECT * FROM lineups').fetchall()
  if request.method == 'POST':
    boolCheck = False
    for team in teams:
      print(team['name'])
      for player in players:
        if player['team_id'] == team['team_id']:
          for sched in schedule:
            if sched['home_id'] == team['team_id'] or sched['away_id'] == team['team_id']:
              player_id = player['player_id']
              match_number = sched['match_number']
              match_request_id = f"{match_number}:{player_id}"
              cf_player = conn.execute('SELECT cf_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['cf_player']
              cd_player = conn.execute('SELECT cd_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['cd_player']
              lw_player = conn.execute('SELECT lw_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['lw_player']
              rw_player = conn.execute('SELECT rw_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['rw_player']
              ld_player = conn.execute('SELECT ld_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['ld_player']
              rd_player = conn.execute('SELECT rd_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['rd_player']
              gk_player = conn.execute('SELECT gk_player FROM lineups WHERE team_id = ? AND match_number = ?',(team['team_id'], sched['match_number'])).fetchone()['gk_player']
              # this get player position
              position_request = request.form[match_request_id]

              if position_request != 'B' and boolCheck is False:
                boolCheck = True
                
              # update that player position for that match number
              # cf_player INTEGER NOT NULL,
              # cd_player INTEGER NOT NULL,
              # lw_player INTEGER NOT NULL,
              # rw_player INTEGER NOT NULL,
              # ld_player INTEGER NOT NULL,
              # rd_player INTEGER NOT NULL,
              # gk_player INTEGER NOT NULL
              conn = get_db_connection()
              if position_request != 'B':
                match position_request:
                  case 'CF':
                    conn.execute('UPDATE lineups SET cf_player = ? WHERE match_number = ?',(player_id,match_number))
                    flash(f"Center -> {player['first_name']} {player['last_name']}", 'correct')
                  case 'CD':
                    conn.execute('UPDATE lineups SET cd_player = ? WHERE team_id = ? AND match_number = ?',(player_id,team['team_id'], match_number))
                    flash(f"Center Defender -> {player['first_name']} {player['last_name']}", 'correct')
                  case 'LW':
                    conn.execute('UPDATE lineups SET lw_player = ? WHERE team_id = ? AND match_number = ?',(player_id,team['team_id'],match_number))
                    flash(f"Left Wing -> {player['first_name']} {player['last_name']}", 'correct')
                  case 'RW':
                    conn.execute('UPDATE lineups SET rw_player = ? WHERE team_id = ? AND match_number = ?',(player_id,team['team_id'],match_number))
                    flash(f"Right Wing -> {player['first_name']} {player['last_name']}", 'correct')
                  case 'LD':
                    conn.execute('UPDATE lineups SET ld_player = ? WHERE team_id = ? AND match_number = ?',(player_id,team['team_id'],match_number))
                    flash(f"Left Driver -> {player['first_name']} {player['last_name']}", 'correct')
                  case 'RD':
                    conn.execute('UPDATE lineups SET rd_player = ? WHERE team_id = ? AND match_number = ?',(player_id,team['team_id'],match_number))
                    flash(f"Right Driver -> {player['first_name']} {player['last_name']}", 'correct')
                  case 'GK':
                    conn.execute('UPDATE lineups SET gk_player = ? WHERE team_id = ? AND match_number = ?',(player_id,team['team_id'],match_number))
                    flash(f"Goal Keeping -> {player['first_name']} {player['last_name']}", 'correct')
                conn.commit()
              else:
                match int(player['player_id']):
                  case [cf_player]:
                    conn.execute('UPDATE lineups SET cf_player = ? WHERE match_number',(0,match_number))
                  case [cd_player]:
                    conn.execute('UPDATE lineups SET cd_player = ? WHERE match_number',(0,match_number))
                  case [lw_player]:
                    conn.execute('UPDATE lineups SET lw_player = ? WHERE match_number',(0,match_number))
                  case [rw_player]:
                    conn.execute('UPDATE lineups SET rw_player = ? WHERE match_number',(0,match_number))
                  case [ld_player]:
                    conn.execute('UPDATE lineups SET ld_player = ? WHERE match_number',(0,match_number))
                  case [rd_player]:
                    conn.execute('UPDATE lineups SET rd_player = ? WHERE match_number',(0,match_number))
                  case [gk_player]:
                    conn.execute('UPDATE lineups SET gk_player = ? WHERE match_number',(0,match_number))
                conn.commit()
              # your code  
              # print(f"- {player['first_name']} - match {match_number} - request id {match_request_id} - position {position_request}")
    print('Submite')
    if boolCheck is True:
      flash('Updated!', 'correct')
    else:
      flash('Nothing Changed', 'correct')
    return redirect(url_for('profile_lineups'))
  return render_template("user/lineups.html",
                         title="Your lineup",
                         teams=teams,
                         players=players,
                         schedule=schedule,
                          lineups = lineups)


@app.route('/profile/schedule/', methods=('GET', 'POST'))
@login_required
def profile_schedule():
  return render_template("user/schedule.html", title="Your schedule")


@app.route('/schedule/', methods=('GET', 'POST'))
def schedule():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  schedule = conn.execute('SELECT * FROM schedule').fetchall()
  matchnumber = conn.execute(
    "SELECT COUNT(DISTINCT match_number) AS count FROM schedule").fetchone(
    )['count']
  conn.close()

  return render_template("schedule.html",
                         title="This Week's schedule",
                         teams=teams,
                         schedule=schedule,
                         matchnumber=matchnumber)

@app.route('/<int:id>/boxscore/', methods=('GET', 'POST'))
def schedule_boxscore(id):
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams').fetchall()
  schedule = conn.execute('SELECT * FROM schedule WHERE schedule_id = ?', (id,)).fetchone()
  print(schedule)
  matchnumber = conn.execute(
    "SELECT COUNT(DISTINCT match_number) AS count FROM schedule").fetchone(
    )['count']
  player_stats = conn.execute(
    'SELECT p.player_id AS id, p.last_name AS last, p.first_name AS first, p.team_id AS team_id, p.age AS year, ps.position AS position, p.overall AS overall, ps.game_played AS game_played, ps.shots as shots, ps.goals AS goals, ps.shot_percentage AS shot_percentage, ps.assists AS assists, ps.points AS points, ps.steals AS steals, ps.saves AS saves, ps.save_percentage AS save_percentage, ps.match_number AS match_number FROM players_stats AS ps INNER JOIN players AS p ON p.player_id = ps.player_id'
  ).fetchall()
  conn.close()

  return render_template("schedule_boxscore.html",
                         title="This Week's schedule",
                         teams=teams,
                         schedule=schedule,
                         matchnumber=matchnumber, player_stats=player_stats)


@app.route('/profile/standings/', methods=('GET', 'POST'))
@login_required
def profile_standings():
  return render_template("user/standings.html", title="Customize Standings")


@app.route('/profile/players/add/', methods=('GET', 'POST'))
@login_required
def add_player():
  conn = get_db_connection()
  teams = conn.execute('SELECT * FROM teams WHERE coach_id = ?',
                       (current_user.id, )).fetchall()
  conn.close()
  if len(teams) <= 0:
    return redirect(url_for('profile_players'))
  else:
    if request.method == 'POST':
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      age = request.form['age']
      jersey = request.form['jersey']
      if first_name + last_name + age + jersey == '':
        flash('Please fill out at least one information about the player')
      else:
        if first_name == '':
          first_name = 'First'
        if last_name == '':
          last_name = 'Last'
        if age == '':
          age = 'NA'
        if jersey == '':
          jersey = 0
        else:
          jersey = int(jersey)
        team_id = request.form['team_id']
        conn = get_db_connection()
        players = conn.execute('SELECT jersey FROM players WHERE team_id = ?',(team_id,)).fetchall()
        jersey_list = []
        for player in players:
          jersey_list.append(player['jersey'])
        strjl = str(jersey_list)[1:-1]
        print(strjl)
        if jersey in jersey_list:
          flash(f'Jersey number {jersey} is already existed in the team', 'error')
          flash(f'Taken jersey numbers {strjl}')
          return redirect(url_for('add_player'))
        position = request.form['position']
        swimming = 0
        ballhandling = 0
        passing = 0
        shooting = 0
        defense = 0
        aggression = 0
        goalkeeping = 0
        overall = 0
        if position == "Attacker":
          swimming = random.randrange(60, 100)
          ballhandling = random.randrange(60, 100)
          passing = random.randrange(60, 100)
          shooting = random.randrange(60, 100)
          defense = random.randrange(60, 100)
          aggression = random.randrange(40, 100)
          goalkeeping = 0
          overall = (swimming * 1.3 + ballhandling * 1.1 +
                     passing * 1.25 + shooting*1.15 + defense*1.2)//6
        elif position == "CD":
          swimming = random.randrange(60, 100)
          ballhandling = random.randrange(60, 100)
          passing = random.randrange(60, 100)
          shooting = random.randrange(60, 100)
          defense = random.randrange(75, 100)
          aggression = random.randrange(40, 100)
          goalkeeping = 0
          overall = (swimming + ballhandling +
                     passing + shooting + defense * 2)//6
        elif position == "CF":
          swimming = random.randrange(45, 100)
          ballhandling = random.randrange(60, 100)
          passing = random.randrange(60, 100)
          shooting = random.randrange(80, 100)
          defense = random.randrange(40, 100)
          aggression = random.randrange(20, 100)
          goalkeeping = 0
          overall = (swimming + ballhandling * 1.25 +
                     passing + shooting * 2 + defense * .75)//6
        else:
          swimming = 0
          ballhandling = 0
          passing = random.randrange(60, 100)
          shooting = 0
          defense = 0
          aggression = random.randrange(1, 100)
          goalkeeping = random.randrange(70, 100)
          overall = (passing + goalkeeping) // 2
        conn = get_db_connection()
        conn.execute(
          'INSERT INTO players(team_id, first_name, last_name, age, position, jersey, swimming, ballhandling, passing, shooting, defense, aggression, goalkeeping, overall) VALUES (?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?)',
          (team_id, first_name, last_name, age, position, jersey,swimming, ballhandling, passing, shooting, defense, aggression, goalkeeping, overall))
        conn.commit()
        id = conn.execute(
          'SELECT player_id FROM players ORDER BY player_id DESC LIMIT 1'
        ).fetchone()
        conn.close()
        flash('New Player added')
        return redirect(url_for('editPlayer', id=id['player_id']))
  return render_template('user/add_player.html',
                         title="Add Player",
                         teams=teams)


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


# if position == "Attacker":
#             swimming = random.randrange(60, 100)
#             ballhandling = random.randrange(60, 100)
#             passing = random.randrange(60, 100)
#             shooting = random.randrange(60, 100)
#             defense = random.randrange(60, 100)
#             aggression = random.randrange(40, 100)
#             goalkeeping = 0
#             overall = (swimming * 1.3 + ballhandling * 1.1 +
#                        passing * 1.25 + shooting*1.15 + defense*1.2)//6
#         elif position == "CD":
#             swimming = random.randrange(60, 100)
#             ballhandling = random.randrange(60, 100)
#             passing = random.randrange(60, 100)
#             shooting = random.randrange(60, 100)
#             defense = random.randrange(75, 100)
#             aggression = random.randrange(40, 100)
#             goalkeeping = 0
#             overall = (swimming + ballhandling +
#                        passing + shooting + defense * 2)//6
#         elif position == "CF":
#             swimming = random.randrange(45, 100)
#             ballhandling = random.randrange(60, 100)
#             passing = random.randrange(60, 100)
#             shooting = random.randrange(80, 100)
#             defense = random.randrange(40, 100)
#             aggression = random.randrange(20, 100)
#             goalkeeping = 0
#             overall = (swimming + ballhandling * 1.25 +
#                        passing + shooting * 2 + defense * .75)//6
#         else:
#             swimming = 0
#             ballhandling = 0
#             passing = random.randrange(60, 100)
#             shooting = 0
#             defense = 0
#             aggression = random.randrange(1, 100)
#             goalkeeping = random.randrange(70, 100)
#             overall = (passing + goalkeeping) // 2

#         sql = "UPDATE players SET jersey = ?, first_name = ?, last_name = ?, age = ?, swimming = ?, ballhandling = ?, passing = ?, shooting = ?, defense = ?, aggression = ?, goalkeeping = ?, fit = ?, overall = ? WHERE player_id = ? AND team_id = ?"
#         val = (jersey, firstname, lastname, year, swimming, ballhandling, passing,
#                shooting, defense, aggression, goalkeeping, 0, overall, intPLAYERID, intTeamId)
#         mycursor = connection.cursor()
#         connection.execute(sql, val)
#         print(jersey)
#         connection.commit()