from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from datetime import date, time
import json
from werkzeug.exceptions import HTTPException
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class ActivityRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    distance = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    time = db.Column(db.Time, nullable=False)
    comment = db.Column(db.String(350), nullable=True)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('records_get'))

@app.get('/records')
def records_get():
    all_records = ActivityRecord.query.order_by(desc(ActivityRecord.date)).all()
    list_of_records = []
    
    for record in all_records:
        record_dict = {
            'id': record.id,
            'date': record.date.strftime('%d-%m-%Y'),
            'distance': record.distance, 
            'time': record.time.strftime('%Hh %Mmin %Ss'),
            'comment': record.comment
        }
        list_of_records.append(record_dict)
    return list_of_records

@app.post('/records')
def records_post():
    try:
        date_arguments = request.json['date'].split('-')
        time_arguments = request.json['time'].split(':')
        formatTime(time_arguments)
        date_arguments = [int(i) for i in date_arguments]
        time_arguments = [int(i) for i in time_arguments]
        request_date = date(date_arguments[0],date_arguments[1],date_arguments[2])
        request_time = time(time_arguments[0],time_arguments[1],time_arguments[2])
    except:
        exception = HTTPException()
        exception.code = 400
        exception.description = "Bad Request"
        return handle_exception(exception)
    else:
        new_record = ActivityRecord(
            date=request_date,
            distance=request.json['distance'],
            time=request_time,
            comment=request.json['comment'])
        db.session.add(new_record)
        db.session.commit()
        return {'201': 'Created'}

@app.route('/records/<id>', methods=['DELETE'])
def delete(id):
    record = ActivityRecord.query.get(id)
    if not record:
        exception = HTTPException()
        exception.code = 404
        exception.description = "Resource not found"
        return handle_exception(exception)
    else:
        db.session.delete(record)
        db.session.commit()
        return {'200': 'OK'}

@app.route('/summary', methods=['GET'])
def summary():
    summary_info = db.session.query(
        func.count(ActivityRecord.id),
        func.sum(ActivityRecord.distance),
        3600 * func.sum(func.strftime('%H',ActivityRecord.time))
        +
        60 * func.sum(func.strftime('%M', ActivityRecord.time))
        +
        func.sum(func.strftime('%S', ActivityRecord.time)),
        ).all()
    summary_info = list(summary_info)
    return {
        'number_of_days': summary_info[0][0],
        'total_distance': summary_info[0][1],
        'total_time': summary_info[0][2],
    }

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description
    })
    response.content_type = 'application/json'
    return response


def formatTime(timeString):
    for i in range(0,len(timeString)):
        if(timeString[i] == ''):
            timeString[i]= '00'
        if(int(timeString[i]) < 0):
            timeString[i] = 0
    