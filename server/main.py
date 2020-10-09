from flask import Flask,render_template,Blueprint,request,json,Response
from . import db
import time


main = Blueprint('main',__name__)

def getTimes(arr,dept,inn,out,nos) :

    arr = list(map(int,arr.split(':')))
    dept = list(map(int,dept.split(':')))

    arr =  arr[1]*60*1000 + arr[0]*60*60*1000
    dept = dept[1]*60*1000 + dept[0]*60*60*1000

    if(dept < arr) :
        arr = 1000*60*60*24 - arr
        tTime = arr + dept
    else :
        tTime = dept - arr
    st = tTime//nos
    in_time = st*inn//1000
    out_time = st*out//1000

    in_time = "" + str(in_time//3600)  + ':' + str((in_time%3600)//60)
    out_time = "" + str(out_time//3600) + ':' + str((out_time%3600)//60)

    return in_time , out_time



def getStopsData() :
    stops = db.session.execute("select stop_name from stops")
    stops_data = [str(r[0]) for r in stops]
    return json.dumps(stops_data)


@main.route("/")
def render_home() :
    msg  = request.args.get('msg')
    data = request.cookies.get('data')
    if(data == None) :
        username = None
    else :

        data = json.loads(data)
        username = data['name']

    return render_template('index.html', stops = getStopsData(),msg = msg , username = username)


@main.route("/searchbus/",methods=['GET'])
def render_searchBus() :
    msg  = request.args.get('msg')
    data = request.cookies.get('data')
    if(data == None) :
        username = None
    else :
        data = json.loads(data)
        username = data['name']

    msg = "HAPPY JOURNEY"

    return render_template("searchbus2.html",stops = getStopsData(), results = [],formdetails = None,msg = msg  , username = username)


@main.route("/searchbus/",methods=['POST'])
def searchBus() :

    data  = request.cookies.get('data')
    if(data == None) :
        
        username = None
    else :

        data = json.loads(data)
        username = data['name']

    source = request.form['source']
    dest = request.form['dest']
    jdate = request.form['jdate']
    bus_class = request.form['bus_class']

    SQL_final = "select q2.busno , route , no_of_stops  , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc , ratings from ( select  busno , route , no_of_stops , q1.bclass , arr_time , dept_time , class_name  ,no_of_seats , reserved , class_inc , ratings from (select busno , route , no_of_stops , bclass , arr_time , dept_time , ratings from busses where busno in  (select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :source) intersect select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :dest ) ) ) as q1 inner join bus_class on q1.bclass = bus_class.bclass ) as q2 left outer join (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno "
    SQL_final2 = "select q2.busno , route , no_of_stops , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc , ratings from ( select  busno , route , no_of_stops , q1.bclass , arr_time , dept_time , class_name  ,no_of_seats , reserved , class_inc , ratings from (select busno , route , no_of_stops , bclass , arr_time , dept_time , ratings from busses where busno in  (select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :source) intersect select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :dest ) ) ) as q1 inner join (select * from bus_class where bclass = :busclass) as q4  on q1.bclass = q4.bclass ) as q2 left outer join (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno "

    if bus_class  != "ANY" :
        results = db.session.execute(SQL_final2,{'source':source ,'dest':dest,'jdate':jdate ,'busclass' : bus_class})

    else :
        results = db.session.execute(SQL_final,{'source':source ,'dest':dest,'jdate':jdate})

    
    bus_details = [ [i for i in r] for r in results]
    
    # try :
    i = 0 
    while i < len(bus_details) :
        dropornot = db.session.execute("select x.in_no , y.out_no from (select busno ,stop_no as in_no , stop_name as in_name , i.stop_id as in_id from (select * from bus_stops where busno = :busno ) as i join ( select * from stops where stop_name  = :source ) as s on i.stop_id = s.stop_id ) as x join (select busno ,stop_no as out_no , stop_name as out_name , j.stop_id as out_id from (select * from bus_stops where busno = :busno) as j join ( select * from stops where stop_name  = :dest) as d on j.stop_id = d.stop_id ) as y on x.busno = y.busno ",{'busno':bus_details[i][0],'source':source,'dest':dest})
        [inn,out] = [ i for i in dropornot.first()]
        if(inn < out) :
            bus_details[i].append(inn)
            bus_details[i].append(out)
            bus_details[i].append(100 + (bus_details[i][-1] - bus_details[i][-2])*bus_details[i][-4])
            intime , outtime  = getTimes(bus_details[i].pop(3),bus_details[i].pop(3),inn,out,bus_details[i].pop(2))
            if jdate == '20' + time.strftime('%y-%m-%d')  : 
                curTime = time.strftime('%X')[0:5]
                curTime = list(map(int,curTime.split(':')))
                if not  int(intime.split(':')[0]) > curTime[0]  : 
                    bus_details.pop(i)
                    continue
                    
            bus_details[i].append(intime)
            bus_details[i].append(outtime)
            i += 1 
        else :
            bus_details.pop(i)
    if len(bus_details) == 0 :
        msg = 'Sorry No Bus Available '
    else :
        msg = ''

    return render_template('searchbus2.html',formdetails = request.form,results = bus_details , stops = getStopsData(),msg  = msg , username = username)
    # except Exception as e: 
    #     print("new exception : ",e)
    #     return render_template('searchbus2.html',formdetails=request.form,results=[],stops=getStopsData())
    

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
