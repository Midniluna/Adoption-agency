from unittest import TestCase

from app import app
from models import db, Pet

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False


class PetViewsTestCase(TestCase):
    """Tests for views of pets"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.app_context = app.app_context()
        cls.app_context.push()

        # Create all tables in the database
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        """Make demo data"""

        Pet.query.delete()

        pet = Pet(name="Spot", species="dog")
        db.session.add(pet)
        db.session.commit()

        self.pet_id = pet.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()


    def test_pet_model(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            pet = Pet.query.get(self.pet_id)

            self.assertEqual(pet.name, "Spot")
            self.assertEqual(pet.photo_url, "https://i.imgur.com/89XRpp8.png")
            self.assertTrue(pet.available)
            self.assertIn(f"is available!", html)



    def test_new_pet(self):
        with app.test_client() as client:
            
            post_resp = client.post('/add', data={"name" : "Rex", "species" : "rodent", "photo_url" : None, "age" : "4", "notes" : "He's so cute tootsit. The sproingly scrunkus."})
            rex = Pet.query.filter_by(name="Rex").first()

            self.assertEqual(post_resp.status_code, 302)
            self.assertIsNotNone(rex.photo_url)



    def test_unavailable_pet(self):
        with app.test_client() as client:

            pet = Pet(name = "Dom", species = "Iguana", available = False)
            db.session.add(pet)
            db.session.commit()

            # Don't really need this line in retrospect
            # dom = Pet.query.filter_by(name="Dom").first()

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn("is not available", html)
