from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def initandconnect():
    try:
        connection = sqlite3.connect('diary.db')
        connection.execute('''create table if not exists diary_db (
            id integer primary key autoincrement,
            date date unique not null,
            diary_data text not null)''')
        connection.commit()
        return connection
    except:
        print("error")
        return None

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        diarydata = request.form["diarydata"]
        date = request.form["date"]
        if diarydata and date:
            with sqlite3.connect('diary.db') as connection:
                connection.execute("insert into diary_db (diary_data, date) values (?, ?)", (diarydata, date))
                connection.commit()
        return redirect(url_for('index'))

    with sqlite3.connect('diary.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select * from diary_db')
        diary_data = cursor.fetchall()
    
    return render_template('index.html', diarydata=diary_data)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    with sqlite3.connect('diary.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select * from diary_db where id = ?", (entry_id,))
        entry = cursor.fetchone()
    return render_template('entry.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=["POST"])
def delete_entry(entry_id):
    with sqlite3.connect('diary.db') as connection:
        connection.execute("delete from diary_db where id = ?", (entry_id,))
        connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    initandconnect()
    app.run(debug=True)
