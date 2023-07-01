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

            

# name species photo_url age notes

# EXAMPLE TESTS BELOW




# class SnackViewsTestCase(TestCase):
#     """Tests for views for Snacks."""

#     def test_snack_add_form(self):
#         with app.test_client() as client:
#             resp = client.get("/add")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('<form id="snack-add-form"', html)

#     def test_snack_add(self):
#         with app.test_client() as client:
#             d = {"name": "Test2", "price": 2}
#             resp = client.post("/add", data=d, follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("Added Test2 at 2", html)




# class UserViewsTestCase(TestCase):
#     """Tests for views for Users."""

#     def setUp(self):
#         """Make demo data."""

#         User.query.delete()

#         user = User(name="Test User", email="test@test.com")
#         db.session.add(user)
#         db.session.commit()

#         self.user_id = user.id

#     def tearDown(self):
#         """Clean up fouled transactions."""

#         db.session.rollback()

#     def test_user_edit_form(self):
#         with app.test_client() as client:
#             resp = client.get(f"/users/{self.user_id}/edit")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("<form", html)

#     def test_user_edit(self):
#         with app.test_client() as client:
#             resp = client.post(
#                 f"/users/{self.user_id}/edit",
#                 data={'name': 'Test2', 'email': "test2@test.com"},
#                 follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn(f"User {self.user_id} updated!", html)

#             user = User.query.get(self.user_id)
#             self.assertEquals(user.name, "Test2")
#             self.assertEquals(user.email, "test2@test.com")

#     def test_user_edit_form_fail(self):
#         with app.test_client() as client:
#             # add w/ invalid email
#             resp = client.post(
#                 f"/users/{self.user_id}/edit",
#                 data={'name': 'Test3', 'email': 'not-an-email'})
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("<form", html)
#             self.assertNotIn("updated!", html)
