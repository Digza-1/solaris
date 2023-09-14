import mysql.connector

sqlPass = "CH3-CH2-CH2-CH3"

q1 = "create database project_solaris;"
q2 = "use project_solaris;"

q3 = """create table admins ( admin_id int primary key,
username varchar(40) unique,
passwd varchar(50) not null);"""

q4 = '''create table users ( player_id int primary key,
username varchar(40) unique,
passwd varchar(50) not null);'''

q5 = '''create table game_settings ( player_id int primary key,
world_id int,
seed int,
x_pos int,
y_pos int,
speed int,
grey_thershold decimal(5,3)
red_thershold decimal(5,3)
blue_thershold decimal(5,3)
difficulty varchar(15),
costume int)
'''

q6 = '''create table game_default_settings (
x_pos int,
y_pos int,
speed int,
grey_thershold decimal(5,3)
red_thershold decimal(5,3)
blue_thershold decimal(5,3)
difficulty varchar(15),
costume int)
 '''




query_list = [q1, q2, q3, q4, q5, q6 ]


def create_tables():
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database=""
    )
    mycursor = mydb.cursor()

    for query in query_list:
        print(query)
        mycursor.execute(query)
        mydb.commit()

    mycursor.close()
    mydb.close()


create_tables()
