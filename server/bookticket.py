from flask import Flask , render_template , Blueprint,request
from . import db

book = Blueprint('book',__name__)

@book.route('/bookticket/')
def render_bookticket():
    busno = int(request.args.get("busno"))
    source = request.args.get("source")
    dest = request.args.get("dest")
    jdate = request.args.get("jdate")

    SQL = " (select * from ( select * from busses where busno = :busno) as q1 join bus_stops on q1.bclass = bus_stops.bclass) as q2 right outer join   (select * from bus_object where bus_date = :jdate ) as q3 on q2.busno = q3.busno "

    results = db.session.execute(SQL,{'busno':busno,'source':source,'dest':dest,'jdate':jdate})
    render_template("bookingticket.html"results = results)


@book.route('/bookticket/',methods=["POST"])
def bookTicker():
    busno = int(request.data.get('busno'))
    bookSeats = request.data.get('seatsBooked')
    passDetails = request.data.get("passengers")