import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
connect = psycopg2.connect("dbname=term user=postgres password=1234")
cur = connect.cursor()  # create cursor


@app.route('/')
def main():
    return render_template("main.html")

@app.route('/withdraw', methods=['post', 'get'])
def withdraw():
    id = request.form["id"]
    cur.execute("delete from items where seller = '{}'".format(id))
    cur.execute("delete from account where id = '{}'".format(id))
    cur.execute("delete from trade where buyer = '{}' or seller = '{}'".format(id, id))
    cur.execute("delete from users where id = '{}'".format(id))
    connect.commit()

    return render_template("main.html")

@app.route('/category_get', methods=['post', 'get'])
def category_get():
    return render_template("category_add.html")

@app.route('/category_add', methods=['post', 'get'])
def category_add():
    code = request.form["code"]
    type = request.form["type"]

    cur.execute("select * from category where code = '{}'".format(code))
    result = cur.fetchall()
    if len(result) != 0:
        return render_template("category_add_fail.html", error="이미 존재하는 code 입니다.")

    cur.execute("insert into category values ('{}', '{}')".format(code, type))
    connect.commit()

    return render_template("category_add_success.html", id='admin')

@app.route('/users', methods=['post', 'get'])
def users():
    cur.execute("select * from users")
    users = cur.fetchall()

    return render_template("users.html", users=users)

@app.route('/trades', methods=['post', 'get'])
def trades():
    cur.execute("select * from trade")
    trades = cur.fetchall()

    return render_template("trades.html", trades=trades)

@app.route('/logout', methods=['post', 'get'])
def logout():
    return render_template("main.html")


@app.route('/item_get', methods=['post'])
def item_get():
    id = request.form["id"]
    cur.execute("select * from category")
    results = cur.fetchall()
    return render_template("item_add.html", results=results, id=id)

@app.route('/item_add', methods=['post'])
def item_add():
    id = request.form["id"]
    code = request.form["code"]
    name = request.form["name"]
    price = int(request.form["price"])
    stock = int(request.form["stock"])

    toTuple = (code,)

    cur.execute("select code from category")
    codes = cur.fetchall()

    if toTuple not in codes:
        return render_template("add_fail.html", error="존재하지 않는 code입니다.", id=id)

    cur.execute(
        "select * from items where code = '{}' and name = '{}' and price = '{}' and seller = '{}'".format(code, name,
                                                                                                          price, id))
    result = cur.fetchone()

    if result is None:
        cur.execute("insert into items values ('{}', '{}', {}, {}, '{}')".format(code, name, price, stock, id))
        connect.commit()
    else:
        cur.execute(
            "update items set stock = stock + {} where code = '{}' and name = '{}' and price = {} and seller = '{}'".format(
                stock, code, name, price, id))
        connect.commit()

    return render_template("add_success.html", id=id)


@app.route('/item_buy', methods=['post'])
def item_buy():
    code = request.form["code"]
    name = request.form["name"]
    price = int(request.form["price"])
    stock = int(request.form["stock"])
    seller = request.form["seller"]
    buyer = request.form["buyer"]

    cur.execute("select balance, rating from account where id = '{}'".format(buyer))
    profile = cur.fetchone()

    return render_template("item_buy.html", code=code, name=name, price=price, stock=stock, seller=seller, buyer=buyer,
                           profile=profile)


@app.route('/item_buying', methods=['post'])
def item_buying():
    code = request.form["code"]
    name = request.form["name"]
    price = int(request.form["price"])
    stock = int(request.form["stock"])
    seller = request.form["seller"]
    buyer = request.form["buyer"]
    amount = int(request.form["amount"])
    balance = int(request.form["balance"])
    rating = request.form["rating"]

    total_price = amount * price
    cur.execute("select discount from account natural join rating_info where id ='{}'".format(buyer))
    discount = float(cur.fetchone()[0])

    if amount > stock or total_price > balance:
        return render_template("buy_fail.html", code=code, name=name, price=price, stock=stock, seller=seller,
                               buyer=buyer, error="stock, balance 범위내에서 입력해주세요.")

    discount_price = int(total_price * discount / 100)
    final_price = int(total_price - discount_price)

    return render_template("item_buying.html", price=price, amount=amount, name=name, code=code, balance=balance,
                           rating=rating, total_price=total_price, discount_price=discount_price,
                           final_price=final_price, seller=seller, buyer=buyer)


