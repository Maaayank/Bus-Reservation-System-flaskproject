from flask import Flask , render_template , Blueprint,request,jsonify ,redirect , url_for , make_response
from . import db
import json

book = Blueprint('book',__name__)

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



@book.route('/bookticket/',methods=['GET'])
def render_bookticket():

    data = request.cookies.get("data")

    if(data == None) :
        return redirect(url_for("auth.render_login" , msg = "Login required"))

    data = json.loads(data)

    uid  = data['uid']

    if uid == None :
        return redirect(url_for("auth.render_login",msg =  "Login Required") )

    username  = data['name']

    busno = int(request.args.get("busno"))
    source = request.args.get("source")
    dest = request.args.get("dest")
    jdate = request.args.get("jdate")

    SQL = "select q2.busno , route , no_of_stops  , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc  from (select  busno , route, ratings , startat , endat , arr_time , dept_time , no_of_stops , class_name , no_of_seats , reserved , class_inc    from ( select *  from busses where busno = :busno) as q1 join bus_class on q1.bclass = bus_class.bclass) as q2 left outer join   (select  busno,bus_id , seats_occupied , bus_date  from bus_object where bus_date = :jdate ) as q3 on q2.busno = q3.busno "

    results = db.session.execute(SQL,{'busno':busno,'jdate':jdate})
    print(busno,source,dest,jdate)
    
    result2 = db.session.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :source)",{'source':source})
    result3 = db.session.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :dest)", {'dest':dest})
    bus_detail = []
    bus_detail = [ i for i in results.first()]
    bus_detail.append(result2.first()[0])
    bus_detail.append(result3.first()[0])
    bus_detail.append(100 + (bus_detail[-1] - bus_detail[-2])*bus_detail[-3])
    print(bus_detail)
    intime , outtime  = getTimes(bus_detail.pop(3),bus_detail.pop(3),bus_detail[-3],bus_detail[-2],bus_detail.pop(2))
    bus_detail.append(intime)
    bus_detail.append(outtime)
    print("henlo" , bus_detail)

    resp = make_response(render_template("bookticket.html" ,card = bus_detail , username = username))

    data['busno'] = busno
    data['jdate'] = jdate
    data['source'] = source
    data['dest'] = dest
    resp.set_cookie('data',json.dumps(data))
    return resp



@book.route('/bookticket/',methods=["POST"])
def bookTicket():

    data = request.cookies.get("data")
    data = json.loads(data)
    uid = data.get('uid')
    busno = data.get('busno')
    jdate = data.get('jdate')
    source = data.get('source')
    dest =  data.get('dest')
    if uid == None :
        return redirect(url_for("render_user"),msg ='Login First' )

    detail = request.get_json(force = True)

    passDetails = detail.get("passengers")

    print(busno,passDetails)

    SQL = "select q2.busno , route , no_of_stops  , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc  from (select  busno , route, ratings , startat , endat , arr_time , dept_time , no_of_stops , class_name , no_of_seats , reserved , class_inc    from ( select *  from busses where busno = :busno) as q1 join bus_class on q1.bclass = bus_class.bclass) as q2 left outer join   (select  busno,bus_id , seats_occupied , bus_date  from bus_object where bus_date = :jdate ) as q3 on q2.busno = q3.busno "

    result = db.session.execute(SQL,{'busno':busno,'jdate':jdate})

    bus_detail = []
    bus_detail = [i for i in result.first()]

    result2 = db.session.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :source) and busno = :busno",{'source':source , 'busno': busno})

    result3 = db.session.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :dest) and busno = :busno", {'dest':dest, 'busno': busno})

    (s_no,) = result2.first()
    (d_no,) = result3.first()

    print(d_no,s_no)
    print(type(bus_detail[-1]))
    fare  = 100 + (d_no - s_no)*bus_detail[-1]

    for passs in passDetails :
        db.session.execute("insert into temp_pass (bus_id,pass_name,seat_no,journeyfrm,journeyto,uid,jdate,fare,age,gender) values(:bus_id,:name,:sno,:jfrm , :jto,:uid,:jdate,:fare,:age,:gen)",{'bus_id' : bus_detail[0],'name':passs['name'],'sno':passs['sno'],'jfrm':source,'jto':dest,'jdate':jdate,'fare':fare,'age':passs['age'],'gen':passs['gender'] , 'uid' : uid})
    db.session.commit()
    return jsonify({'msg' : 'successful'}), 200
