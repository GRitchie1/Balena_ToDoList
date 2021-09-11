from flask import Flask, render_template, request, redirect, url_for
from list_items import List_Items
import random

app = Flask('__name__')
app.config['SECRET_KEY'] = 'SECRET_PROJECT'


lists= List_Items()
categories = {"todo":"To Do","complete":"Complete",}
random_item = []


#Main url to redirect to login page
@app.route('/')
def toDo():
  name= "gregor"

  return render_template("index.html", name=name, categories = categories)



#Main Categories Route
@app.route("/<category>", methods=["GET", "POST"])
def list(category):
  list_items = lists.get_list_by_category(category)

  if request.method == "POST":

    [(name, action)] = request.form.items()

    if action == "Y":
        lists.complete(name)

    elif action == "X":
        lists.uncomplete(name)

    elif action == "Random":
        rand_items = lists.get_list_by_category("todo")
        global random_item
        random_item = random.choice(rand_items)
    elif action == "Edit":
        return redirect(url_for("item",name = str(name)))


  return render_template("lists.html",category=category, categories=categories,list_items=list_items,random_item=random_item)

@app.route("/item/<name>", methods=["GET", "POST"])
def item(name):
    item_index = lists.get_index_by_name(name)
    item = lists.get_item_by_index(item_index)
    return render_template("items.html", categories=categories,item=item)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
