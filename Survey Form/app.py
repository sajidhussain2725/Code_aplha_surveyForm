from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/static')

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'survey_data'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['number']
        programmer_type = request.form['dropdown']
        focus_area = request.form['radio-set']
        interests = request.form.getlist('checkbox-set')
        comments = request.form['comments']
        other_specify = request.form.get('other-specify', '')

        cursor = mysql.connection.cursor()
        query = "INSERT INTO survey_data (name, email, age, programmer_type, focus_area, interests, comments, other_specify) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email, age, programmer_type, focus_area, ', '.join(interests), comments, other_specify)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        return "Data has been successfully submitted!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
