import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Task I

def init_db():
    # import the FIFA dataset
    secret = open('secret.txt', 'r')
    pw = secret.read()[:-1]
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS fifa;")
    conn.commit()
    df = pd.read_csv('data/players_20.csv', index_col = False)
    df.columns = [c.lower() for c in df.columns]
    engine = create_engine('postgresql://postgres:{0}@localhost:5432/postgres'.format(pw))
    df.to_sql("fifa", engine, method='multi')
    call = '''alter table fifa 
DROP COLUMN IF EXISTS index,
alter column sofifa_id type int4,
add primary key (sofifa_id),
alter column work_rate type varchar,
alter column weight_kg type int4,
alter column weak_foot type int4,
alter column wage_eur type money,
alter column value_eur type money,
alter column team_position type varchar,
alter column team_jersey_number type int4,
alter column st type varchar,
alter column skill_moves type int4,
alter column skill_long_passing type int4,
alter column skill_fk_accuracy type int4,
alter column skill_dribbling type int4,
alter column skill_curve type int4,
alter column skill_ball_control	type int4,
alter column short_name	type varchar,
alter column shooting type int4,
alter column rwb type varchar,
alter column rw type varchar,
alter column rs type varchar,
alter column rm type varchar,
alter column rf type varchar,
alter column release_clause_eur type money using release_clause_eur::numeric::money,
alter column real_face type varchar,
alter column rdm type varchar,
alter column rcm type varchar,
alter column rcb type varchar,
alter column rb	type varchar,
alter column ram type varchar,
alter column preferred_foot type varchar,
alter column power_strength type int4,
alter column power_stamina type int4,
alter column power_shot_power type int4,
alter column power_long_shots type int4,
alter column power_jumping type int4,
alter column potential type int4,
alter column player_url type varchar,
alter column player_traits type varchar,
alter column player_tags type varchar,
alter column player_positions type varchar,
alter column physic type int4,
alter column passing type int4,
alter column pace type int4,
alter column overall type int4,
alter column nationality type varchar,
alter column nation_position type varchar,
alter column nation_jersey_number type int4,
alter column movement_sprint_speed type int4,
alter column movement_reactions type int4,
alter column movement_balance type int4,
alter column movement_agility type int4,
alter column movement_acceleration type int4,
alter column mentality_vision type int4,
alter column mentality_positioning type int4,
alter column mentality_penalties type int4,
alter column mentality_interceptions type int4,
alter column mentality_composure type int4,
alter column mentality_aggression type int4,
alter column lwb type varchar,
alter column lw	type varchar,
alter column ls	type varchar,
alter column long_name type varchar,
alter column loaned_from type varchar,
alter column lm	type varchar,
alter column lf type varchar,
alter column ldm type varchar,
alter column lcm type varchar,
alter column lcb type varchar,
alter column lb type varchar,
alter column lam type varchar,
alter column joined type date USING joined::date,
alter column international_reputation type int4,
alter column height_cm type int4,
alter column goalkeeping_reflexes type int4,
alter column goalkeeping_positioning type int4,
alter column goalkeeping_kicking type int4,
alter column goalkeeping_handling type int4,
alter column goalkeeping_diving type int4,
alter column gk_speed type int4,
alter column gk_reflexes type int4,
alter column gk_positioning type int4,
alter column gk_kicking type int4,
alter column gk_handling type int4,
alter column gk_diving type int4,
alter column dribbling type int4,
alter column dob type date USING joined::date,
alter column defending_standing_tackle type int4,
alter column defending_sliding_tackle type int4,
alter column defending_marking type int4,
alter column defending type int4,
alter column contract_valid_until type int4,
alter column cm type varchar,
alter column club type varchar,
alter column cf type varchar,
alter column cdm type varchar,
alter column cb type varchar,
alter column cam type varchar,
alter column body_type type varchar,
alter column attacking_volleys type int4,
alter column attacking_short_passing type int4,
alter column attacking_heading_accuracy type int4,
alter column attacking_finishing type int4,
alter column attacking_crossing type int4,
alter column age type int4;'''
    cursor.execute(call)
    conn.commit()
    conn.close()


# Task II

## 1

def top_players(x):
    # List the x players who achieved highest improvement across all skillsets. The steps are:
    # 1. Overall skill scores are calculated by averaging scores of dribbling, curve, fk accuracy, long passing and ball control.
    # 2. The improvement is overall skill scores minus overall score of a player
    # 3. Choose the players with top x improvement scores.
    # Input: x: the number of players to output
    # Output: a list of full names of players with top x improvements
    secret = open('secret.txt', 'r')
    pw = secret.read()[:-1]
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select long_name from fifa
                order by (skill_dribbling + skill_curve + skill_fk_accuracy + skill_long_passing + skill_ball_control)/5 - overall desc
                limit {0};'''
    cursor.execute(call.format(x))
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return [a[0] for a in output]

## 2

def largest_club_2021(y):
    # List the y clubs that have largest number of players with contracts ending in 2021.
    # Input: y: the number of clubs to output
    # Output: list of the required club names
    secret = open('secret.txt', 'r')
    pw = secret.read()[:-1]
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select club from fifa
                where contract_valid_until = 2021
                group by club
                order by count(distinct long_name) desc limit {0};'''
    cursor.execute(call.format(y))
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return [a[0] for a in output]

## 3

def largest_club(z):
    # List the z clubs with largest number of players in the dataset where z >= 5.
    # Input: y: the number of clubs to output
    # Output: list of the required club names
    if z < 5:
        raise TypeError("Error: the number should be greater or equal to 5")
    secret = open('secret.txt', 'r')
    pw = secret.read()[:-1]
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select club from fifa
                group by club
                order by count(distinct long_name) desc limit {0};'''
    cursor.execute(call.format(z))
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return [a[0] for a in output]

## 4

def popular_nation_team():
    # Get the most popular nation_position and team_position in the dataset
    # Output: a dictionary with nation: most popular nation_position, and team: most popular team position
    secret = open('secret.txt', 'r')
    pw = secret.read()[:-1]
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call1 = '''select nation_position from fifa
                group by nation_position
                order by count(distinct long_name) desc limit 2;'''
    call2 = '''select team_position from fifa
                group by team_position
                order by count(distinct long_name) desc limit 1;'''
    cursor.execute(call1)
    nation = cursor.fetchall()
    cursor.execute(call2)
    team = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"nation": nation[1][0],"team": team[0][0]}

## 5

def popular_nationality():
    # Get the most popular nationality for the players in the dataset
    secret = open('secret.txt', 'r')
    pw = secret.read()[:-1]
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select nationality from fifa
                group by nationality
                order by count(distinct long_name) desc limit 1;'''
    cursor.execute(call)
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return output[0][0]



