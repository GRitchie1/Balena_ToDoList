#From my files
from __main__ import db
#Builtin
from datetime import datetime

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