@app.route('/confirm', methods=['post'])
def confirm():
    price = request.form["price"]
    amount = request.form["amount"]
    name = request.form["name"]
    code = request.form["code"]
    buyer = request.form["buyer"]
    final_price = int(request.form["final_price"])
    seller = request.form["seller"]
    total_price = int(request.form["total_price"])

    cur.execute("update account set balance = balance + {} where id ='{}'".format(total_price, seller))
    cur.execute("update account set balance = balance - {} where id ='{}'".format(final_price, buyer))
    connect.commit()

    cur.execute("select * from rating_info")
    rating_infos = cur.fetchall()

    cur.execute("select balance from account where id ='{}'".format(buyer))
    balanceOfBuyer = cur.fetchone()[0]
    cur.execute("select balance from account where id ='{}'".format(seller))
    balanceOfSeller = cur.fetchone()[0]

    for info in rating_infos:
        if balanceOfBuyer > info[1]:
            cur.execute("update account set rating = '{}' where id ='{}'".format(info[0], buyer))
            break

    for info in rating_infos:
        if balanceOfSeller > info[1]:
            cur.execute("update account set rating = '{}' where id ='{}'".format(info[0], seller))
            break

    cur.execute("insert into trade values('{}', '{}', '{}', {})".format(buyer, seller, code, total_price))
    connect.commit()

    cur.execute(
        "update items set stock = stock - {} where code ='{}' and name ='{}' and price ={} and seller ='{}'".format(
            amount, code, name, price, seller))
    connect.commit()
    cur.execute("delete from items where stock = 0")
    connect.commit()

    return render_template("buy_success.html", id=buyer)


@app.route('/return', methods=['post'])
def re_turn():
    return render_template("main.html")


@app.route('/cancel', methods=['post'])
def cancel():
    id = request.form["id"]
    return redirect(url_for('register', id=id))

@app.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'GET':
        return loginSuccess(request.args.get('id', type=str))

    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]

    if send == "sign up":
        cur.execute("SELECT id FROM users where id like '{}';".format(id))
        result = cur.fetchall()
        if len(result) != 0:
            return render_template("ID_collision.html")
        cur.execute("INSERT INTO users VALUES('{}', '{}');".format(id, password))
        cur.execute("INSERT INTO account VALUES('{}', '{}', '{}');".format(id, 10000, 'beginner'))
        connect.commit()
        return render_template("signup_success.html")
    else:
        cur.execute("SELECT password FROM users where id like '{}';".format(id))
        result = cur.fetchone()

        if result is None:
            return render_template("login_fail.html", error="일치하는 id가 없습니다.")

        if result[0] == password:
            return loginSuccess(id)
        else:
            return render_template("login_fail.html", error="비밀번호가 일치하지 않습니다.")


def loginSuccess(id):
    cur.execute("select max(count) from (select count(*) as count from trade group by code) as result;")
    maxCount = cur.fetchone()

    if maxCount[0] is None:
        return render_template("login_success.html", id=id, results=[], profile=getProfile(id), items=getItems(id))

    cur.execute("select type from trade natural join category group by type having count(*) = {};".format(maxCount[0]))
    popular_categories = cur.fetchall()
    result = []
    for popular_category in popular_categories:
        tmp = [popular_category[0]]

        cur.execute(
            "select max(count) from (select count(*) as count from trade natural join category where type = '{}' group by buyer) as result;".format(
                popular_category[0]))
        maxCount = cur.fetchone()
        cur.execute(
            "select buyer from trade natural join category where type = '{}' group by buyer having count(*) = {};".format(
                popular_category[0], maxCount[0]))
        best_buyer = cur.fetchone()
        tmp += best_buyer

        cur.execute(
            "select max(count) from (select count(*) as count from trade natural join category where type = '{}' group by seller) as result;".format(
                popular_category[0]))
        maxCount = cur.fetchone()
        cur.execute(
            "select seller from trade natural join category where type = '{}' group by seller having count(*) = {};".format(
                popular_category[0], maxCount[0]))
        best_seller = cur.fetchone()
        tmp += best_seller

        result.append(tmp)

    return render_template("login_success.html", id=id, results=result, profile=(getProfile(id)), items=(getItems(id)))


def getItems(id):
    cur.execute("select * from items where seller <> '{}'".format(id))
    items = cur.fetchall()
    return items


def getProfile(id):
    cur.execute("select id, balance, rating from account where id = '{}'".format(id))
    profile = cur.fetchone()
    return profile

if __name__ == '__main__':
    app.run()