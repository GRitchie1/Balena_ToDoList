#Installed
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import AddItemForm, AddStepForm, EditItemForm
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

categories = {"todo":"To Do","complete":"Complete","prioritised":"Prioritised","timed":"Timed"}


random_item = { 'name': ''}


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
    elif category == "prioritised":
        list_items = Item.query.filter(Item.complete == False).order_by(Item.priority)
    elif category == "timed":
        list_items = Item.query.filter(Item.complete == False)
    else:
        list_items = Item.query.all()

    if request.method == "POST":
        global random_item
        [(name, action)] = request.form.items()

        #Item table actions
        if action == "Complete":
            item = Item.query.get(name)
            item.complete = True
            db.session.commit()
        elif action == "Uncomplete":
            item = Item.query.get(name)
            item.complete = False
            db.session.commit()
        elif action == "Open":
            return redirect(url_for("item",item_id = name))

        #Random item actions
        elif action == "Random":
            rand_items = Item.query.filter(Item.snoozed == False, Item.complete == False).all()
            if len(rand_items) > 0:
                random_item = random.choice(rand_items)
            else:
                random_item = { 'name': ''};
        elif action == "Snooze":
            item = Item.query.get(name)
            item.snoozed = True
            item.snooze_count = item.snooze_count + 1
            db.session.commit()
            rand_items = Item.query.filter(Item.snoozed == False, Item.complete == False).all()
            if len(rand_items) > 0:
                random_item = random.choice(rand_items)
            else:
                random_item = { 'name': ''};
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
       if action == "Complete":
           item = Item.query.get(name)
           item.complete = True
           db.session.commit()
       elif action == "Uncomplete":
           item = Item.query.get(name)
           item.complete = False
           db.session.commit()
       elif action == "Edit":
           return redirect(url_for("edit_item",item_id = name))
       #Step Actions
       elif action == "Y":
           step = Step.query.get(name)
           step.complete = True
           db.session.commit()
       elif action == "X":
           step = Step.query.get(name)
           step.complete = False
           db.session.commit()

    return render_template("items.html", categories=categories,item=item, steps = Step.query.filter(Step.item_id == item.id).order_by(Step.number),add_step = AddStepForm())


#Add Items
@app.route("/add_item", methods=["GET", "POST"])
def add_item():

    return(render_template("add_item.html",categories=categories, add_item = AddItemForm()))

@app.route("/add_item_submit", methods=["POST"])
def add_item_submit():
    add_item_form = AddItemForm()
    if add_item_form.validate_on_submit():

        if add_item_form.priority.data > 99:
            priority = 99
        elif add_item_form.priority.data < 0:
            priority = 0
        else:
            priority = add_item_form.priority.data

        item = Item(name = add_item_form.name.data, description = add_item_form.description.data, priority = priority)
        db.session.add(item)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        return(redirect(url_for("list",category = "todo")))


#Edit Items
@app.route("/edit_item/<item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get(item_id)
    if request.method == "POST":
        [(name, action)] = request.form.items()

        #Item Actions
        if action == "Complete":
            item = Item.query.get(name)
            item.complete = True
            db.session.commit()
        elif action == "Uncomplete":
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
        elif action == "DOWN":                        #Increase number, but move down list
            up_step = Step.query.get(name)
            item = Item.query.get(up_step.item_id)
            down_step = up_step
            for step in item.steps:
                if step.number == up_step.number + 1:
                    down_step = step
            down_step.number = down_step.number - 1
            up_step.number = up_step.number + 1
            db.session.commit()
        elif action == "UP":                      #Decrease number but move up list
            down_step = Step.query.get(name)
            item = Item.query.get(down_step.item_id)
            up_step = down_step
            for step in item.steps:
                if step.number == down_step.number - 1:
                    up_step = step
            down_step.number = down_step.number - 1
            up_step.number = up_step.number + 1
            db.session.commit()

    return(render_template("edit_item.html",categories=categories, item=item, steps = Step.query.filter(Step.item_id == item.id).order_by(Step.number), edit_item = EditItemForm(name=item.name,description=item.description,priority=item.priority), add_step = AddStepForm()))

@app.route("/<item_id>/edit_item_submit", methods=["POST"])
def edit_item_submit(item_id):
    edit_item_form = EditItemForm()
    #Fix
    if edit_item_form.validate_on_submit():
        item = Item.query.get(item_id)
        item.name = edit_item_form.name.data
        item.description = edit_item_form.description.data

        if edit_item_form.priority.data > 99:
            item.priority = 99
        elif edit_item_form.priority.data < 0:
            item.priority = 0
        else:
            item.priority = edit_item_form.priority.data
        db.session.commit()
    return(redirect(url_for("item",item_id = item_id)))



#Add Steps
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
    return(redirect(url_for("edit_item",item_id = item_id)))



#Start server
if __name__ == '__main__':
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
