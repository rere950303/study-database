import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect("dbname=tutorial user=postgres password=0000")
cur = connect.cursor()  # create cursor


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/return', methods=['post'])
def re_turn():
    return render_template("main.html")


@app.route('/print_table', methods=['post'])
def print_table():
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall()

    return render_template("print_table.html", users=result)


@app.route('/register', methods=['post'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]

    if send == "sign up":
        cur.execute("SELECT id FROM users where id like '{}';".format(id))
        result = cur.fetchall()
        if len(result) != 0:
            return "id가 중복됩니다. 다른 id를 입력해주세요."
        cur.execute("INSERT INTO users VALUES('{}', '{}');".format(id, password))
        connect.commit()
        return "정상적으로 회원가입 되었습니다."
    else:
        cur.execute("SELECT password FROM users where id like '{}';".format(id))
        result = cur.fetchone()
        if result[0] == password:
            return render_template("login_success.html")
        else:
            return render_template("login_fail.html")


if __name__ == '__main__':
    app.run()
