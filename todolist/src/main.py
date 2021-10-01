#Installed
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer

#Builtin
from datetime import datetime
import random
import csv
import os


TESTMODE = False;

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/toDoListDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    description = db.Column(db.String(200), unique = False) #a review's text
    #category = ##Items tags
    complete = db.Column(db.Boolean, default=False, nullable=False)
    snoozed = db.Column(db.Boolean, default=False, nullable=False)
    steps = db.relationship('Step', backref='item', lazy = 'dynamic', cascade = "all, delete, delete-orphan")
    snooze_count = db.Column(db.Integer, default=0)
    priority = db.Column(db.Integer, unique = False, default=0) #Steps placement
    due_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "Item ID: {}, Name: {}, Description: {}, Snoozed: {}, Complete: {}".format(self.id, self.name, self.description, self.snoozed, self.complete)

class Step(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    number = db.Column(db.Integer, unique = False) #Steps placement
    complete = db.Column(db.Boolean, default=False, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return "Item ID: {}, Step ID: {}, Name: {}, Number: {}, Complete: {}".format(self.item_id, self.id, self.name, self.number, self.complete)

if TESTMODE:
    #Remove database each restart for testing
    if os.path.exists('/data/toDoListDB.db'):
      os.remove('/data/toDoListDB.db')

db.create_all() #Create database - initialise tables

if TESTMODE:
    #Data for testing
    with open("/usr/src/app/data.csv", "r") as csvfile:
        list_items = csv.reader(csvfile)
        id_counter = 0
        for row in list_items:
            id_counter=id_counter+1
            item = Item(id = id_counter, name = row[0], description = row[1], complete = False)
            step = Step(name= "Step 1", number = 1, item_id = id_counter)
            db.session.add(item)
            db.session.add(step)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


#Start server
if __name__ == '__main__':
    import routes
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
