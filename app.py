from contextlib import contextmanager
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "recipes.db"

app = Flask(__name__)
app.secret_key = "change-this-for-production"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_connection():
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                prep_minutes INTEGER NOT NULL DEFAULT 0
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
        if count == 0:
            conn.executemany(
                """INSERT INTO recipes (name, category, ingredients, instructions, prep_minutes)
                   VALUES (?, ?, ?, ?, ?)""",
                [
                    ("Vegetable Sandwich", "Breakfast", "Bread, tomato, cucumber, cheese",
                     "Slice vegetables. Add them to bread with cheese and toast.", 15),
                    ("Banana Smoothie", "Drinks", "Banana, milk, oats",
                     "Blend all ingredients until smooth.", 5),
                    ("Simple Fried Rice", "Lunch", "Cooked rice, vegetables, oil, salt",
                     "Saute vegetables, add rice and seasoning, then mix well.", 20),
                ],
            )


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sql = "SELECT * FROM recipes WHERE 1=1"
    params = []
    if query:
        sql += " AND (name LIKE ? OR ingredients LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY name COLLATE NOCASE"
    with db_connection() as conn:
        recipes = conn.execute(sql, params).fetchall()
        categories = [r["category"] for r in conn.execute(
            "SELECT DISTINCT category FROM recipes ORDER BY category"
        ).fetchall()]
    return render_template("index.html", recipes=recipes, categories=categories,
                           query=query, selected_category=category)


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        ingredients = request.form.get("ingredients", "").strip()
        instructions = request.form.get("instructions", "").strip()
        try:
            prep_minutes = int(request.form.get("prep_minutes", "0"))
        except ValueError:
            prep_minutes = -1

        if not all([name, category, ingredients, instructions]):
            flash("Please complete all required fields.", "error")
        elif prep_minutes < 0:
            flash("Preparation time must be zero or more minutes.", "error")
        else:
            with db_connection() as conn:
                conn.execute(
                    """INSERT INTO recipes
                       (name, category, ingredients, instructions, prep_minutes)
                       VALUES (?, ?, ?, ?, ?)""",
                    (name, category, ingredients, instructions, prep_minutes),
                )
            flash("Recipe added successfully.", "success")
            return redirect(url_for("index"))
    return render_template("form.html", recipe=None, page_title="Add a recipe")


@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    with db_connection() as conn:
        recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    if recipe is None:
        flash("Recipe not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        ingredients = request.form.get("ingredients", "").strip()
        instructions = request.form.get("instructions", "").strip()
        try:
            prep_minutes = int(request.form.get("prep_minutes", "0"))
        except ValueError:
            prep_minutes = -1

        if not all([name, category, ingredients, instructions]):
            flash("Please complete all required fields.", "error")
        elif prep_minutes < 0:
            flash("Preparation time must be zero or more minutes.", "error")
        else:
            with db_connection() as conn:
                conn.execute(
                    """UPDATE recipes SET name=?, category=?, ingredients=?,
                       instructions=?, prep_minutes=? WHERE id=?""",
                    (name, category, ingredients, instructions, prep_minutes, recipe_id),
                )
            flash("Recipe updated successfully.", "success")
            return redirect(url_for("index"))
    return render_template("form.html", recipe=recipe, page_title="Edit recipe")


@app.route("/delete/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    with db_connection() as conn:
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    flash("Recipe deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
