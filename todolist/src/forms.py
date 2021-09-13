from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class FieldsRequiredForm(FlaskForm):
  """Require radio fields to have content. This works around the bug that WTForms radio fields don't honor the `DataRequired` or `InputRequired` validators."""
  class Meta:
    def render_field(self, field, render_kw):
      if field.type == "_Option":
        render_kw.setdefault("required", True)
      return super().render_field(field, render_kw)

categories = [(False,"To Do"), (True, "Complete")]

## Create Form Here
class AddItemForm(FieldsRequiredForm):
  name  = StringField("Item Name", validators=[DataRequired()], default = "")
  description = TextAreaField("Item Description", validators=[DataRequired()], default = "")
  submit = SubmitField("Add Item")
