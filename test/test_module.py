import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, "src")
sys.path.insert(0,src_dir)

import pytest
from src.module import *


def test_init_db():
    init_db()
    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()

    # Test table existence
    cursor.execute("select exists (select * from fifa);")
    exist = cursor.fetchall()[0][0]
    assert exist == True, "Table not created"

    # Test columns
    cursor.execute('''SELECT
	column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'fifa';''')
    col_info = cursor.fetchall()
    cols = [('sofifa_id', 'integer'), ('physic', 'integer'), ('gk_diving', 'integer'), ('gk_handling', 'integer'),
            ('gk_kicking', 'integer'), ('gk_reflexes', 'integer'), ('gk_speed', 'integer'),
            ('gk_positioning', 'integer'), ('attacking_crossing', 'integer'), ('attacking_finishing', 'integer'),
            ('attacking_heading_accuracy', 'integer'), ('attacking_short_passing', 'integer'),
            ('attacking_volleys', 'integer'), ('skill_dribbling', 'integer'), ('skill_curve', 'integer'),
            ('skill_fk_accuracy', 'integer'), ('skill_long_passing', 'integer'), ('skill_ball_control', 'integer'),
            ('movement_acceleration', 'integer'), ('movement_sprint_speed', 'integer'), ('movement_agility', 'integer'),
            ('movement_reactions', 'integer'), ('movement_balance', 'integer'), ('power_shot_power', 'integer'),
            ('power_jumping', 'integer'), ('power_stamina', 'integer'), ('power_strength', 'integer'),
            ('power_long_shots', 'integer'), ('mentality_aggression', 'integer'), ('mentality_interceptions', 'integer'),
            ('mentality_positioning', 'integer'), ('mentality_vision', 'integer'), ('mentality_penalties', 'integer'),
            ('mentality_composure', 'integer'), ('defending_marking', 'integer'), ('defending_standing_tackle', 'integer'),
            ('defending_sliding_tackle', 'integer'), ('goalkeeping_diving', 'integer'), ('goalkeeping_handling', 'integer'),
            ('goalkeeping_kicking', 'integer'), ('goalkeeping_positioning', 'integer'), ('goalkeeping_reflexes', 'integer'),
            ('age', 'integer'), ('dob', 'date'), ('height_cm', 'integer'), ('weight_kg', 'integer'), ('overall', 'integer'),
            ('potential', 'integer'), ('value_eur', 'money'), ('wage_eur', 'money'), ('international_reputation', 'integer'),
            ('weak_foot', 'integer'), ('skill_moves', 'integer'), ('release_clause_eur', 'money'),
            ('team_jersey_number', 'integer'), ('joined', 'date'), ('contract_valid_until', 'integer'),
            ('nation_jersey_number', 'integer'), ('pace', 'integer'), ('shooting', 'integer'), ('passing', 'integer'),
            ('dribbling', 'integer'), ('defending', 'integer'), ('player_url', 'character varying'),
            ('short_name', 'character varying'), ('long_name', 'character varying'), ('ldm', 'character varying'),
            ('player_traits', 'character varying'), ('cdm', 'character varying'), ('rdm', 'character varying'),
            ('nationality', 'character varying'), ('club', 'character varying'), ('rwb', 'character varying'),
            ('lb', 'character varying'), ('lcb', 'character varying'), ('cb', 'character varying'),
            ('player_positions', 'character varying'), ('preferred_foot', 'character varying'), ('rcb', 'character varying'),
            ('rb', 'character varying'), ('ls', 'character varying'), ('work_rate', 'character varying'),
            ('body_type', 'character varying'), ('real_face', 'character varying'), ('st', 'character varying'),
            ('player_tags', 'character varying'), ('team_position', 'character varying'), ('rs', 'character varying'),
            ('loaned_from', 'character varying'), ('lw', 'character varying'), ('lf', 'character varying'),
            ('nation_position', 'character varying'), ('cf', 'character varying'), ('rf', 'character varying'),
            ('rw', 'character varying'), ('lam', 'character varying'), ('cam', 'character varying'),
            ('ram', 'character varying'), ('lm', 'character varying'), ('lcm', 'character varying'),
            ('cm', 'character varying'), ('rcm', 'character varying'), ('rm', 'character varying'),
            ('lwb', 'character varying')]
    assert col_info == cols, "Columns wrong"

    conn.commit()
    conn.close()

