from flask import Flask, render_template, flash, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, get_database_uri, get_echo_TorF, Pet
from IPython import embed

from forms import AddPetForm, EditPetForm
# from forms import UserForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = get_echo_TorF()

app.config["SECRET_KEY"] = "oh-so-se cret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)



@app.route('/')
def homepage():
    """Populate homepage with list of pets"""

    pets = Pet.query.all()

    return render_template("pet-postings.html", pets = pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():

    """Add a pet here"""
    form = AddPetForm()

    if form.validate_on_submit():
        """Submit a new pet to the database"""

        if (form.photo_url.data == ""):
            # Will allow the pet model to utilize the default value if nothing is entered, otherwise it commits as an empty string
            form.photo_url.data = None

        name = form.name.data
        # I actually didn't know about using something like a dictionary and **data, but I went to the solution file and found this and thought it was such a good idea I had to add it! I also did some research on it after discovering it
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()

        flash(f"Added {name}!")

        return redirect('/')
    else:
        return render_template("pet-form.html", form=form)
    

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    """View a pet and provide form for modifying pet details"""
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    
    # Get the user object, assign new values, commit

    if form.validate_on_submit():
        """Commit form inputs and update pet data"""
        pet = Pet.query.get_or_404(pet_id)

        # I need to ask if there's a better way to write this
        # UPDATE: I asked, Ian if you're reading this these commented out parts are some of my various attempts

        # data = [(k, v) for k, v in form.data.items() if k != "csrf_token" and v != '' and v != None]

        ### Attemt 1 ###
        # for (k, v) in data:
        #     print(k)
        #     print(v)
        #     embed()
        #     pet.k = v
        #     db.session.commit()
            
            # print(pet.k)

        ### Attempt 2 ###
        # for {k: v} in data:
        #     pet.k = v
        #     db.session.commit()

        # Only update the database if the fields aren't blank
        if (form.photo_url.data != ""):
            pet.photo_url = form.photo_url.data

        if (form.age.data != None):
            pet.age = form.age.data

        if (form.notes.data != ""):
            pet.notes = form.notes.data

        pet.available = form.available.data
        
        db.session.commit()

        flash(f"Edited {pet.name}!")
        return redirect('/')
    else:
        return render_template("edit-pet.html", form=form, pet=pet)