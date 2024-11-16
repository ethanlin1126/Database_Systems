from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# 設定 MongoDB 連線字串
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"  # 替換為你的 MongoDB 連線字串
mongo = PyMongo(app)

@app.route('/')
def index():
    # 從 MongoDB 中取得所有資料
    data = list(mongo.db.employees.find())
    for item in data:
        item["_id"] = str(item["_id"])  # 將 ObjectId 轉換為字串
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add_data():
    # 從表單取得資料
    name = request.form.get('name')
    age = request.form.get('age')
    position = request.form.get('position')
    salary = request.form.get('salary')
    
    if name and age and position and salary:
        # 插入資料到 MongoDB
        mongo.db.employees.insert_one({
            'name': name,
            'age': int(age),
            'position': position,
            'salary': float(salary)
        })
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update_data(id):
    # 從表單取得更新後的資料
    name = request.form.get(f'name-{id}')
    age = request.form.get(f'age-{id}')
    position = request.form.get(f'position-{id}')
    salary = request.form.get(f'salary-{id}')

    if name and age and position and salary:
        # 更新 MongoDB 資料
        mongo.db.employees.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': name,
                'age': int(age),
                'position': position,
                'salary': float(salary)
            }}
        )
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_data(id):
    # 從 MongoDB 刪除資料
    mongo.db.employees.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
