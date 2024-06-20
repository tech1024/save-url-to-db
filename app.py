from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def get_urls():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM urls')
    urls = cursor.fetchall()
    conn.close()

    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)