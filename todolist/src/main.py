#Installed
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer

#Builtin
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
            item = Item(id = id_counter, name = row[0], description = row[1], complete = False)
            step = Step(name= "Step 1", number = 1, item_id = id_counter)
            db.session.add(item)
            db.session.add(step)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()

def export_data():
    with open('/usr/src/app/export.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        list_items = Item.query.all()
        output = []
        for item in list_items:
            output.append([item.name, item.description, item.complete])
        writer.writerows(output)


#Start server
if __name__ == '__main__':
    import routes
    from models import Item, Step

    if TESTMODE:
        import_data()


    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
