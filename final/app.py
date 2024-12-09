from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'restaurant_reservation'
}

# Home page with reservation form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']
        people = request.form['people']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO reservations (name, phone, date, people) VALUES (%s, %s, %s, %s)",
                       (name, phone, date, people))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('success', name=name, phone=phone, date=date, people=people))

    return render_template('index.html')

# Success page
@app.route('/success')
def success():
    name = request.args.get('name')
    phone = request.args.get('phone')
    date = request.args.get('date')
    people = request.args.get('people')
    return render_template('success.html', name=name, phone=phone, date=date, people=people)

# Check or update reservation
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM reservations WHERE name=%s AND phone=%s", (name, phone))
            reservation = cursor.fetchone()  # 確保讀取一行結果
            # 若未找到預約，將 reservation 設為 None
            if reservation is None:
                reservation = None
        finally:
            cursor.fetchall()  # 確保讀取所有未讀取的結果，避免錯誤
            cursor.close()  # 確保游標被正確關閉
            connection.close()

        if reservation:
            return render_template('update.html', reservation=reservation)
        else:
            return render_template('manage.html', error="No reservation found.")

    return render_template('manage.html')


# Update reservation
@app.route('/update', methods=['POST'])
def update():
    reservation_id = request.form['id']
    date = request.form['date']
    people = request.form['people']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("UPDATE reservations SET date=%s, people=%s WHERE id=%s", (date, people, reservation_id))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))

# Delete reservation
@app.route('/delete', methods=['POST'])
def delete():
    reservation_id = request.form['id']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM reservations WHERE id=%s", (reservation_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
