from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, find_dotenv
from flask_mysqldb import MySQL
import os


app = Flask(__name__)
load_dotenv(find_dotenv())

app.config["MYSQL_HOST"] = os.environ.get("HOST")
app.config["MYSQL_USER"] = os.environ.get("USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DATABASE")
mysql = MySQL(app)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/get_books", methods=["GET"])
def get_books():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        result = cur.fetchall()
        cur.close()
        books = []
        for i in range(len(result)):
            books.append({
                "id": result[i][0],
                "name": result[i][1],
                "author": result[i][2],
                "country": result[i][3]
            })
        return jsonify(books)
    else:
        return jsonify("method incorrect"),500

@app.route("/create_book", methods=["POST"])
def create_book():
    if request.method == "POST":
        data = request.get_json()
        name = data['name']
        author = data['author']
        country = data['country']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (name,author,country) VALUES(%s,%s,%s)", (name, author, country))
        mysql.connection.commit()
        cur.close()
        return jsonify("OK")
    else:
        return jsonify("method incorrect"),500

@app.route("/edit_book", methods=["PUT"])
def edit_book():
    if request.method == "PUT":
        data = request.get_json()
        id   = data['id']
        name = data['name']
        author = data['author']
        country = data['country']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE books SET name = %s, author = %s , country = %s WHERE Id = %s", (name, author, country, id))
        mysql.connection.commit()
        cur.close()
        return jsonify("ok")
    else:
        return jsonify("method incorrect"),500

@app.route("/delete_book", methods=["DELETE"])
def delete_book():
    if request.method == "DELETE":
        data = request.get_json()
        id = data['id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM books WHERE id=%s", id)
        mysql.connection.commit()
        cur.close()
        return jsonify("ok")
    else:
        return jsonify("method incorrect"),500
          

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
