import mysql.connector

sqlPass = "CH3-CH2-CH2-CH3"

q1 = "create database project_solaris;"
q2 = "use project_solaris;"
q3 = """create table player_stats 
( player_id int primary key,world_id int,
distance_moved int,depth int,blocks_broken int,blocks_placed int);"""

q4 = "create table users ( player_id int primary key,username varchar(40) unique,passwd varchar(50) not null);"
q5 = "create table items ( item_id int primary key,item_name varchar(20) );"

query_list = [q1, q2, q3, q4, q5]


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
