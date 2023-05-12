import sqlite3
import random
connection = sqlite3.connect('database.db')

with open('schema1.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()


class Players():
    TEAM_NUM = 8
    """ generated source for class Players """
    length = 0
    intPlayerId = 0
    player_arr = []
    # This is the player_id in the database.
    intTeamId = 0

    # This is the team_id in the database.
    strName = ""

    # This is the name in the database.
    intAge = 0

    # This is the age in the database.
    strAge = ""

    # This is the skill level for the player at their normal position.
    first = ""
    last = ""
    position = str()
    jersey = 0
    age = 0
    swimming = 0
    ballhandling = 0
    passinging = 0
    shooting = 0
    defense = 0
    goalkeeping = 0
    fit = 0
    aggression = 0
    overall = 0
    strRosterPos = ""
    strMatchPos = ""
    strStatus = "s"

    # This is the stats for the player at their normal position.
    games_played = 0
    shots = 0
    goals = 0
    shot_percentage = 0.00
    assists = 0
    points = 0
    steals = 0
    goals_allowed = 0
    saves = 0
    shots_allowed = 0
    save_percentage = 0.00
    match_rating = 0.00

    transition_speed = 0.00
    transition_distance = 23.9

    def __init__(self, intTeamId, intPLAYERID):
        """ generated source for method __init__ """
        self.intPlayerId = intPLAYERID
        self.setSkills(intTeamId, intPLAYERID)
        # createStats(intTeamId, intPLAYERID, jersey)

    def createStats(self, intTeamId, intPLAYERID, jersey):
        sql = "SELECT position FROM players WHERE player_id = ? AND team_id = ?"
        val = (intPLAYERID, intTeamId)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        position = mycursor.fetchone()[0]
        print(position)

        sql = "SELECT first_name FROM first_name ORDER BY RAND() LIMIT 1"
        mycursor = connection.cursor()
        mycursor.execute(sql)
        firstname = mycursor.fetchone()[0]
        print(firstname)

        sql = "SELECT last_name FROM last_name ORDER BY RAND() LIMIT 1"
        mycursor = connection.cursor()
        mycursor.execute(sql)
        lastname = mycursor.fetchone()[0]
        print(lastname)

        age = random.randrange(1, 5)
        year = ""
        if age == 1:
            year = "Fr"
        elif age == 2:
            year = "So"
        elif age == 3:
            year = "Jr"
        else:
            year = "Sr"
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

        sql = "UPDATE players SET jersey = ?, first_name = ?, last_name = ?, age = ?, swimming = ?, ballhandling = ?, passing = ?, shooting = ?, defense = ?, aggression = ?, goalkeeping = ?, fit = ?, overall = ? WHERE player_id = ? AND team_id = ?"
        val = (jersey, firstname, lastname, year, swimming, ballhandling, passing,
               shooting, defense, aggression, goalkeeping, 0, overall, intPLAYERID, intTeamId)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        print(jersey)
        connection.commit()

    def setSkills(self, intTeamId, intPLAYERID):
        sql = "SELECT first_name, last_name, age, position, jersey, swimming, ballhandling, passing, shooting, defense, goalkeeping, fit, aggression, overall FROM players WHERE player_id = ? AND team_id = ?;"
        val = (intPLAYERID, intTeamId)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        nextval = mycursor.fetchone()
        # for x in nextval:
        #     print(x)
        self.first = nextval[0]
        self.player_arr.append(nextval[0])
        self.last = nextval[1]
        self.age = nextval[2]
        self.position = nextval[3]
        self.jersey = nextval[4]
        self.swimming = nextval[5]
        self.ballhandling = nextval[6]
        self.passinging = nextval[7]
        self.shooting = nextval[8]
        self.defense = nextval[9]
        self.goalkeeping = nextval[10]
        self.fit = nextval[11]
        self.aggression = nextval[12]
        self.overall = nextval[13]

        self.transition_speed = (self.swimming/99) * 1.6

        return nextval
    
    def setStats(self, intTeamId, opp_team_id, intPLAYERID, match_number):
        if self.shots > 0:
            self.shot_percentage = self.goals / self.shots
        if self.goals_allowed > 0:
            self.save_percentage = self.saves/self.shots_allowed
        self.points = self.goals + self.assists
        self.games_played +=1
        sql = "INSERT INTO players_stats(season, player_id, age, team_id, opp_team_id, match_number, position, game_played, shots, goals, shot_percentage, assists, points, steals, goals_allowed, saves, save_percentage, match_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (1, self.intPlayerId, self.age, intTeamId, opp_team_id, match_number, self.position, self.games_played, self.shots, self.goals, self.shot_percentage, self.assists, self.points, self.steals, self.goals_allowed, self.saves, self.save_percentage, self.match_rating)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        nextval = mycursor.fetchone()

        self.games_played = 0
        self.shots = 0
        self.goals = 0
        self.shot_percentage = 0.00
        self.assists = 0
        self.points = 0
        self.steals = 0
        self.goals_allowed = 0
        self.saves = 0
        self.save_percentage = 0.00
        self.match_rating = 0.00
        connection.commit()
    def __str__(self):
        """ generated source for method toString """
        return self.player_arr
    # sql = "SELECT count(*) FROM players"
    # mycursor = connection.cursor()
    # mycursor.execute(sql)
    # myresult = mycursor.fetchone()[0]
    # print(myresult)
    # for x in range(1, 15):
    #     count = 0
    #     for y in range(1, 9):
    #         __init__(y, x*8 - (8-y), x)
    #         print(y, x*8 - (8-y), x)


class lineup:
    TEAM_NUM = 8
    lineup_id = 0
    team_id = 0
    lineup_arr = []
    cf_player = Players(1, 1)
    cd_player = Players(1, 1)
    lw_player = Players(1, 1)
    rw_player = Players(1, 1)
    ld_player = Players(1, 1)
    rd_player = Players(1, 1)
    gk_player = Players(1, 1)

    def __init__(self, intTeamId, MatchNumber):
        self.getLineup(intTeamId, MatchNumber)

    def getLineup(self, intTeamId, MatchNumber):
        sql = "SELECT lineup_id, cf_player, cd_player, lw_player, rw_player, ld_player, rd_player, gk_player FROM lineups WHERE match_number = ? AND team_id = ?;"
        val = (MatchNumber, intTeamId)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        # print(f"{mycursor.fetchone()[7]}")

        nextval = mycursor.fetchone()
        for x in nextval:
            print(x)
        print(nextval[1])
        self.cf_player = Players(intTeamId, nextval[1])
        self.cd_player = Players(intTeamId, nextval[2])
        self.lw_player = Players(intTeamId, nextval[3])
        self.rw_player = Players(intTeamId, nextval[4])
        self.ld_player = Players(intTeamId, nextval[5])
        self.rd_player = Players(intTeamId, nextval[6])
        self.gk_player = Players(intTeamId, nextval[7])
        lineup_arr = [self.cf_player, self.cd_player, self.lw_player,
                      self.rw_player, self.ld_player, self.rd_player, self.gk_player]
        return lineup_arr
        # for i in range(1,8):
        #     print(Players(intTeamId, nextval[i]).first)


lineup1 = lineup(1, 1)


class Teams(object):
    team_id = 0
    name = ""
    city = ""
    nickname = ""
    coach_id = 0
    abb = ""
    short_name = ""
    division = ""
    overall = 0
    aggression = 0
    team_lineup = []
    teamOrder = 0

    goals = 0
    cf_player = Players(1, 1)
    cd_player = Players(1, 1)
    lw_player = Players(1, 1)
    rw_player = Players(1, 1)
    ld_player = Players(1, 1)
    rd_player = Players(1, 1)
    gk_player = Players(1, 1)

    def __init__(self, intTeamId):
        sql = "SELECT AVG(overall) FROM players WHERE team_id = ? and overall > ?"
        val = (intTeamId, 0)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        self.overall = mycursor.fetchone()[0]
        self.team_id = intTeamId
        sql = "SELECT AVG(aggression) FROM players WHERE team_id = ? and aggression > ?"
        val = (intTeamId, 0)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        self.aggression = mycursor.fetchone()[0]

        print(self.overall)
        sql = "UPDATE teams SET overall = ?, aggression = ? WHERE team_id = ?"
        val = (self.overall, self.aggression, intTeamId)
        mycursor = connection.cursor()
        print(self.overall)
        mycursor.execute(sql, val)
        connection.commit()
        self.setTeam(intTeamId)

    def setTeam(self, intTeamId):
        sql = "SELECT name, city, nickname, coach_id, abb, short_name, division FROM teams WHERE team_id = ? and overall > ?"
        val = (intTeamId, 0)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        all = mycursor.fetchone()
        self.name = all[0]
        self.city = all[1]
        self.nickname = all[2]
        self.coach_id = all[3]
        self.abb = all[4]
        self.short_name = all[5]
        self.division = all[6]

    def lineup(self, team1, match_number):
        self.team_lineup = lineup(
            team1, match_number).getLineup(team1, match_number)

    def getLineup(self, intTeamId, MatchNumber):
        sql = "SELECT lineup_id, cf_player, cd_player, lw_player, rw_player, ld_player, rd_player, gk_player FROM lineups WHERE match_number = ? AND team_id = ?;"
        val = (MatchNumber, intTeamId)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        # print(f"{mycursor.fetchone()[7]}")

        nextval = mycursor.fetchone()
        for x in nextval:
            print(x)
        print(nextval[1])
        self.cf_player = Players(intTeamId, nextval[1])
        self.cd_player = Players(intTeamId, nextval[2])
        self.lw_player = Players(intTeamId, nextval[3])
        self.rw_player = Players(intTeamId, nextval[4])
        self.ld_player = Players(intTeamId, nextval[5])
        self.rd_player = Players(intTeamId, nextval[6])
        self.gk_player = Players(intTeamId, nextval[7])
        lineup_arr = [self.cf_player, self.cd_player, self.lw_player,
                      self.rw_player, self.ld_player, self.rd_player, self.gk_player]
        return lineup_arr

    def swim(self):
        if (self.cf_player.transition_distance >= 0):
            self.cf_player.transition_distance -= self.cf_player.transition_speed
        if (self.cd_player.transition_distance >= 0):
            self.cd_player.transition_distance -= self.cd_player.transition_speed
        if (self.lw_player.transition_distance >= 0):
            self.lw_player.transition_distance -= self.lw_player.transition_speed
        if (self.rw_player.transition_distance >= 0):
            self.rw_player.transition_distance -= self.rw_player.transition_speed
        if (self.ld_player.transition_distance >= 0):
            self.ld_player.transition_distance -= self.ld_player.transition_speed
        if (self.rd_player.transition_distance >= 0):
            self.rd_player.transition_distance -= self.rd_player.transition_speed

    def newTransition(self):
        self.cf_player.transition_distance = 23.9 - \
            (23.9 - self.cf_player.transition_distance)
        self.cd_player.transition_distance = 23.9 - \
            (23.9 - self.cd_player.transition_distance)
        self.lw_player.transition_distance = 23.9 - \
            (23.9 - self.lw_player.transition_distance)
        self.rw_player.transition_distance = 23.9 - \
            (23.9 - self.rw_player.transition_distance)
        self.ld_player.transition_distance = 23.9 - \
            (23.9 - self.ld_player.transition_distance)
        self.rd_player.transition_distance = 23.9 - \
            (23.9 - self.rd_player.transition_distance)


class Match:
    team1Lineup = lineup(1, 1)
    team2Lineup = lineup(2, 1)
    team1 = Teams(1)
    team2 = Teams(2)
    team1_cf = Players(1, 1)
    team1_cd = Players(1, 1)
    team1_rw = Players(1, 1)
    team1_lw = Players(1, 1)
    team1_ld = Players(1, 1)
    team1_rd = Players(1, 1)
    team1_gk = Players(1, 1)

    team2_cf = Players(1, 1)
    team2_cd = Players(1, 1)
    team2_rw = Players(1, 1)
    team2_lw = Players(1, 1)
    team2_ld = Players(1, 1)
    team2_rd = Players(1, 1)
    team2_gk = Players(1, 1)

    shot_clock = 40
    ball = Players(1, 1)
    lost_postion = False
    previous_pass = Players(1, 1)

    def __init__(self, home_team, away_team, match_number):
        self.team1 = home_team
        self.team2 = away_team
        self.team1Lineup = home_team.getLineup(home_team.team_id, match_number)
        self.team2Lineup = away_team.getLineup(away_team.team_id, match_number)
        self.quarter = 1
        self.scoreboard = {home_team.abb: 0, away_team.abb: 0}
        print(self.scoreboard)
        self.current_possession = None
        self.time_remaining = 480  # in seconds
        print('me')

        self.play()
        self.updateSchedule(home_team, away_team, match_number)
        self.updateStandings(home_team, away_team, match_number)
        self.updateStats(home_team, away_team, match_number)

    def passto(self, off_team, deff_team):
        p1 = random.randrange(1, 4)
        if off_team.gk_player == self.ball:
            if p1 == 1:
                self.ball = off_team.cd_player
                self.previous_pass = off_team.gk_player
            elif p1 == 2:
                self.ball = off_team.rd_player
                self.previous_pass = off_team.gk_player
            else:
                self.ball = off_team.ld_player
                self.previous_pass = off_team.gk_player
        else:
            if (self.ball == off_team.cf_player):
                self.cf_passto(off_team, deff_team)
                self.previous_pass = off_team.cf_player
            elif (self.ball == off_team.lw_player):
                self.lw_passto(off_team, deff_team)
                self.previous_pass = off_team.lw_player
            elif (self.ball == off_team.rw_player):
                self.rw_passto(off_team, deff_team)
                self.previous_pass = off_team.rw_player
            elif (self.ball == off_team.ld_player):
                self.ld_passto(off_team, deff_team)
                self.previous_pass = off_team.ld_player
            elif (self.ball == off_team.rd_player):
                self.rd_passto(off_team, deff_team)
                self.previous_pass = off_team.rd_player
            else:
                self.cd_passto(off_team, deff_team)
                self.previous_pass = off_team.cd_player

    def deff_matchup(self, off_team, deff_team, player):
        if (player == off_team.cf_player):
            return deff_team.cd_player
        elif (player == off_team.lw_player):
            return deff_team.rd_player
        elif (player == off_team.rw_player):
            return deff_team.ld_player
        elif (player == off_team.ld_player):
            return deff_team.rw_player
        elif (player == off_team.rd_player):
            return deff_team.lw_player
        elif (player == off_team.cd_player):
            return deff_team.cf_player

    def rd_passto(self, off_team, deff_team):
        p1 = random.randrange(1, 101)
        if p1 < 25:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.cd_player).defense) - off_team.cd_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.cd_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.cd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cd_player).steals +=1
        elif p1 < 50:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.rw_player).defense) - off_team.rw_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.rw_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.rw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rw_player).steals +=1
        elif p1 < 75:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.cf_player).defense) - off_team.cf_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.cf_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.cf_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cf_player).steals +=1
        elif p1 < 90:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.ld_player).defense) - off_team.ld_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.ld_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.ld_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.ld_player).steals +=1
        else:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.lw_player).defense) - off_team.lw_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.lw_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.lw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.lw_player).steals +=1

    def ld_passto(self, off_team, deff_team):
        p1 = random.randrange(1, 101)
        if p1 < 25:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.cd_player).defense) - off_team.cd_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.cd_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.cd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cd_player).steals +=1

        elif p1 < 50:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.lw_player).defense) - off_team.lw_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.lw_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.lw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.lw_player).steals +=1
        elif p1 < 75:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.cf_player).defense) - off_team.cf_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.cf_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.cf_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cf_player).steals +=1
        elif p1 < 90:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.rd_player).defense) - off_team.rd_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.rd_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.rd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rd_player).steals +=1
        else:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.rw_player).defense) - off_team.rw_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.rw_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.rw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rw_player).steals +=1

    def cd_passto(self, off_team, deff_team):
        p1 = random.randrange(1, 101)
        if p1 < 25:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.ld_player).defense) - off_team.ld_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.ld_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.ld_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.ld_player).steals +=1

        elif p1 < 50:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.rd_player).defense) - off_team.rd_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.rd_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.rd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rd_player).steals +=1
        elif p1 < 75:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.cf_player).defense) - off_team.cf_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.cf_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.cf_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cf_player).steals +=1
        elif p1 < 87:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.lw_player).defense) - off_team.lw_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.lw_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.lw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.lw_player).steals +=1
        else:
            p2 = random.randrange(1, 101)
            if (p2 > ((self.deff_matchup(off_team, deff_team, off_team.rw_player).defense) - off_team.rw_player.ballhandling * 1.5 + 20)):
                self.ball = off_team.rw_player
            else:
                self.ball = self.deff_matchup(
                    off_team, deff_team, off_team.rw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rw_player).steals +=1

    def lw_passto(self, off_team, deff_team):
        p1 = random.randrange(1,101)
        if p1 < 25:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.cd_player).defense) - off_team.cd_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.cd_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.cd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cd_player).steals +=1

        elif p1< 50:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.ld_player).defense) - off_team.ld_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.ld_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.ld_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.ld_player).steals +=1
        elif p1<75:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.cf_player).defense) - off_team.cf_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.cf_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.cf_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cf_player).steals +=1
        elif p1<90:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.rd_player).defense) - off_team.rd_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.rd_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.rd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rd_player).steals +=1
        else:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.rw_player).defense) - off_team.rw_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.rw_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.rw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rw_player).steals +=1

    def rw_passto(self, off_team, deff_team):
        p1 = random.randrange(1,101)
        if p1 < 25:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.cd_player).defense) - off_team.cd_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.cd_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.cd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cd_player).steals +=1

        elif p1< 50:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.rd_player).defense) - off_team.rd_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.rd_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.rd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rd_player).steals +=1
        elif p1<75:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.cf_player).defense) - off_team.cf_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.cf_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.cf_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cf_player).steals +=1
        elif p1<90:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.ld_player).defense) - off_team.ld_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.ld_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.ld_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.ld_player).steals +=1
        else:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.rw_player).defense) - off_team.rw_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.rw_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.rw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rw_player).steals +=1
    def cf_passto(self, off_team, deff_team):
        p1 = random.randrange(1,101)
        if p1 < 30:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.lw_player).defense) - off_team.lw_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.lw_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.lw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.lw_player).steals +=1

        elif p1< 60:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.rw_player).defense) - off_team.rw_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.rw_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.rw_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rw_player).steals +=1
        elif p1<75:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.cd_player).defense) - off_team.cd_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.cd_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.cd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.cd_player).steals +=1
        elif p1<90:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.ld_player).defense) - off_team.ld_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.ld_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.ld_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.ld_player).steals +=1
        else:
            p2 = random.randrange(1,101)
            if(p2 >((self.deff_matchup(off_team, deff_team, off_team.rd_player).defense) - off_team.rd_player.ballhandling * 1.5 + 20) ):
                self.ball = off_team.rd_player
            else:
                self.ball = self.deff_matchup(off_team, deff_team, off_team.rd_player)
                self.shot_clock = 0
                self.deff_matchup(off_team, deff_team, off_team.rd_player).steals +=1

    def shot(self, off_team, deff_team):
        rand1 = random.randrange(0,100)
        rand2 = random.randrange(0,100)
        if off_team.cf_player == self.ball:
            if rand1 < 90 or self.shot_clock<3:
                off_team.cf_player.shots +=1
                deff_team.gk_player.shots_allowed+=1
                if(((off_team.cf_player.shooting) - (deff_team.gk_player.goalkeeping/2))> rand2):
                    off_team.goals += 1
                    deff_team.gk_player.shots_allowed+=1
                    self.score(off_team)
                    print(f"{off_team.nickname}: {off_team.cf_player.last} scores from {int(off_team.cf_player.transition_distance +5)} meters away")
                    self.shot_clock = 0
                    if(self.previous_pass == off_team.cf_player):
                        off_team.cf_player.assists+=1
                    elif(self.previous_pass == off_team.lw_player):
                        off_team.lw_player.assists+=1
                    elif(self.previous_pass == off_team.rw_player):
                        off_team.rw_player.assists+=1
                    elif(self.previous_pass == off_team.ld_player):
                        off_team.ld_player.assists+=1
                    elif(self.previous_pass == off_team.rd_player):
                        off_team.rd_player.assists+=1
                    elif(self.previous_pass == off_team.cd_player):
                        off_team.cd_player.assists+=1
                    elif(self.previous_pass == off_team.gk_player):
                        off_team.gk_player.assists+=1
                    off_team.cf_player.goals +=1
                    deff_team.gk_player.goals_allowed+=1
                else:
                    deff_team.gk_player.saves+=1
                    self.shot_clock = 0
        elif off_team.lw_player == self.ball:
            if rand1 < 70 or self.shot_clock<3:
                off_team.lw_player.shots +=1
                deff_team.gk_player.shots_allowed+=1
                if(((off_team.lw_player.shooting/1.2) - (deff_team.gk_player.goalkeeping/2))< rand2):
                    off_team.goals += 1
                    self.score(off_team)
                    print(f"{off_team.nickname}: {off_team.lw_player.last} scores from {int(off_team.lw_player.transition_distance+ 8)} meters away!")
                    self.shot_clock = 0
                    if(self.previous_pass == off_team.cf_player):
                        off_team.cf_player.assists+=1
                    elif(self.previous_pass == off_team.lw_player):
                        off_team.lw_player.assists+=1
                    elif(self.previous_pass == off_team.rw_player):
                        off_team.rw_player.assists+=1
                    elif(self.previous_pass == off_team.ld_player):
                        off_team.ld_player.assists+=1
                    elif(self.previous_pass == off_team.rd_player):
                        off_team.rd_player.assists+=1
                    elif(self.previous_pass == off_team.cd_player):
                        off_team.cd_player.assists+=1
                    elif(self.previous_pass == off_team.gk_player):
                        off_team.gk_player.assists+=1
                    off_team.lw_player.goals +=1
                    deff_team.gk_player.goals_allowed+=1
                else:
                    deff_team.gk_player.saves+=1
                    self.shot_clock = 0
        elif off_team.rw_player == self.ball:
            if rand1 < 70 or self.shot_clock<3:
                off_team.rw_player.shots +=1
                deff_team.gk_player.shots_allowed+=1
                if(((off_team.rw_player.shooting/1.2) - (deff_team.gk_player.goalkeeping/2))> rand2):
                    off_team.goals += 1
                    self.score(off_team)
                    print(f"{off_team.nickname}: {off_team.rw_player.last} scores from {int(off_team.rw_player.transition_distance+ 8)} meters away!")
                    self.shot_clock = 0
                    if(self.previous_pass == off_team.cf_player):
                        off_team.cf_player.assists+=1
                    elif(self.previous_pass == off_team.lw_player):
                        off_team.lw_player.assists+=1
                    elif(self.previous_pass == off_team.rw_player):
                        off_team.rw_player.assists+=1
                    elif(self.previous_pass == off_team.ld_player):
                        off_team.ld_player.assists+=1
                    elif(self.previous_pass == off_team.rd_player):
                        off_team.rd_player.assists+=1
                    elif(self.previous_pass == off_team.cd_player):
                        off_team.cd_player.assists+=1
                    elif(self.previous_pass == off_team.gk_player):
                        off_team.gk_player.assists+=1
                    off_team.rw_player.goals +=1
                    deff_team.gk_player.goals_allowed+=1
                else:
                    deff_team.gk_player.saves+=1
                    self.shot_clock = 0
        elif off_team.rd_player == self.ball:
            if rand1 < 30 or self.shot_clock<3:
                off_team.rd_player.shots +=1
                deff_team.gk_player.shots_allowed+=1
                if(((off_team.rd_player.shooting/1.6) - (deff_team.gk_player.goalkeeping/3) - 10)> rand2):
                    off_team.goals += 1
                    self.score(off_team)
                    print(f"{off_team.nickname}: {off_team.rd_player.last} scores from {int(off_team.rd_player.transition_distance + 10)} meters away!")
                    self.shot_clock = 0
                    if(self.previous_pass == off_team.cf_player):
                        off_team.cf_player.assists+=1
                    elif(self.previous_pass == off_team.lw_player):
                        off_team.lw_player.assists+=1
                    elif(self.previous_pass == off_team.rw_player):
                        off_team.rw_player.assists+=1
                    elif(self.previous_pass == off_team.ld_player):
                        off_team.ld_player.assists+=1
                    elif(self.previous_pass == off_team.rd_player):
                        off_team.rd_player.assists+=1
                    elif(self.previous_pass == off_team.cd_player):
                        off_team.cd_player.assists+=1
                    elif(self.previous_pass == off_team.gk_player):
                        off_team.gk_player.assists+=1
                    off_team.rd_player.goals +=1
                    deff_team.gk_player.goals_allowed+=1
                else:
                    deff_team.gk_player.saves+=1
                    self.shot_clock = 0
        elif off_team.ld_player == self.ball:
            if rand1 < 30 or self.shot_clock<3:
                off_team.ld_player.shots +=1
                deff_team.gk_player.shots_allowed+=1
                if(((off_team.ld_player.shooting/1.6) - (deff_team.gk_player.goalkeeping/3) - 10)> rand2):
                    off_team.goals += 1
                    self.score(off_team)
                    print(f"{off_team.nickname}: {off_team.ld_player.last} scores from {int(off_team.ld_player.transition_distance + 10)} meters away!")
                    self.shot_clock = 0
                    if(self.previous_pass == off_team.cf_player):
                        off_team.cf_player.assists+=1
                    elif(self.previous_pass == off_team.lw_player):
                        off_team.lw_player.assists+=1
                    elif(self.previous_pass == off_team.rw_player):
                        off_team.rw_player.assists+=1
                    elif(self.previous_pass == off_team.ld_player):
                        off_team.ld_player.assists+=1
                    elif(self.previous_pass == off_team.rd_player):
                        off_team.rd_player.assists+=1
                    elif(self.previous_pass == off_team.cd_player):
                        off_team.cd_player.assists+=1
                    elif(self.previous_pass == off_team.gk_player):
                        off_team.gk_player.assists+=1
                    off_team.ld_player.goals +=1
                    deff_team.gk_player.goals_allowed+=1
                else:
                    deff_team.gk_player.saves+=1
                    self.shot_clock = 0
        elif off_team.cd_player == self.ball:
            if rand1 < 20 or self.shot_clock<3:
                off_team.cd_player.shots +=1
                deff_team.gk_player.shots_allowed+=1
                if(((off_team.cd_player.shooting/1.6) - (deff_team.gk_player.goalkeeping/3) - 10)> rand2):
                    off_team.goals += 1
                    self.score(off_team)
                    print(f"{off_team.nickname}: {off_team.cd_player.last} scores from {int(off_team.cd_player.transition_distance + 8)} meters away!")
                    self.shot_clock = 0
                    if(self.previous_pass == off_team.cf_player):
                        off_team.cf_player.assists+=1
                    elif(self.previous_pass == off_team.lw_player):
                        off_team.lw_player.assists+=1
                    elif(self.previous_pass == off_team.rw_player):
                        off_team.rw_player.assists+=1
                    elif(self.previous_pass == off_team.ld_player):
                        off_team.ld_player.assists+=1
                    elif(self.previous_pass == off_team.rd_player):
                        off_team.rd_player.assists+=1
                    elif(self.previous_pass == off_team.cd_player):
                        off_team.cd_player.assists+=1
                    elif(self.previous_pass == off_team.gk_player):
                        off_team.gk_player.assists+=1
                    off_team.cd_player.goals +=1
                    deff_team.gk_player.goals_allowed+=1
                else:
                    deff_team.gk_player.saves+=1
                    self.shot_clock = 0
                    


    def start_game(self):
        print("The game has started!")
        self.current_possession = self.team1.team_id

    def start_quarter(self):
        print("The game has started!")
        self.current_possession = self.team1.team_id

    def switch_possession(self):
        if self.current_possession == self.team1.team_id:
            self.current_possession = self.team2.team_id
            self.team1.newTransition()
        else:
            self.current_possession = self.team1.team_id
            self.team1.newTransition()

    def possesion(self, off_team, deff_team):
        off_team.swim()
        deff_team.swim()
        lost_possession = False
        self.shot_clock = 30
        self.ball = off_team.gk_player
        self.passto(off_team, deff_team)
        
        while self.shot_clock > 0 and self.time_remaining > 0:
            off_team.swim()
            deff_team.swim()
            self.shot_clock -= 1
            self.time_remaining -= 1

            if(self.shot_clock <20): 
                if(self.shot_clock%3 == 0):
                    self.passto(off_team, deff_team)
                elif (self.shot_clock <10) and (self.shot_clock%2 == 0):
                    self.shot(off_team,deff_team)
                    
        self.switch_possession()

    def score(self, team):
        self.scoreboard[team.abb] += 1
        print(f"{team.nickname} scores! with {self.time_remaining//60}:{self.time_remaining%60:02} remaining in Quarter {self.quarter} score: {self.scoreboard}")

    def end_game(self):
        print("Time's up! The game has ended.")
        print(f"Final score: {self.scoreboard}")

    def play(self):
        self.start_game()
        while self.time_remaining > 0 and self.quarter < 5:
            # simulate game play
            if self.current_possession == self.team1.team_id:
                # Team 1 has the ball
                # ...
                self.possesion(self.team1, self.team2)
            else:
                # Team 2 has the ball
                # ...
                self.possesion(self.team2, self.team1)
            rand1 = random.randrange(1, 5)
            # check for score

            # switch possession after a certain time

            # update time remaining
            self.time_remaining -= 1
            if self.time_remaining <= 0 and self.quarter < 4:
                print(
                    f"End of Quarter {self.quarter} score: {self.scoreboard}")
                self.quarter += 1
                self.time_remaining = 480

        self.end_game()
    def updateSchedule(self, home_team, away_team, match_number):
        sql = "UPDATE schedule SET home_goals = ?, away_goals = ?, played = 'Y' WHERE home_id = ? AND match_number = ?"
        val = (home_team.goals, away_team.goals, home_team.team_id, match_number)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        connection.commit()
    def updateStandings(self, home_team, away_team, match_number):
        home_team_wins = 0
        away_team_wins = 0
        tie = 0
        comp_type = ''
        sql = "SELECT competition_type FROM schedule WHERE match_number = ? AND home_id = ?;"
        val = (match_number, home_team.team_id)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        comp_type = mycursor.fetchone()[0]

        if(home_team.goals > away_team.goals):
            home_team_wins = 1
        elif(away_team.goals > home_team.goals):
            away_team_wins = 1
        elif(home_team.goals == away_team.goals):
            tie = 1
        
        sql = "UPDATE standings SET wins = wins + ?, losses = losses + ?, ties = ties + ?, goals_scored = goals_scored + ?, goals_against = goals_against + ? WHERE competition_type = ? AND team_id = ?;"
        val = (home_team_wins, away_team_wins, tie, home_team.goals, away_team.goals, comp_type, home_team.team_id)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        connection.commit()

        sql = "UPDATE standings SET wins = wins + ?, losses = losses + ?, ties = ties + ?, goals_scored = goals_scored + ?, goals_against = goals_against + ? WHERE competition_type = ? AND team_id = ?;"
        val = (away_team_wins, home_team_wins, tie, away_team.goals, home_team.goals, comp_type, away_team.team_id)
        mycursor = connection.cursor()
        mycursor.execute(sql, val)
        connection.commit()
    def updateStats(self, home_team, away_team, match_number):
        home_team.cf_player.setStats(home_team.team_id, away_team.team_id, home_team.cf_player.intPlayerId, match_number)
        home_team.lw_player.setStats(home_team.team_id, away_team.team_id, home_team.lw_player.intPlayerId, match_number)
        home_team.rw_player.setStats(home_team.team_id, away_team.team_id, home_team.rw_player.intPlayerId, match_number)
        home_team.ld_player.setStats(home_team.team_id, away_team.team_id, home_team.ld_player.intPlayerId, match_number)
        home_team.rd_player.setStats(home_team.team_id, away_team.team_id, home_team.rd_player.intPlayerId, match_number)
        home_team.cd_player.setStats(home_team.team_id, away_team.team_id, home_team.cd_player.intPlayerId, match_number)
        home_team.gk_player.setStats(home_team.team_id, away_team.team_id, home_team.gk_player.intPlayerId, match_number)

        away_team.cf_player.setStats(away_team.team_id, home_team.team_id, away_team.cf_player.intPlayerId, match_number)
        away_team.lw_player.setStats(away_team.team_id, home_team.team_id, away_team.lw_player.intPlayerId, match_number)
        away_team.rw_player.setStats(away_team.team_id, home_team.team_id, away_team.rw_player.intPlayerId, match_number)
        away_team.ld_player.setStats(away_team.team_id, home_team.team_id, away_team.ld_player.intPlayerId, match_number)
        away_team.rd_player.setStats(away_team.team_id, home_team.team_id, away_team.rd_player.intPlayerId, match_number)
        away_team.cd_player.setStats(away_team.team_id, home_team.team_id, away_team.cd_player.intPlayerId, match_number)
        away_team.gk_player.setStats(away_team.team_id, home_team.team_id, away_team.gk_player.intPlayerId, match_number)

class Session(object):
    match_number = 0


    def __init__(self):
        self.schedule()
    def schedule(self):
        sql = "SELECT match_number FROM schedule WHERE played = 'N' LIMIT 1;"
        mycursor = connection.cursor()
        mycursor.execute(sql)
        self.match_number = mycursor.fetchone()[0]
        print (self.match_number)
        next_session_match  = self.match_number+2
        while(self.match_number<next_session_match):
            sql = "SELECT match_number, home_id, away_id FROM schedule WHERE played = 'N' LIMIT 1;"
            mycursor = connection.cursor()
            mycursor.execute(sql)
            nextval = mycursor.fetchone()
            
            match_num = nextval[0]
            if nextval[0] == self.match_number+1:
                self.match_number+=1
            if nextval[0] != next_session_match:
                home_id = nextval[1]
                away_id = nextval[2]
                home_team = Teams(home_id)
                away_team = Teams(away_id)
                game = Match(home_team, away_team, match_num)
                
                


    

# # create two teams
# team1 = Teams(4)
# team2 = Teams(3)

# # create a new game
# game = Match(team1, team2, 1)

# # simulate the game
# game.play()

session = Session()
