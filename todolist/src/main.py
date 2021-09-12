from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import csv
import os


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
    number = db.Column(db.Float, unique = False) #Steps placement
    complete = db.Column(db.Boolean, default=False, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return "Item ID: {}, Step ID: {}, Name: {}, Number: {}, Complete: {}".format(self.item_id, self.id, self.name, self.number, self.complete)


#Remove database each restart for testing
if os.path.exists('toDoListDB.db'):
  os.remove('toDoListDB.db')

db.create_all()


#Data for testing
with open("/usr/src/app/data.csv", "r") as csvfile:
    list_items = csv.reader(csvfile)
    id_counter = 0
    for row in list_items:
        id_counter=id_counter+1
        item = Item(id = id_counter,name = row[0], description = row[1], complete = False)
        db.session.add(item)
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
  return render_template("index.html", name=name, items_list=items_list, categories=categories)


#Main Categories Route
@app.route("/<category>", methods=["GET", "POST"])
def list(category):
  list_items = Item.query.filter(Item.complete == False)

  if request.method == "POST":

    [(name, action)] = request.form.items()

    if action == COMP_ACTION:
        Item.complete(name)

    elif action == UNCOMP_ACTION:
        Item.uncomplete(name)

    elif action == "Random":
        rand_items = lists.get_list_by_category("todo")
        global random_item
        random_item = random.choice(rand_items)
    elif action == "Edit":
        return redirect(url_for("item",name = name))
    elif action == "Add New Item":
        return redirect(url_for("add_item"))


  return render_template("lists.html",category=category, categories=categories,list_items=list_items,random_item=random_item)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
