from time import sleep
import psycopg2 as pg

sd = open("stop_details2.txt")

conn = pg.connect("dbname=BTRS user=postgres password=postgres port=5432")
cur = conn.cursor()

details = []

bus_no = 0

lines = sd.readlines()
i =0
while i < len(lines) :
	line = lines[i]
	data = line.strip().split('|')
	print("----> ",line)
	i += 1
	if(data[0] == 'bus :') :
		cur.execute("select * from busses where busno = %s",[int(data[1])])
		c = cur.fetchall()
		print("cccc->",c)
		l = len(c)
		if not l > 0  :

			cur.execute("insert into busses (busno , route , no_of_stops , bclass) values(%s , %s , %s , %s) ",[int(data[1]), data[2] , int(data[-1]) - 1, data[-2]])
			
			print(data)

			for j in range(int(data[-1]) - 1) :

				print(lines[i+j],i+j)
				stop = lines[i+j].strip().split("|")
				if j == 0 :
					cur.execute("update busses set startat = %s ,  arr_time = %s where busno = %s",[stop[1] , stop[-1] , int(data[1])])
					

				if j == int(data[-1]) -2 :
					cur.execute("update busses set endat = %s ,  dept_time = %s where busno = %s",[stop[1] , stop[-1] , int(data[1])])


				cur.execute("select stop_id from stops where stop_name = %s and stop_district = %s and stop_taluka = %s",[stop[1] + "-" + stop[2],stop[2],stop[3]])
				stop_exist = cur.fetchall()
				if len(stop_exist) == 0 :
					cur.execute("insert into stops(stop_name ,stop_district , stop_taluka) values(%s,%s,%s)",[stop[1] + "-" + stop[2],stop[2],stop[3]])
					
				else :
					cur.execute("select stop_id from stops where stop_name = %s and stop_district = %s and stop_taluka = %s",[stop[1] + "-" + stop[2],stop[2],stop[3]])
					(stop_id,) = cur.fetchone()
					cur.execute("insert into bus_stops (busno , stop_id , stop_no) values (%s ,%s , %s) ",[int(data[1]),int(stop_id),j+1])

			print("done ------------------------------------------",i + j+1)
			i = i + j + 1

conn.commit()
cur.close()
conn.close()

			

