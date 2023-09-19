from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

# 连接到MySQL数据库
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test',
            user='root',
            password=''
        )
        if connection.is_connected():
            print('成功連接')
            return connection
    except Error as e:
        print('error:', e)
        return None

# 关闭MySQL连接
def close_mysql_connection(connection):
    if connection is not None and connection.is_connected():
        connection.close()
        print('關閉連接')

@app.route('/')
def index():
    return ('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    action = request.form.get('action')

    if action == 'download':
        # 执行下载 JSON 的操作
        email = request.form.get('mail')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        exercise = request.form.get('exercise')
        dietaryNeeds = request.form.get('dietaryNeeds')
        religion = request.form.get('religion')

        # 将数据存储为Python字典
        data = {
            'email': email,
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'exercise': exercise,
            'dietaryNeeds': dietaryNeeds,
            'religion': religion
        }

        # 转换为JSON字符串，禁用Unicode转义
        json_data = json.dumps(data, ensure_ascii=False)

        # 创建一个响应对象，将JSON数据作为文件附加到响应中
        response = make_response(json_data)
        response.headers['Content-Disposition'] = 'attachment; filename=userData.json'
        response.headers['Content-Type'] = 'application/json'

        return response
    elif action == 'upload':
        # 执行上传到数据库的操作
        email = request.form.get('mail')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        exercise = request.form.get('exercise')
        dietaryNeeds = request.form.get('dietaryNeeds')
        religion = request.form.get('religion')
        print("Email:", email)
        print("Age:", age)
        # 连接到MySQL数据库
        connection = connect_to_mysql()
        if connection is None:
            return "连接到数据库时出错"

        try:
            # 创建MySQL游标
            cursor = connection.cursor()

            # 执行插入操作
            query = "INSERT INTO user_info (email, age, gender, height, weight, exercise, dietaryNeeds, religion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (email, age, gender, height, weight, exercise, dietaryNeeds, religion)
            cursor.execute(query, data)

            # 提交事务
            connection.commit()

            return "数据已成功上传到MySQL数据库: " + query + " " + str(data)
        except Error as e:
            error_message = "上传数据到MySQL数据库时出错: " + str(e)
            print(error_message)
            return error_message
        finally:
            # 关闭游标和数据库连接
            if cursor:
                cursor.close()
            close_mysql_connection(connection)

if __name__ == '__main__':
    app.run(debug=True)
