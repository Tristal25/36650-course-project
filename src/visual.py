import seaborn as sns
from src.module import *
import matplotlib.pyplot as plt

def visualize_top10_improvement():
    # Visualize the 10 players who achieved highest improvement across all skillsets. The steps are:
    # 1. Overall skill scores are calculated by averaging scores of dribbling, curve, fk accuracy, long passing and ball control.
    # 2. The improvement is overall skill scores minus overall score of a player
    # 3. Choose the players with top x improvement scores.

    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select short_name, (skill_dribbling + skill_curve + skill_fk_accuracy + skill_long_passing + skill_ball_control)/5 - overall as improvement 
                from fifa
                order by improvement desc
                limit 10;'''
    cursor.execute(call)
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    dat = pd.DataFrame({
        "player": [a[0] for a in output],
        "improvement": [a[1] for a in output]
        })
    sns.catplot(x = "player", y = "improvement", kind="bar", data = dat)
    plt.show()

def visualize_top5_value():
    # Visualize the 5 players who are highest in value

    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select short_name, cast(value_eur::numeric as integer)
                from fifa
                order by value_eur desc
                limit 5;'''
    cursor.execute(call)
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    dat = pd.DataFrame({
        "player": [a[0] for a in output],
        "value": [a[1] for a in output]
        })
    sns.catplot(x = "player", y = "value", kind="bar", data = dat)
    plt.show()

def visualize_top10_traits():
    # Visualize the 5 players who are highest in value

    conn = psycopg2.connect(database="postgres", user='postgres', password=pw, host='127.0.0.1', port='5432')
    cursor = conn.cursor()
    call = '''select short_name, player_traits
                from fifa
				where player_traits is not NULL;'''
    cursor.execute(call)
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    player = [a[0] for a in output]
    traits = [a[1] for a in output]
    num_traits = [len(a[1].split(sep = ",")) for a in output]
    dat_full = pd.DataFrame({
        "player": player,
        "num_traits": num_traits
        })
    dat = dat_full.loc[dat_full.num_traits >= 6].sort_values("num_traits", ascending=False)
    sns.catplot(x = "player", y = "num_traits", kind="bar", data = dat)
    plt.show()