# Digital Recipe Organizer (RecipeBox)

A beginner-friendly web application for demonstrating the Software Development Life Cycle (SDLC). Users can add, view, search, edit, and delete recipes. Data is stored in a local SQLite database.

## Features
- View sample recipes
- Add a recipe with category, ingredients, instructions, and preparation time
- Search by recipe name or ingredient
- Filter by category
- Edit and delete recipes
- Validate required fields and non-negative preparation time
- Store data in SQLite

## Requirements
- Python 3.10 or newer
- Internet connection only for the optional Google Fonts styling; the application itself works without it
- Flask (installed from requirements.txt)

## Run on Windows
1. Extract the ZIP.
2. Open the extracted `Digital_Recipe_Organizer` folder in VS Code.
3. Open a terminal in that folder.
4. Create a virtual environment (recommended):
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the app:
   ```bash
   python app.py
   ```
7. Open the local address printed in the terminal, normally `http://127.0.0.1:5000`.

The SQLite database and three example recipes are created automatically on first run.

## Quick demonstration
1. Show the home page and sample recipes.
2. Search for `banana` or filter by `Drinks`.
3. Add a recipe and show it in the list.
4. Edit the recipe and save.
5. Delete the recipe.
6. Try submitting the form with a required field empty or a negative time to show validation.

## Project structure
- `app.py` — routes, validation, database access
- `templates/` — HTML pages
- `static/style.css` — styling
- `tests/test_app.py` — automated tests
- `SDLC_Lifecycle_Document.docx` — lifecycle report

## Notes
This is a classroom demonstration project, not a production service. Before public deployment, use a production WSGI server, secure configuration, CSRF protection, and a backup strategy.
