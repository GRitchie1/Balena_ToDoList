from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class FieldsRequiredForm(FlaskForm):
  class Meta:
    def render_field(self, field, render_kw):
      if field.type == "_Option":
        render_kw.setdefault("required", True)
      return super().render_field(field, render_kw)

categories = [(False,"To Do"), (True, "Complete")]

class AddItemForm(FieldsRequiredForm):
  name  = StringField("Item Name", validators=[DataRequired()])
  description = TextAreaField("Item Description", validators=[DataRequired()])
  priority = IntegerField("Priority", validators=[DataRequired()])
  due_date = DateField('Due Date')
  due_time = TimeField('Due Time (hh:mm)',format = "%H:%M")
  submit = SubmitField("Add Item")


class AddStepForm(FieldsRequiredForm):
   name  = StringField("Step Name", validators=[DataRequired()])
   submit = SubmitField("Add Step")

class EditItemForm(FieldsRequiredForm):
  name  = StringField("Item Name", validators=[DataRequired()])
  description = TextAreaField("Item Description", validators=[DataRequired()])
  priority = IntegerField("Priority", validators=[DataRequired()])
  due_date = DateField('Due Date')
  due_time = TimeField('Due Time (hh:mm)',format = "%H:%M")
  submit = SubmitField("Save Changes")
