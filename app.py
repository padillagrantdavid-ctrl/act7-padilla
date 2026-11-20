import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
DATABASE = Path(__file__).with_name("students.db")

STUDENT_PROFILE = {
	"student_id": "24-00170",
	"name": "Grant David Padilla",
	"program": "BSIT",
	"year": 3,
	"section": "B",
}


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/student")
def get_student():
	return jsonify(STUDENT_PROFILE)


@app.route("/hello")
def say_hello():
	name = request.args.get("name", "Student")
	return jsonify({"message": f"Hello, {name}!"})


@app.route("/academic")
def get_academic_profile():
	return jsonify(
		{
			"student_id": STUDENT_PROFILE["student_id"],
			"name": STUDENT_PROFILE["name"],
			"program": STUDENT_PROFILE["program"],
			"year": STUDENT_PROFILE["year"],
			"section": STUDENT_PROFILE["section"],
		}
	)


def get_db_connection():
	conn = sqlite3.connect(DATABASE)
	conn.row_factory = sqlite3.Row
	return conn


@app.route("/students")
def get_students():
	conn = get_db_connection()
	try:
		students = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
		return jsonify([dict(student) for student in students])
	finally:
		conn.close()


@app.route("/students/<int:student_db_id>")
def get_student_by_id(student_db_id):
	conn = get_db_connection()
	try:
		student = conn.execute(
			"SELECT * FROM students WHERE id = ?", (student_db_id,)
		).fetchone()
	finally:
		conn.close()

	if student is None:
		return jsonify({"error": "Student not found"}), 404
	return jsonify(dict(student))


@app.route("/students/section/<section>")
def get_students_by_section(section):
	conn = get_db_connection()
	try:
		students = conn.execute(
			"SELECT * FROM students WHERE upper(section) = ? ORDER BY id",
			(section.upper(),),
		).fetchall()
		return jsonify([dict(student) for student in students])
	finally:
		conn.close()


if __name__ == "__main__":
	app.run(debug=True)