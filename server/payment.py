from flask import Flask , render_template , Blueprint , request ,url_for ,redirect , make_response 
from . import db
import time
from uuid import uuid4
import json
import time

pay = Blueprint('pay',__name__)


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


@pay.route('/paymentpage')
def render_paymentPage() :
    return render_template('payment.html')


@pay.route('/ackticket',methods=['GET'])
def render_ticket() : 

    tid = request.args.get("tid")
    data = request.cookies.get("data")
    data = json.loads(data)
    uid = data['uid']
    name = data['name']

    print(tid)
    
    if uid == None :
        return redirect(url_for("render_login"))

    result1 = db.session.execute("select * from transactions where transaction_id = :tid", {'tid':tid})

    transaction = result1.fetchall()
    
    if  len(transaction) == 0 :
        msg = "no transactions made"
        return render_template('ticketresult.html', tickets = [] , transaction = [], username = name)

    else :

        tickets = db.session.execute("select fare ,pass_name , ticket_no , seat_no , journeyto ,journeyfrm , busno , bus_date  from (select * from ((select fare , ticket_no , pass_id from tickets where transaction_id = :tid) as q1" + 
        " join (select pass_name , bus_id , seat_no , journeyfrm , journeyto , pass_id from bus_passengers ) as q2 " +
        "on q1.pass_id = q2.pass_id ) as q3  join bus_object  on bus_object.bus_id = q3.bus_id) as q5 ",{'tid' : tid})

        tickets = [ [i for i in r] for r in tickets]
        # print(tickets)

        for ticket in tickets:

            (inn,) = db.session.execute("select stop_no from bus_stops where bs_id = :bs",{'bs':ticket[-3]}).first()
            (outt,) = db.session.execute("select stop_no from bus_stops where bs_id = :bs",{'bs':ticket[-4]}).first()

            (busno,route,no_of_stops , a ,d ,bclass) = db.session.execute("select busno , route , no_of_stops  , arr_time , dept_time , bclass  from busses where busno = :busno",{'busno': ticket[-2]}).first()

            intime , outtime = getTimes(a,d,inn,outt,no_of_stops)
            (source,) = db.session.execute("select stop_name  from stops where stop_id = (select stop_id from bus_stops where bs_id = :bs)",{'bs': ticket[-3]}).first()
            (dest,) = db.session.execute("select stop_name from stops where stop_id = (select stop_id from bus_stops where bs_id = :bs)",{'bs': ticket[-4]}).first()

            ticket.pop(-3)
            ticket.pop(-3)

            ticket.append(source)
            ticket.append(dest)
            ticket.append(route)
            ticket.append(bclass)
            ticket.append(intime)
            ticket.append(outtime)
            
    print(tickets[0])
    print(transaction)
    print()
    return render_template('ticketresult.html', tickets = tickets , transaction = transaction[0]  , username = name)


@pay.route('/pay',methods=['GET'])
def render_payment() :

    data = request.cookies.get("data")
    data = json.loads(data)
    uid = data['uid']
    name = data['name']

    if uid == None :
        return redirect(url_for("render_login"))

    busno = data['busno']
    jdata = data['jdate']

    if busno == None : 
        return redirect(url_for('render_searchbus',msg = 'select bus first'))

    return render_template('payment.html' , username = name)

