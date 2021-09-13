from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import csv
import os
from forms import AddItemForm, AddStepForm
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toDoListDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

categories = {"todo":"To Do","complete":"Complete",}


random_item = []

#Actions
COMP_ACTION = "Y"
UNCOMP_ACTION = "X"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    description = db.Column(db.String(200), unique = False) #a review's text
    #category = ##Items tags
    complete = db.Column(db.Boolean, default=False, nullable=False)
    snoozed = db.Column(db.Boolean, default=False, nullable=False)
    steps = db.relationship('Step', backref='item', lazy = 'dynamic', cascade = "all, delete, delete-orphan")

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


#Remove database each restart for testing
#f os.path.exists('toDoListDB.db'):
#  os.remove('toDoListDB.db')

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



#Main url to redirect to login page
@app.route('/')
def toDo():
  name= "gregor"
  items_list = Item.query.all()
  print(items_list)
  #return render_template("index.html", name=name, items_list=items_list, categories=categories)
  return redirect(url_for('list', category='todo'))


#Main Categories Route
@app.route("/<category>", methods=["GET", "POST"])
def list(category):
    if category == "todo":
        list_items = Item.query.filter(Item.complete == False)
    elif category == "complete":
        list_items = Item.query.filter(Item.complete == True)
    else:
        list_items = Item.query.all()

    if request.method == "POST":
        global random_item
        [(name, action)] = request.form.items()

        #Item table actions
        if action == COMP_ACTION:
            item = Item.query.get(name)
            item.complete = True
            db.session.commit()
        elif action == UNCOMP_ACTION:
            item = Item.query.get(name)
            item.complete = False
            db.session.commit()
        elif action == "Edit":
            return redirect(url_for("item",item_id = name))

        #Random item actions
        elif action == "Random":
            rand_items = Item.query.filter(Item.snoozed == False, Item.complete == False).all()
            random_item = random.choice(rand_items)
        elif action == "Snooze":
            item = Item.query.get(name)
            item.snoozed = True
            db.session.commit()
            rand_items = Item.query.filter(Item.snoozed == False, Item.complete == False).all()
            random_item = random.choice(rand_items)
        elif action == "Reset Snooze":
            snoozed_items = Item.query.filter(Item.snoozed == True).all()
            for item in snoozed_items:
                item.snoozed = False
                db.session.commit()

        #Other actions
        elif action == "Add New Item":
            return redirect(url_for("add_item"))
    return render_template("lists.html",category=category, categories=categories,list_items=list_items,random_item=random_item)


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item(item_id):
    item = Item.query.get(item_id)

    if request.method == "POST":

       [(name, action)] = request.form.items()

       #Item Actions
       if action == "Complete Item":
           item = Item.query.get(name)
           item.complete = True
           db.session.commit()
       elif action == "Uncomplete Item":
           item = Item.query.get(name)
           item.complete = False
           db.session.commit()
       elif action == "Delete":
           item = Item.query.get(name)
           db.session.delete(item)
           db.session.commit()
           return redirect(url_for("list",category = "todo"))
       #Step Actions
       elif action == "Y":
           step = Step.query.get(name)
           step.complete = True
           db.session.commit()
       elif action == "X":
           step = Step.query.get(name)
           step.complete = False
           db.session.commit()
       elif action == "DEL":
           step = Step.query.get(name)
           db.session.delete(step)
           db.session.commit()

    return render_template("items.html", categories=categories,item=item, add_step = AddStepForm())

@app.route("/add_item", methods=["GET", "POST"])
def add_item():

    return(render_template("add_item.html",categories=categories, add_item = AddItemForm()))

@app.route("/add_item_submit", methods=["POST"])
def add_item_submit():
    add_item_form = AddItemForm()
    if add_item_form.validate_on_submit():

        item = Item(name = add_item_form.name.data, description = add_item_form.description.data)
        db.session.add(item)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
    return(redirect(url_for("list",category = "todo")))

@app.route("/<item_id>/add_step_submit", methods=["POST"])
def add_step_submit(item_id):
    add_step_form = AddStepForm()
    if add_step_form.validate_on_submit():

        item = Item.query.get(item_id)
        steps_count = len(item.steps.all()) + 1
        step = Step(name = add_step_form.name.data, number = steps_count, item_id = item_id)
        db.session.add(step)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
    return(redirect(url_for("item",item_id = item_id)))

if __name__ == '__main__':
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