def test_top_players_happy():
    assert top_players(1) is not None, "Return None for valid input"
    assert top_players(1) == ['Thom Haye'], "Top 1 player wrong"
    assert top_players(5) ==['Alejandro Corredera Alardi', 'Thom Haye', 'Wilson Allan Rosan Dourado',
                             'Charlie Adam', 'Alan Zamorado'], "Wrong answer for normal input number"
    assert top_players(50) == ['Alejandro Corredera Alardi', 'Thom Haye', 'Alan Zamorado', 'Nuno Caio Cedrim Feitosa',
                               'Wilson Allan Rosan Dourado', 'Charlie Adam', 'Yong Gi Ryang', 'Hakan Çalhanoğlu',
                               'Ager Aketxe Barrutia', 'Hicham Faik', '小池 裕太', 'Gerardo Alfredo Bruna Blanco',
                               'Luca Clemenza', '中村 宪剛', '太田 宏介', 'Daniel Aquino Pintos', 'Sebastian Giovinco',
                               'José Ernesto Sosa', 'Enis Bardhi', 'Mario Kvesić', 'Nordin Gerzić', 'Selçuk İnan',
                               'Marcos Álvarez', 'Caner Erkin', 'Reece Cole', 'Víctor Ignacio Malcorra', '汪嵩', '卢琳',
                               'Iuri José  Picanço Medeiros', 'Unai Vencedor Paris', 'Felipe Castaldo Curcio',
                               'Néstor Susaeta Jaurrieta', 'Sean Goss', 'Jorge Jonathan Espericueta Escamilla',
                               'Pedro León Sánchez Gil', 'Driss Fettouhi', '远藤 保仁', 'Matías Nicolás Rojas Romero',
                               'Matías Ariel Fernández Fernández', 'Alessandro Rosina', 'James  Ward-Prowse',
                               'Cristian Eduardo Canío Manosalva', 'Salvador Sevilla López', 'Marko Vejinović',
                               'Ross Wallace', 'Juan Brunetta', 'Robert Skov', 'Daniel Pacheco Lobato', 'Lovro Majer',
                               'Rubén  Rochina Naixes'], "Wrong answer for large input number"

def test_top_players_sad():
    try:
        top_players(None)
        assert False
    except TypeError:
        assert True

    try:
        top_players("abc")
        assert False
    except TypeError:
        assert True

    try:
        top_players(1.5)
        assert False
    except TypeError:
        assert True

    try:
        top_players(-2)
        assert False
    except TypeError:
        assert True

    try:
        top_players(0)
        assert False
    except TypeError:
        assert True

def test_largest_club_2021_happy():
    assert largest_club_2021(1) is not None, "Return None for valid input"
    assert largest_club_2021(1) == ['1. FC Kaiserslautern'], "Top 1 club wrong"
    assert largest_club_2021(5) == ['FC Ingolstadt 04', '1. FC Kaiserslautern', 'FC Girondins de Bordeaux', 'Kasimpaşa SK',
                                    'SV Wehen Wiesbaden'], "Wrong answer for normal input number"
    assert largest_club_2021(50) == ['FC Ingolstadt 04', '1. FC Kaiserslautern', 'FC Girondins de Bordeaux',
                                     'Kasimpaşa SK', 'SV Wehen Wiesbaden', 'FC St. Gallen', 'Ascoli', 'Newport County',
                                     'MSV Duisburg', 'Hellas Verona', 'FC Zürich', 'Al Fateh', 'Amiens SC',
                                     'Crystal Palace', 'Vélez Sarsfield', 'Holstein Kiel', 'Colchester United',
                                     'Real Sporting de Gijón', 'KFC Uerdingen 05', 'Leyton Orient', 'SC Preußen Münster',
                                     'Pisa', 'Heart of Midlothian', 'Getafe CF', 'Pogoń Szczecin', 'Fleetwood Town',
                                     'Leeds United', 'UD Las Palmas', 'SCR Altach', 'SC Paderborn 07', 'SV Meppen',
                                     'VfL Osnabrück', 'Blackburn Rovers', 'KV Kortrijk', 'Ranheim Fotball', 'Empoli',
                                     'Preston North End', 'Karlsruher SC', 'Aberdeen', 'Eintracht Braunschweig',
                                     'En Avant de Guingamp', 'Ipswich Town', 'Rio Ave FC', 'FC Erzgebirge Aue',
                                     'Olympique de Marseille', 'Deportivo Alavés', 'Gimnasia y Esgrima La Plata',
                                     'Málaga CF', 'PEC Zwolle', 'Lechia Gdańsk'], "Wrong answer for large input number"

