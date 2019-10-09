from flask import Flask , render_template , Blueprint,request
from . import db

book = Blueprint('book',__name__)

@book.route('/bookticket/')
def render_bookticket():
    busno = int(request.args.get("busno"))
    source = request.args.get("source")
    dest = request.args.get("dest")
    jdate = request.args.get("jdate")

    SQL = " select q2.busno , route , no_of_stops  , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc  from (select  busno , route, ratings , startat , endat , arr_time , dept_time , no_of_stops , class_name , no_of_seats , reserved , class_inc    from ( select *  from busses where busno = :busno) as q1 join bus_class on q1.bclass = bus_class.bclass) as q2 right outer join   (select  busno,bus_id , seats_occupied , bus_date  from bus_object where bus_date = :jdate ) as q3 on q2.busno = q3.busno "

    results = db.session.execute(SQL,{'busno':busno,'jdate':jdate})

    result2 = db.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :source)",{'source':source})
    result3 = db.session.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :dest)", {'dest':dest})
    bus_detail = []
    bus_detail = [ i for i in results.first()]
    bus_detail.append(result2.first()[0])
    bus_detailappend(result3.first()[0])
    bus_details.append(100 + (bus_detail[-1] - bus_detail[-2])*bus_detail[-3])
    in_time , outtime  = getTimes(bus_detail.pop(3),bus_detail.pop(4),inn,out,bus_detail.pop(2))
    bus_detail.append(intime)
    bus_detail.append(outtime)


    render_template("bookingticket.html"results = results)


@book.route('/bookticket/',methods=["POST"])
def bookTicket():
    busno = int(request.data.get('busno'))
    bookSeats = request.data.get('seatsBooked')
    passDetails = request.data.get("passengers")
    source = request.data.get('source')
    dest = request.data.get('dest')

    SQL = " select q2.busno , route , no_of_stops  , arr_time , dept_time , class_name  ,no_of_seats , reserved , bus_date , seats_occupied , class_inc  from (select  busno , route, ratings , startat , endat , arr_time , dept_time , no_of_stops , class_name , no_of_seats , reserved , class_inc    from ( select *  from busses where busno = :busno) as q1 join bus_class on q1.bclass = bus_class.bclass) as q2 right outer join   (select  busno,bus_id , seats_occupied , bus_date  from bus_object where bus_date = :jdate ) as q3 on q2.busno = q3.busno "

    result = db.esecute(SQL,{'busno':busno,'jdate':jdate})

     result2 = db.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :source)",{'source':source})
    result3 = db.session.execute(" select stop_no from bus_stops where stop_id = ( select stop_id from stops where stop_name = :dest)", {'dest':dest})
    bus_detail = []
    bus_detail = [ i for i in results.first()]
    price  = 100 + (result3.first()[0] - result2.first()[0])*bus_detail[-1]
    TotalCost = len(bookSeats)*price




