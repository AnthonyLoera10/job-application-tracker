from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    connection = sqlite3.connect("database.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            location TEXT,
            date_applied TEXT,
            status TEXT,
            url TEXT,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    applications = connection.execute(
        "SELECT * FROM applications"
    ).fetchall()

    total = connection.execute(
        "SELECT COUNT(*) FROM applications"
    ).fetchone()[0]

    interviews = connection.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Interview'"
    ).fetchone()[0]

    offers = connection.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Offer'"
    ).fetchone()[0]

    rejected = connection.execute(
    "SELECT COUNT(*) FROM applications WHERE status = 'Rejected'"
).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        applications=applications,
        total=total,
        interviews=interviews,
        offers=offers,
        rejected=rejected
    )

@app.route("/add", methods=["POST"])
def add_application():
    company = request.form["company"]
    position = request.form["position"]
    location = request.form["location"]
    date_applied = request.form["date"]
    status = request.form["status"]
    url = request.form["url"]
    notes = request.form["notes"]

    connection = sqlite3.connect("database.db")

    connection.execute("""
        INSERT INTO applications
        (company, position, location, date_applied, status, url, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (company, position, location, date_applied, status, url, notes))

    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    if request.method == "POST":
        company = request.form["company"]
        position = request.form["position"]
        location = request.form["location"]
        date_applied = request.form["date"]
        status = request.form["status"]
        url = request.form["url"]
        notes = request.form["notes"]

        connection.execute("""
            UPDATE applications
            SET company = ?, position = ?, location = ?,
                date_applied = ?, status = ?, url = ?, notes = ?
            WHERE id = ?
        """, (company, position, location, date_applied,
              status, url, notes, id))

        connection.commit()
        connection.close()

        return redirect("/")

    application = connection.execute(
        "SELECT * FROM applications WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template("edit.html", application=application)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_application(id):
    connection = sqlite3.connect("database.db")

    connection.execute(
        "DELETE FROM applications WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)