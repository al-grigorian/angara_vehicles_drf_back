import psycopg2

connection = psycopg2.connect(dbname="angara_vehicles_assembly", host="localhost", user="postgres", password="psadeiw123", port="5433")
cursor = connection.cursor()
