import mysql.connector

mydb = mysql.connector.connect(host='Sizov.mysql.pythonanywhere-services.com',database='Sizov$Nearest_bar',user='Sizov',password='Astra055')
mycursor=mydb.cursor()

#mycursor.execute("CREATE TABLE bars_fav (name VARCHAR(255), rait DOUBLE, price VARCHAR(255), adress VARCHAR(255), url VARCHAR(255) , longitude DOUBLE, latitude DOUBLE, time_open TIME, time_close TIME, likes INT, favorite INT)")
#mycursor.execute("CREATE TABLE guys (id INT,  last_longitude FLOAT, last_latitude FLOAT, last_visit_time TIME, last_visit_data DATE)")
#mycursor.execute("DELETE FROM guys WHERE id = 275457031")

#mycursor.execute("DROP TABLE bars_fav")

#info = ('Ровесник', '4.66', '150–250 ₽', 'Малый Гнездниковский пер. 9 стр. 2 Москва Россия', '/maps/org/rovesnik/168523045237/', 55.762768, 37.605373)
#s="UPDATE bars_fav SET rait='4.66' WHERE  (name = 'Ровесник' AND longitude = 55.762768 AND latitude = 37.605373)"
#print(s.format(('Ровесник',)))
#mycursor.execute("UPDATE bars_fav SET rait='4.66' WHERE (name = %s AND longitude = %s)", (info[0], info[-2],))
#sql_formula = "INSERT INTO bars_fav (name, rait, price, adress, url, longitude, latitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#resa = mycursor.fetchall()
#print(resa)
#mydb.commit()

#mycursor.execute("SHOW TABLES;")

#mycursor.execute("DELETE FROM bars_fav WHERE name = 'Под Мухой'")
#mydb.commit()

#resa = mycursor.fetchall()

#for i in resa:
 #   print(i[5], i[6])

#id2=275457031
#find_id="SELECT * FROM guys WHERE id={}".format(id2)
#mycursor.execute(find_id)

