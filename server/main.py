from flask import Flask,render_template,Blueprint,request,json,Response
from . import db

main = Blueprint('main',__name__)

def getStopsData() :

    stops = db.session.execute("select stop_name from stops")
    stops_data = [str(r[0]) for r in stops]
    return json.dumps(stops_data)

@main.route("/")
def homePage() :
    return render_template('index.html', stops = getStopsData())

@main.route("/searchbus/")
def searchBusPage() :
    return render_template("searchbus.html",stops = getStopsData(), results = [],formdetails = None)


@main.route("/searchbus/",methods=['POST'])
def searchBus() :
    source = request.form['source']
    dest = request.form['dest']
    jdate = request.form['jdate']
    bus_class = request.form['bus_class']
    SQL_final = "select q2.busno , route , no_of_stops , bclass , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc from ( select  busno , route , no_of_stops , q1.bclass , arr_time , dept_time , class_name  ,no_of_seats , reserved , class_inc from (select busno , route , no_of_stops , bclass , arr_time , dept_time from busses where busno in  (select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :source) intersect select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :dest ) ) ) as q1 inner join bus_class on q1.bclass = bus_class.bclass ) as q2 left outer join (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno "
    SQL_final2 = "select q2.busno , route , no_of_stops , bclass , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc from ( select  busno , route , no_of_stops , q1.bclass , arr_time , dept_time , class_name  ,no_of_seats , reserved , class_inc from (select busno , route , no_of_stops , bclass , arr_time , dept_time from busses where busno in  (select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :source) intersect select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :dest ) ) ) as q1 inner join (select * from bus_class where bclass = ':busclass') as q4  on q1.bclass = q4.bclass ) as q2 left outer join (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno "

    print("hello")
    if bus_class  != "ANY" :
        results = db.session.execute(SQL_final2,{'source':source ,'dest':dest,'jdate':jdate ,'busclass' : bus_class})

    else :
        results = db.session.execute(SQL_final,{'source':source ,'dest':dest,'jdate':jdate})

    bus_details = [ [i for i in r] for r in results]
    try :

        i = 0 
        while i < len(bus_details) :
            dropornot = db.session.execute("select x.in_no , y.out_no from (select busno ,stop_no as in_no , stop_name as in_name , i.stop_id as in_id from (select * from bus_stops where busno = 34567 ) as i join ( select * from stops where stop_name  = ':source' ) as s on i.stop_id = s.stop_id ) as x join (select busno ,stop_no as out_no , stop_name as out_name , j.stop_id as out_id from (select * from bus_stops where busno = 12345) as j join ( select * from stops where stop_name  = ':dest') as d on j.stop_id = d.stop_id ) as y on x.busno = y.busno ")
            inn = dropornot.in_no
            out = dropornot.out_no
            if(inn < out) :
                bus_details.append(inn)
                bus_details.append(out)
                bus_details.append(50 + bus_details[i][2]*bus_details[i][-3])
               #todo further work
                i += 1 
            else :
                bus_details.pop(i)

            


    except : print("no bus")
    
    return render_template('searchbus.html',formdetails = request.form,results = bus_details,stops = getStopsData())

        

# select *
# from ( select  *
# 	from (select * 
# 		from busses
# 		where busno in  (select busno
# 						 from bus_stops
# 						 where stop_id in (select stop_id 
# 										 from stops
# 										 where stops.stop_name = 'pune' or stops.stop_district = 'pune') 
# 						intersect 
# 						select busno 
# 						from bus_stops 
# 						where stop_id in (select stop_id 
# 										from stops 
# 										where stops.stop_name = 'mumbai' or stops.stop_district = 'mumbai' )
#         )) as q1 inner join (select * from bus_class where bclass = :busclass) as q5 on q1.bclass = q5.bclass
#     ) as q2 left outer join  
# (select * 
# from bus_object
# where bus_date = '10-08-2019') as q3
# on q2.busno = q3.bus_no 
