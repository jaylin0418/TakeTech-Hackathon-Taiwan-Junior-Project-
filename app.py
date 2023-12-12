import os
from datetime import time
#from re import DEBUG
from flask import render_template, redirect, request, url_for, flash, abort, session, sessions
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import query
from myproject import app, db
from myproject.models import User, Product, Volunteer
from myproject.forms import LoginForm, ProductForm, RegistrationForm, ApplyForm, SearchForm, VolunteerForm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
from sqlalchemy import exc


@app.route('/')
def home():
    return render_template('home.html')


# array = Product.query.all()
# array_num = []
# for i in array:
#     array_num.append(i.id)
# print(array_num)


# array_username = []
# k = User.query.all()
# for i in k:
#     array_username.append(i.user_id)


@app.route('/intro')
def intro():
    return render_template('intro.html')


@app.route('/schools')
def school():
    return render_template('schools.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/team_info')
def team_info():
    return render_template('team_info.html')


@app.route('/article')
def article():
    return render_template('article.html')


@app.route('/article_GoogleMeet')
def article_GoogleMeet():
    return render_template('article_GoogleMeet.html')


@app.route('/article_GoogleDrive')
def article_GoogleDrive():
    return render_template('article_GoogleDrive.html')


@app.route('/article_GoogleClassroom')
def article_Classroom():
    return render_template('article_GoogleClassroom.html')


@app.route('/international')
def international():
    return render_template('international.html')


@app.route('/volunteer_list')
@login_required
def volunteer_list():
    infos = Volunteer.query.all()
    return render_template('volunteer_list.html', infos=infos)


@app.route('/volunteer', methods=["GET", "POST"])
@login_required
def volunteer():
    form = VolunteerForm()
    if request.method == "GET":
        return render_template('volunteer.html', form=form)
    elif request.method == "POST":
        try:
            person = Volunteer(volunteer_id=current_user.user_id,
                               name=form.name.data,
                               experience=form.experience.data,
                               reason=form.experience.data,
                               professional=form.professional.data,
                               time=form.time.data,
                               contact=form.contact.data)
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
            flash('註冊失敗，可能您表單填寫有誤或是您已經登錄為志工')
            return render_template('volunteer.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        try:
            user = User(username=form.username.data,
                        password=form.password.data, user_id=form.user_id.data, role=form.role.data)
            # add to db table
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        except:
            db.session.rollback()
            flash('電子郵件或使用者名稱已經有人使用')
            return render_template('register.html', form=form, warning='')
    return render_template('register.html', form=form, warning='')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                return redirect('/welcome')
        except:
            flash('登入失敗，請重新登入')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/post_product', methods=['GET', 'POST'])
@login_required
def post_product():
    form = ProductForm()
    if request.method == 'GET':
        return render_template('post_product.html', form=form)
    elif request.method == 'POST':
        product = Product(uploader=current_user.username,
                          uploader_id=current_user.user_id,
                          product_name=form.product_name.data,
                          product_details=form.product_details.data,
                          image=form.image.data,
                          quantities=form.quantities.data,
                          brand=form.brand.data,
                          expiration_date=form.expiration_date.data,
                          date_posted=time.ctime())
        db.session.add(product)
        db.session.commit()
        array = Product.query.all()
        global array_num
        array_num = []
        for i in array:
            array_num.append(i.id)
        print(array_num)
        return redirect('/products')


@app.route('/products', methods=["GET", "POST"])
@login_required
def products():
    form = SearchForm()
    infos = Product.query.all()
    if request.method == "GET":
        return render_template('products.html', infos=infos, form=form)
    elif request.method == "POST":
        k = Product.query.filter(
            Product.product_name.ilike(f'%{form.word.data}%'))
        return render_template('products.html', infos=k, form=form)


@app.route('/welcome')
@login_required
def welcome():
    return redirect(url_for('home'))


@app.route('/send', methods=["POST", "GET"])
@login_required
def send():
    if request.method == "GET":
        return render_template('send.html')
    if request.method == "POST":
        if int(request.form.get('case_num')) not in array_num:
            flash("物件編號不存在")
            return render_template('send.html')
        k = Product.query.filter_by(
            id=int(request.form.get('case_num'))).first()
        if k.uploader_id != current_user.user_id:
            flash("此物件非您擁有")
            return render_template('send.html')
        email = MIMEMultipart()
        # 郵件標題
        email[
            "subject"] = f"需求申請回覆 寄件者（物件擁有者）：{current_user.user_id} 物件號碼：{request.form.get('case_num')}"
        email["from"] = 'tacktechofficial@gmail.com'  # 寄件者
        email["to"] = request.form.get('reciever')
        inner = request.form.get(
            'content')+'\r\n----------------------------\r\n物件擁有者不願透露電子郵件，此信件為您申請物件的擁有者撰寫，透過官方帳號發送，請勿回覆此郵件。如果仍需聯絡物件用有者，請透過原申請頁面寄信'
        email.attach(MIMEText(inner))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("tacktechofficial@gmail.com",
                           "ndticvekvhfviilf")  # 登入寄件者gmail
                smtp.send_message(email)  # 寄送郵件
                print("Complete!")
                return render_template('home.html')
            except Exception as e:
                print("Error message: ", e)
                return render_template('home.html')


@app.route('/requests')
def requests():
    infos = User.query.all()
    return render_template('request.html', infos=infos)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/<array_username>', methods=["GET", "POST"])
@login_required
def single_user(array_username):
    user = User.query.filter_by(user_id=array_username).first()
    if request.method == 'GET':
        return render_template('single_user.html', user=user)
    elif request.method == "POST":
        content = request.form.get('content')
        user = User.query.filter_by(username=current_user.username).first()
        user.intro = content
        db.session.commit()
        return render_template('single_user.html', user=user)


@app.route('/<int:array_num>', methods=['GET', 'POST'])
def print_num(array_num):
    form = ApplyForm()
    info = Product.query.filter_by(id=array_num).first()
    try:
        reciever = info.uploader
    except:
        return render_template('home.html')
    if request.method == "GET":
        return render_template('single.html', info=info, form=form)
    elif request.method == "POST":
        email = MIMEMultipart()
        # 郵件標題
        email["subject"] = f"需求申請 申請機構為 {current_user.user_id}，物件號碼 {array_num}"
        email["from"] = 'tacktechofficial@gmail.com'  # 寄件者
        email["to"] = request.form.get('reciever')
        inner = request.form.get(
            'content')+f'\r\n--------------------------------------------------------\r\n備註：您可以選擇直接與機構透過電子郵件聯絡。若您不願意透露電子郵件（\r\n該申請機構的電子郵件為：{current_user.username}），也可以透過 http://127.0.0.1:8080/send 進行回覆。請勿回覆本郵件！若確定物品成功捐贈，請立即前往該物件詳細資料的網頁點選刪除，避免繼續收到申請。'
        email.attach(MIMEText(inner))
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("tacktechofficial@gmail.com",
                           "ndticvekvhfviilf")  # 登入寄件者gmail
                smtp.send_message(email)  # 寄送郵件
                print("Complete!")
                return render_template('home.html')
            except Exception as e:
                print("Error message: ", e)
                return render_template('home.html')


@app.route('/delete', methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "GET":
        return redirect(url_for("home"))
    elif request.method == "POST":
        del_num = request.form.get('del_num')
        k = Product.query.filter_by(id=del_num).first()
        db.session.delete(k)
        db.session.commit()
        return redirect(url_for("home"))


if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8080, debug=True)

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    app.secret_key = "12987987"
