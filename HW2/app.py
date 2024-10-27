from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'employee_db'

mysql = MySQL(app)

# 顯示首頁和三個表格
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    
    # 查詢三個表格的資料
    cur.execute("SELECT * FROM name_age_table")
    name_age_data = cur.fetchall()
    
    cur.execute("SELECT * FROM name_position_table")
    name_position_data = cur.fetchall()
    
    cur.execute("SELECT * FROM name_salary_table")
    name_salary_data = cur.fetchall()
    
    cur.close()
    return render_template('index.html', 
                           name_age_data=name_age_data, 
                           name_position_data=name_position_data, 
                           name_salary_data=name_salary_data)

# 處理表單提交
@app.route('/add', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        salary = request.form['salary']
        
        cur = mysql.connection.cursor()
        # 插入資料到三個表格
        cur.execute("INSERT INTO name_age_table (name, age) VALUES (%s, %s)", (name, age))
        cur.execute("INSERT INTO name_position_table (name, position) VALUES (%s, %s)", (name, position))
        cur.execute("INSERT INTO name_salary_table (name, salary) VALUES (%s, %s)", (name, salary))
        mysql.connection.commit()
        cur.close()
        
    return redirect(url_for('index'))

# 更新資料
@app.route('/update/<string:table>/<int:id>', methods=['POST'])
def update_employee(table, id):
    if request.method == 'POST':
        name = request.form['name']
        cur = mysql.connection.cursor()
        # 根據表格名稱和提供的欄位進行更新
        if table == 'name_age_table':
            age = request.form['age']
            cur.execute("UPDATE name_age_table SET name=%s, age=%s WHERE id=%s", (name, age, id))
        elif table == 'name_position_table':
            position = request.form['position']
            cur.execute("UPDATE name_position_table SET name=%s, position=%s WHERE id=%s", (name, position, id))
        elif table == 'name_salary_table':
            salary = request.form['salary']
            cur.execute("UPDATE name_salary_table SET name=%s, salary=%s WHERE id=%s", (name, salary, id))
        
        mysql.connection.commit()
        cur.close()
        
    return redirect(url_for('index'))

# 刪除資料
@app.route('/delete/<string:table>/<int:id>', methods=['GET'])
def delete_employee(table, id):
    cur = mysql.connection.cursor()
    # 根據表格名稱進行刪除
    if table == 'name_age_table':
        cur.execute("DELETE FROM name_age_table WHERE id=%s", [id])
    elif table == 'name_position_table':
        cur.execute("DELETE FROM name_position_table WHERE id=%s", [id])
    elif table == 'name_salary_table':
        cur.execute("DELETE FROM name_salary_table WHERE id=%s", [id])
    
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

# Join 資料
@app.route('/join')
def join_tables():
    cur = mysql.connection.cursor()
    # Join 三個表格
    cur.execute("""
        SELECT a.name, a.age, p.position, s.salary 
        FROM name_age_table a
        JOIN name_position_table p ON a.name = p.name
        JOIN name_salary_table s ON a.name = s.name
    """)
    joined_data = cur.fetchall()
    cur.close()
    
    return render_template('join.html', joined_data=joined_data)

if __name__ == '__main__':
    app.run(debug=True)

# Join 資料
@app.route('/join')
def join_tables():
    cur = mysql.connection.cursor()
    # Join 三個表格
    cur.execute("""
        SELECT a.name, a.age, p.position, s.salary 
        FROM name_age_table a
        JOIN name_position_table p ON a.name = p.name
        JOIN name_salary_table s ON a.name = s.name
    """)
    joined_data = cur.fetchall()
    cur.close()
    
    return render_template('join.html', joined_data=joined_data)