def test_largest_club_2021_sad():
    try:
        largest_club_2021(None)
        assert False
    except TypeError:
        assert True

    try:
        largest_club_2021("abc")
        assert False
    except TypeError:
        assert True

    try:
        largest_club_2021(1.5)
        assert False
    except TypeError:
        assert True

    try:
        largest_club_2021(-2)
        assert False
    except TypeError:
        assert True

    try:
        largest_club_2021(0)
        assert False
    except TypeError:
        assert True

def test_largest_club_happy():
    assert largest_club(5) is not None, "Return None for valid input"
    assert largest_club(5) == ['Arsenal', '1. FC Union Berlin', 'AS Monaco', '1. FSV Mainz 05', 'Aston Villa'], "Top 5 club wrong"
    assert largest_club(10) is not None, "Return None for valid input"
    assert largest_club(10) == ['Borussia Mönchengladbach', 'Bournemouth', 'Atlético Madrid', 'Athletic Club de Bilbao',
                                'Aston Villa', '1. FC Union Berlin', '1. FSV Mainz 05', 'Arsenal', 'AS Monaco',
                                'Brighton & Hove Albion'], "Wrong answer for normal input number"
    assert largest_club(50) == ['Watford', 'Wolverhampton Wanderers', 'Tottenham Hotspur', 'VfL Wolfsburg',
                                'West Ham United', 'RC Celta', 'Real Madrid', 'SC Paderborn 07', 'Real Valladolid CF',
                                'Valencia CF', 'Southampton', 'Sevilla FC', 'Paris Saint-Germain', 'RB Leipzig',
                                'Crystal Palace', 'Hertha BSC', 'FC Nantes', 'Manchester City', 'Liverpool', 'Lecce',
                                'Leicester City', 'Udinese', 'Norwich City', 'Sheffield United', 'Atlético Madrid',
                                'Newcastle United', '1. FC Union Berlin', 'Everton', 'Chelsea', 'Parma', '1. FSV Mainz 05',
                                'Borussia Mönchengladbach', 'FC Barcelona', 'Eintracht Frankfurt', 'AS Monaco',
                                'Bournemouth', 'Hellas Verona', 'Fortuna Düsseldorf', 'Juventus', 'CD Leganés',
                                'Brighton & Hove Albion', 'Lazio', 'Athletic Club de Bilbao', 'Deportivo Alavés',
                                'Aston Villa', 'Burnley', 'Arsenal', 'FC Augsburg', 'Manchester United',
                                'SV Werder Bremen'], "Wrong answer for large input number"

def test_largest_club_sad():
    try:
        largest_club(None)
        assert False
    except TypeError:
        assert True

    try:
        largest_club("abc")
        assert False
    except TypeError:
        assert True

    try:
        largest_club(1.5)
        assert False
    except TypeError:
        assert True

    try:
        largest_club(-2)
        assert False
    except TypeError:
        assert True

    try:
        largest_club(0)
        assert False
    except TypeError:
        assert True

    try:
        largest_club(4)
        assert False
    except TypeError:
        assert True


def test_popular_nation_team():
    assert popular_nation_team() is not None, "Returned None"
    assert popular_nation_team() == {'nation': 'SUB', 'team': 'SUB'}, "Wrong result"

def test_popular_nationality():
    assert popular_nationality() is not None, "Returned None"
    assert popular_nationality() == 'England', "Wrong result"

