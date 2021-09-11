import csv

class List_Items:
    def __init__(self):
        self.list_items = []
        self.load_data()

    def add(self, name, description, category):
        if name is not None and description is not None and category is not None:
            list_item = Item(name, description, category)
            self.list_items.append(list_item)

    def get_index_by_name(self, name):
        for i, list_item in enumerate(self.list_items):
            if list_item.name == name:
                return i

    def get_list_by_category(self, category):
        locs = []
        for i, list_item in enumerate(self.list_items):
            if list_item.category == category:
                locs.append(list_item)
        return locs

    def delete(self, name):
        i = self.get_index_by_name(name)
        self.list_items.pop(i)

    def uncomplete(self, name):
        i = self.get_index_by_name(name)
        if self.list_items[i].category == "complete":
            self.list_items[i].category = "todo"

    def complete(self, name):
        i = self.get_index_by_name(name)
        if self.list_items[i].category == "todo":
            self.list_items[i].category = "complete"

    def load_data(self):
        with open("/usr/src/app/data.csv", "r") as csvfile:
            list_items = csv.reader(csvfile)
            for row in list_items:
                self.add(row[0], row[1], row[2])

    def __repr__(self):
        for list_item in self.list_items:
            print(f'{list_item.name} - {list_item.description} - {list_item.category}')


    def get_item_by_index(self, i):
        return self.list_items[i]


class Item:
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category
        self.steps = []

    def add_step(self,step):
        self.steps.append(step)
        self.steps = sorted(self.steps, key=lambda x: x.number)


class Step:
    def __init__(self, name, number):
        self.name= name
        self.number = number
        self.complete = False
