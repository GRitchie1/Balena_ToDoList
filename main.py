from flask import Flask, render_template, request, redirect, url_for
from list_items import List_Items

app = Flask('__name__')
app.config['SECRET_KEY'] = 'SECRET_PROJECT'


lists= List_Items()
categories = {"todo":"To Do","complete":"Complete",}

COMP_ACTION = "Y"
UNCOMP_ACTION = "X"

@app.route('/')
def toDo():
  name= "gregor"

  return render_template("index.html", name=name, categories = categories)


@app.route("/<category>", methods=["GET", "POST"])
def locations(category):
  list_items = lists.get_list_by_category(category)

  if request.method == "POST":
    
    [(name, action)] = request.form.items()

    if action == COMP_ACTION:
      lists.complete(name)
      
    elif action == UNCOMP_ACTION:
      lists.uncomplete(name)
  
  return render_template("lists.html",category=category, categories=categories,list_items=list_items)



app.run(host='0.0.0.0', port=8080)