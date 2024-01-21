from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, time
import json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class ActivityRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    distance = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    time = db.Column(db.Time, nullable=False)
    comment = db.Column(db.String(350))


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('records_get'))

@app.get('/records')
def records_get():
    all_records = ActivityRecord.query.all()
    list_of_records = []
    
    for record in all_records:
        record_dict = {
            'id': record.id, 'date': record.date.strftime('%d-%m-%Y'),
            'distance': record.distance, 
            'time': record.time.strftime('%H:%M:%S'),
            'comment': record.comment
        }
        list_of_records.append(record_dict)
    return list_of_records

@app.post('/records')
def records_post():
    date_arguments = request.json['date'].split('-')
    time_arguments = request.json['time'].split(':')
    date_arguments = [int(i) for i in date_arguments]
    time_arguments = [int(i) for i in time_arguments]  
    request_date = date(date_arguments[0],date_arguments[1],date_arguments[2])
    request_time = time(time_arguments[0],time_arguments[1],time_arguments[2])
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