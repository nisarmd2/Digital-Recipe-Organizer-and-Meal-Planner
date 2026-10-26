import tempfile
import unittest
from pathlib import Path
import app as recipe_app


class RecipeAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        recipe_app.DB_PATH = Path(self.temp_dir.name) / "test_recipes.db"
        recipe_app.app.config["TESTING"] = True
        self.client = recipe_app.app.test_client()
        recipe_app.init_db()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_displays_seed_recipe(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Vegetable Sandwich", response.data)

    def test_add_recipe(self):
        response = self.client.post("/add", data={
            "name": "Test Soup", "category": "Dinner",
            "ingredients": "Water, vegetables", "instructions": "Boil everything",
            "prep_minutes": "12"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Soup", response.data)

    def test_search_by_ingredient(self):
        response = self.client.get("/?q=banana")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Banana Smoothie", response.data)

    def test_missing_required_field_is_rejected(self):
        response = self.client.post("/add", data={
            "name": "", "category": "Dinner", "ingredients": "Rice",
            "instructions": "Cook", "prep_minutes": "10"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please complete all required fields", response.data)


if __name__ == "__main__":
    unittest.main()
