from flask import Flask, render_template, request, redirect, url_for
from list_items import List_Items
import random

app = Flask('__name__')
app.config['SECRET_KEY'] = 'SECRET_PROJECT'


lists= List_Items()
categories = {"todo":"To Do","complete":"Complete",}
random_item = []

COMP_ACTION = "Y"
UNCOMP_ACTION = "X"

@app.route('/')
def toDo():
  name= "gregor"

  return render_template("index.html", name=name, categories = categories)


@app.route("/<category>/<int:rand>", methods=["GET"])
def get_random(category,rand=0):
    list_items = lists.get_list_by_category(category)
    if rand == 1:
        global random_item
        random_item = random.choice(list_items)
    return redirect(url_for("items",category=category))

@app.route("/<category>", methods=["GET", "POST"])
def items(category):
  list_items = lists.get_list_by_category(category)

  if request.method == "POST":

    [(name, action)] = request.form.items()

    if action == COMP_ACTION:
      lists.complete(name)

    elif action == UNCOMP_ACTION:
      lists.uncomplete(name)


  return render_template("lists.html",category=category, categories=categories,list_items=list_items,random_item=random_item)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