@pay.route('/pay',methods=['POST'])
def payment() : 

    data = request.cookies.get("data")
    data = json.loads(data)
    uid = data.get('uid')

    if uid == None :
        return redirect(url_for("render_user"))

    busno = data.get('busno')
    jdate = data.get('jdate')
    source = data.get('source')
    dest = data.get('dest')

    cardDetails = request.form

    detail  = db.session.execute("select * from temp_pass where uid = :uid and bus_id = :busno",{'uid':uid , 'busno' : busno})

    details = detail.fetchall()

    result2 = db.session.execute(" select bs_id from bus_stops where stop_id = ( select stop_id from stops where stop_name = :source) and busno = :busno",{'source':source , 'busno' : busno})

    result3 = db.session.execute(" select bs_id from bus_stops where stop_id = ( select stop_id from stops where stop_name = :dest) and busno = :busno", {'dest':dest , 'busno' : busno})

    (s_bs,) = result2.first()
    (d_bs,) = result3.first()

    bus_data = db.session.execute("select * from bus_object where busno = :busno and bus_date = :jdate", {'busno' : busno , 'jdate' : jdate}).fetchall()

    if len(bus_data) == 0 :

        bus_id = uuid4().int%123456789
        db.session.execute("insert into bus_object values(:bus_id , :busno , :jdate , :seats)", {'bus_id' : bus_id , 'busno' : busno , 'jdate' : jdate , 'seats' : [] })

    pass_ids = []
    for detail in details :

        print(detail)
        db.session.execute("update bus_object set seats_occupied = array_append(seats_occupied , :seat ) where bus_id = :bus_id",{'bus_id' : bus_id , 'seat' : detail[3] })

        pass_id = uuid4().int%123456789
        pass_ids.append([pass_id , detail[-3]])
        db.session.execute("insert into bus_passengers values(:pass_id,:bus_id,:pass_name,:seat_no,:journeyfrm,:journeyto, :age , :gender )",{'bus_id': bus_id , 'pass_id' : pass_id, 'pass_name': detail[2] ,'seat_no': detail[3], 'journeyfrm' : s_bs , 'journeyto' : d_bs , 'age': detail[-2] ,'gender' : detail[-1] })

    tid = uuid4().int%123456789
    totalFare = sum( pass_id[1] for pass_id in pass_ids)
    db.session.execute(" insert into transactions values(:tid , :uid , :total , :date)", { 'tid' : tid , 'uid' : uid , 'total' : totalFare , 'date' : time.strftime('%d-%m-%Y')})

    for pass_id in pass_ids :
        tno = uuid4().int%123456789
        db.session.execute("insert into tickets values(:tno , :pass_id , :fare , :tid )", { 'tno' : tno , "tid" : tid , "pass_id" : pass_id[0] , "fare" : pass_id[1] })


    db.session.execute('delete from temp_pass where bus_id = :busno and uid = :uid and  jdate = :jdate' , { 'jdate' : jdate , 'busno' : busno , 'uid' : uid})

    db.session.commit()

    return redirect(url_for('pay.render_ticket', tid = tid))


@pay.route('/paypage',methods=['GET'])
def payment_op() : 
    return render_template('ticketresult.html')

# for passenger in passDetails :

#     busData = db.session.execute("select * from bus_object where busno = :busno and bus_date = :jdate", {'busno' : busno , 'jdate' : jdate}).fetchall()
#     print(busData)
#     if len(busData) == 0 :

#         busId = 3
#         db.session.execute("insert into bus_object values(:bus_id , :busno , :jdate , :seats)", {'bus_id' : busId , 'busno' : busno , 'jdate' : jdate , 'seats' : [int(passenger["seat_no"])] })
    
#     else : 

#         busId = int(busData[0][0])
#         db.session.execute("update bus_object set seats_occupied = array_append(seats_occupied , :seat ) where bus_id = :bus_id",{'bus_id' : busId , 'seat' : int(passenger["seat_no"])})
        

#     db.session.execute("insert into bus_passengers values(:pass_id,:bus_id,:pass_name,:seat_no,:journeyfrm,:journeyto)",{'bus_id': busId , 'pass_id' : i, 'pass_name': passDetails[0]['name'] ,'seat_no': int( passenger['seat_no']) , 'journeyfrm' : s_bs , 'journeyto' : d_bs})
#     i += 1


# db.session.execute(" insert into transactions values(:tid , :uid , :total)", { 'tid' : 1 , 'uid' : uid , 'total' : 1})

# for passenger in passDetails :

#     db.session.execute("insert into tickets values(:tno , :pass_id , :fare , :tid )", {"tid" : tid , "pass_id" : 1 , "fare" : fare })
    
# db.session.commit()

# result2 = db.execute(" select stop_no , bs_id from bus_stops where stop_id = ( select stop_id from stops where stop_name = :source)",{'source':source})

# result3 = db.session.execute(" select stop_no  , bs_id from bus_stops where stop_id = ( select stop_id from stops where stop_name = :dest)", {'dest':dest})

# (s_no , s_bs) = result2.first()
# (d_no , d_bs) = result3.first()
