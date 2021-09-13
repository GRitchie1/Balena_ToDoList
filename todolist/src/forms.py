from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, DecimalField
from wtforms.validators import DataRequired

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
  submit = SubmitField("Add Item")

class AddStepForm(FieldsRequiredForm):
   name  = StringField("Step Name", validators=[DataRequired()])
   number = DecimalField("Step Number", validators=[DataRequired()])
   submit = SubmitField("Add Item")
