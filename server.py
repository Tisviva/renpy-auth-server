from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(error="missing fields"), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify(error="user exists"), 400
    finally:
        cur.close()
        conn.close()

    return jsonify(success=True)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify(success=True)
    else:
        return jsonify(error="invalid credentials"), 401


if __name__ == "__main__":
    app.run()
