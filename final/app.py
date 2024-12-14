from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='restaurant_reservation'
)
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']
        people = request.form['people']

        try:
            # Insert into the name_and_phone table
            cursor.execute(
                "INSERT INTO name_and_phone (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

            # Insert into the name_and_date table
            cursor.execute(
                "INSERT INTO name_and_date (name, date) VALUES (%s, %s)",
                (name, date)
            )

            # Insert into the name_and_people table
            cursor.execute(
                "INSERT INTO name_and_people (name, people) VALUES (%s, %s)",
                (name, people)
            )

            conn.commit()
            return redirect(f'/success?name={name}&phone={phone}&date={date}&people={people}')
        except Exception as e:
            conn.rollback()
            message = f"Error: {e}"

    return render_template('index.html', message=message)

@app.route('/success')
def success():
    name = request.args.get('name')
    phone = request.args.get('phone')
    date = request.args.get('date')
    people = request.args.get('people')
    return render_template('success.html', name=name, phone=phone, date=date, people=people)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        
        # Check the name and phone in the name_and_phone table
        cursor.execute(
            "SELECT * FROM name_and_phone WHERE name = %s AND phone = %s", (name, phone)
        )
        reservation = cursor.fetchone()
        if reservation:
            # Fetch the date and people from the other tables
            cursor.execute(
                "SELECT date FROM name_and_date WHERE name = %s", (name,)
            )
            date = cursor.fetchone()

            cursor.execute(
                "SELECT people FROM name_and_people WHERE name = %s", (name,)
            )
            people = cursor.fetchone()

            # Pass reservation_id to the update form
            return render_template('update.html', reservation={
                'id': reservation[0],  # Assuming id is the first column
                'name': reservation[1],
                'phone': reservation[2],
                'date': date[0] if date else '',
                'people': people[0] if people else ''
            })
        else:
            message = 'No reservation found for the given details.'

    return render_template('manage.html', message=message)

@app.route('/update', methods=['POST'])
def update():
    try:
        name = request.form['name']
        date = request.form['date']
        people = request.form['people']
        reservation_id = request.form['id']

        # Ensure the required fields are present
        if not name or not date or not people:
            return "Error: Missing required fields", 400

        # Update database using reservation_id to uniquely identify the reservation
        cursor.execute(
            "UPDATE name_and_date SET date = %s WHERE id = %s",
            (date, reservation_id)
        )
        cursor.execute(
            "UPDATE name_and_people SET people = %s WHERE id = %s",
            (people, reservation_id)
        )

        conn.commit()
        return redirect('/')
    except KeyError as e:
        return f"Missing field: {e}", 400
    except Exception as e:
        conn.rollback()
        return f"Error: {e}", 500

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']

    try:
        # Delete data from the three tables based on 'name'
        cursor.execute("DELETE FROM name_and_phone WHERE name = %s", (name,))
        cursor.execute("DELETE FROM name_and_date WHERE name = %s", (name,))
        cursor.execute("DELETE FROM name_and_people WHERE name = %s", (name,))

        conn.commit()
        return redirect('/')
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)