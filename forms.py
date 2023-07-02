"""Forms for our demo Flask app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, Optional,  URL

species = [("cat", "Cat"), ("dog", "Dog"), ("bird", "Bird"), ("fish", "Fish"), ("snake", "Snake"), ("rodent", "Rodent"), ("rabbit", "Rabbit"), ("reptile", "Reptile (i.e Snakes, Lizards, Chameleons)"), ("amphibian", "Amphibian (i.e Frogs/Toads, Salamanders, Axolotls)"), ("other", "Other")]

def coerce_bool(x):
    if isinstance(x, str):
        return x == "True" if x != "None" else None
    else:
        return bool(x) if x is not None else None


class AddPetForm(FlaskForm):
    """Form for adding pets"""

    name = StringField("Pet Name", validators=[InputRequired()], render_kw={"placeholder" : "Please Enter Name of Pet"})
    species = SelectField("Pet Species", validators=[InputRequired()], choices=species, render_kw={"placeholder" : "Please Enter Species of Pet"})
    photo_url = StringField("Enter Photo Url", validators=[Optional(), URL()], render_kw={"placeholder" : "(Optional)"})
    age = IntegerField("Pet Age", validators=[Optional(), NumberRange(0, 30)], render_kw={"placeholder" : "Enter an age (in years) between 0-30 (Optional)"})
    notes = TextAreaField("Additional Notes", validators=[Optional()], render_kw={"placeholder" : "(Optional)"})

class EditPetForm(FlaskForm):
    photo_url = StringField("Enter Photo Url", validators=[Optional(), URL()], render_kw={"placeholder" : "(Optional)"})
    age = IntegerField("Pet Age", validators=[Optional(), NumberRange(0, 30)], render_kw={"placeholder" : "Enter an age (in years) between 0-30 (Optional)"})
    available = SelectField("Is the pet still available?", choices=[(True, "Yes"), (False, "No")], coerce=coerce_bool)
    notes = TextAreaField("Edit Notes", validators=[Optional()], render_kw={"placeholder" : "(Optional)"})


