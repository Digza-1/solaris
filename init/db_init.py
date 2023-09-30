import mysql.connector


# init database
q1 = "create database project_solaris;"
q2 = "use project_solaris;"

# admins table
q3 = """create table admins ( admin_id int primary key auto_increment,
username varchar(40) unique,
passwd varchar(50) not null);"""

# users table
q4 = """create table users ( player_id int primary key auto_increment,
username varchar(40) unique,
passwd varchar(50) not null);"""

# settings sql
# game settings sql
q5 = """create table game_settings (player_id int primary key,
    seed decimal(5,3),
    speed decimal(5,3),
    grey_threshold decimal(5,3),
    red_threshold decimal(5,3),
    blue_threshold decimal(5,3),
    difficulty varchar(15),
    costume int);"""

# default settings sql
q6 = """create table game_default_settings (
    speed decimal(5,3),
    grey_threshold decimal(5,3),
    red_threshold decimal(5,3),
    blue_threshold decimal(5,3),
    difficulty varchar(15),
    costume int);"""

# game worlds
q7 = """create table game_worlds ( player_id int,
world_id int primary key auto_increment,
world_name varchar(40),
seed int,
x_pos int,
y_pos int,
obj_x int,
obj_y int);
"""

# player stats
q8 = """create table player_stats ( player_id int primary key,
world_id int,
distance_moved int,
dist_from_obj int,
collisions int)
"""

inq1 = "insert into users(username,passwd) values('user','user');"
inq2 = "insert into admins(username,passwd) values('admin','root');"

# initialise game_default_settings
inq3 = """insert into game_default_settings (
    speed, grey_threshold, red_threshold, blue_threshold, difficulty, costume
) values (0.1, 0.25, 0.01, 0.1, 'normal', 0);"""

inq4 = """insert into game_settings (
    player_id, seed, speed, grey_threshold, red_threshold, blue_threshold, difficulty, costume
) values (0,0, 0.1, 0.25, 0.01, 0.1, 'normal', 1);"""

inq5 = """insert into game_default_settings(speed,
grey_threshold,
red_threshold,
blue_threshold,
difficulty,
costume) values(0.1, 0.25, 0.01, 0.1,'normal',1);"""

# q2, q3, q4, q5, q6, q7, q8

query_list = [q1, q2, q3, q4, q5, q6, q7, q8, inq1, inq2, inq3, inq4]
sqlPass = "123"


def database_init():
    global query_list
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database=""
    )
    mycursor = mydb.cursor()

    try:
        mycursor.execute("drop database project_solaris")
        mydb.commit()
    except:
        pass
    ind = 0
    for query in query_list:
        print(ind)
        mycursor.execute(query)
        mydb.commit()
        ind += 1

    mycursor.close()
    mydb.close()


database_init()
