from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 連線設置
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="amber1126",
    database="employee_db"
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('form.html', employees=employees)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    position = request.form['position']
    salary = request.form['salary']
    
    cursor = db.cursor()
    sql = "INSERT INTO employees (name, age, position, salary) VALUES (%s, %s, %s, %s)"
    val = (name, age, position, salary)
    cursor.execute(sql, val)
    db.commit()

    employee_id = cursor.lastrowid
    new_employee = {
        "id": employee_id,
        "name": name,
        "age": age,
        "position": position,
        "salary": salary
    }

    return jsonify(new_employee)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    age = request.form['age']
    position = request.form['position']
    salary = request.form['salary']

    cursor = db.cursor()
    sql = "UPDATE employees SET name=%s, age=%s, position=%s, salary=%s WHERE id=%s"
    val = (name, age, position, salary, id)
    cursor.execute(sql, val)
    db.commit()

    return jsonify({"status": "success"})

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor = db.cursor()
    sql = "DELETE FROM employees WHERE id=%s"
    cursor.execute(sql, (id,))
    db.commit()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
