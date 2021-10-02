#Installed
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer

#Builtin
from datetime import datetime
import random
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/toDoListDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

TESTMODE = False;

def import_data():
    #Remove database each restart for testing
    if os.path.exists('/data/toDoListDB.db'):
        os.remove('/data/toDoListDB.db')

    db.create_all() #Create database - initialise tables

    #Data for testing
    with open("/usr/src/app/data.csv", "r") as csvfile:
        list_items = csv.reader(csvfile)
        id_counter = 0
        for row in list_items:
            id_counter=id_counter+1
            for i in range(len(row)):
                if row[i]=="TRUE":
                    row[i]= True
                elif row[i]=="FALSE":
                    row[i] = False


            item = Item(id = id_counter, name = row[1], description = row[2], complete = row[3], snoozed = row[4], snooze_count = row[5], priority= row[6], due_time = datetime.strptime(row[7], '%d/%m/%Y %H:%M'))
            step = Step(name= "Step 1", number = 1, item_id = id_counter)
            print(item)
            db.session.add(item)
            db.session.add(step)
            try:
                db.session.commit()
                print("success")
            except Exception:
                print("fail")
                db.session.rollback()

def export_data():
    with open('/usr/src/app/export.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        list_items = Item.query.all()
        output = []
        for item in list_items:
            output.append([item.id, item.name, item.description, item.complete, item.snoozed, item.snooze_count, item.priority, item.due_time])
        writer.writerows(output)


#Start server
if __name__ == '__main__':
    import routes
    from models import Item, Step

    if TESTMODE:
        import_data()


    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
