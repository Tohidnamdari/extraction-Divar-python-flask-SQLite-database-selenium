from flask import Flask,render_template,request,redirect,make_response,flash
from selenium import webdriver
from time import sleep
from database import db
db.create_all()
from database import home,Users
from database import app


@app.route('/about',methods=['GET','POST'])
def about():

    return render_template('about.html',user=request.cookies.get("user"))


@app.route("/logout")
def logout():
    flash("کاربر خارج شد", "danger")
    response = make_response(redirect('/login'))
    response.delete_cookie("user")
    return response
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        found=False
        for u in range(len(Users.query.all())):
            if username==Users.query.all()[u].username and password==Users.query.all()[u].password:
                flash("کاربر وارد شد", "success")
                response=make_response(redirect('/'))
                response.set_cookie("user",username)
                found = True
                return response
        if found==False:
                flash("نام کاربری یا رمز عبور اشتباه است", "danger")
                return render_template('login.html')
    return render_template('login.html',user=request.cookies.get("user"))


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        if password==re_password and len(password)==8:
            flash("کاربر ثبت نام شد", "success")
            admin1=Users(username=username,password=password)
            db.session.add(admin1)
            db.session.commit()
            return redirect('/')
        else:
            flash("رمز عبور با تکرار ان همخوانی ندارد یا تعداد ارقام  رمز عبور کمتر از 8 میباشد ", "danger")

            return redirect('/register')
    else:
        return render_template('register.html',user=request.cookies.get("user"))

@app.route('/result_by_all_sort',methods=['GET','POST'])
def result_by_all_sort():
    if request.cookies.get("user"):
        for all_sort in range(len(home.query.all())):
            select_sort = home.query.all()[all_sort].allmony
            split_sort = select_sort.split(" ")
            split_sort_2 = split_sort[0].split("٬")
            result = ""
            for all_split in range(len(split_sort_2)):
                result += split_sort_2[all_split]
            end_sort = home.query.all()[all_sort]
            end_sort.all_int = result
            db.session.commit()

        order_sort = home.query.order_by(home.all_int).all()




        return render_template('result_by_all_sort.html',user=request.cookies.get("user"),items=len(home.query.all()),pages_banck1=order_sort)
    else:
        return redirect('/login')
@app.route('/result_by_sort',methods=['GET','POST'])
def result_by_sort():
    if request.cookies.get("user"):
        for all_sort in range(len(home.query.all())):
            get_sort = home.query.all()[all_sort].mony
            split_sort= get_sort.split(" ")
            filter_sort = split_sort[0].split("٬")
            result_filter = ""
            for extract in range(len(filter_sort)):
                result_filter += filter_sort[extract]
            end_sort = home.query.all()[all_sort]
            end_sort.mony_int = result_filter
            db.session.commit()

        sort_order = home.query.order_by(home.mony_int).all()

        return render_template('result_by_sort.html',user=request.cookies.get("user"),items=len(home.query.all()),pages_banck1=sort_order)
    else:
        return redirect('/login')


@app.route('/result_extraction',methods=['GET','POST'])
def result_extraction():
    if request.cookies.get("user"):
        return render_template('result_extraction.html',user=request.cookies.get("user"),pages_banck1=home.query.all(),items=len(home.query.all()))
    else:
        return redirect('/login')
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html',user=request.cookies.get("user"))
@app.route('/search',methods=['GET','POST'])
def search():
    global Number_ph
    if request.cookies.get("user"):
        if request.method == 'POST':
                driver = webdriver.Chrome('./chromedriver.exe')
                metr1 = request.form.get('metr')
                metr2 = request.form.get('metr1')
                mony1= request.form.get('mony1')
                mony2= request.form.get('mony2')
                city = request.form.get('city')
                driver.get("https://divar.ir/s/saveh/buy-apartment?price="+mony1+"-"+mony2+"&"+"size="+metr1+"-"+metr2)
                title = driver.find_elements_by_class_name("kt-post-card__title")
                for i in range(len(title)):
                    name=title[i].text
                    title[i].click()
                    print(driver.title)
                    sleep(2)
                    Information = driver.find_elements_by_class_name("kt-unexpandable-row__value")
                    if Information[0]:

                        metr=Information[0].text


                    if Information[1]:
                        allmony=Information[1].text


                    if Information[2]:
                       mony=Information[2].text


                    if Information[3]:
                       karbar=Information[3].text



                    sleep(2)
                    Information2=driver.find_elements_by_class_name("kt-group-row-item__value")
                    if Information2:
                        tabage=Information2[0].text


                        salsakht=Information2[1].text


                        room=Information2[2].text


                    sleep(3)


                    sleep(3)
                    if Information[3].text=="همکف":
                        tabage = Information[3].text
                    else:
                        e= Information[3].text.split("از")
                        tabage=e[0]
                    salsakht = Information2[1].text

                    room = Information2[2].text
                    metr =Information2[0].text
                    allmony = Information[0].text
                    mony = Information[1].text
                    karbar = Information[2].text
                    admin = home(name=name, metr=metr, allmony=allmony, mony=mony, karbar=karbar, tabage=tabage,
                                 salsakht=salsakht, room=room)
                    db.session.add(admin)
                    db.session.commit()
                    sleep(1)
                    driver.back()
                    title = driver.find_elements_by_class_name("kt-post-card__title")  # تمام المنت ها رو باز توی متغیر میزیزیم تا روش کلیک بشه
                    sleep(1)

                return render_template('search.html',user=request.cookies.get("user"))
        return render_template('search.html',user=request.cookies.get("user"))
    else:
        return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html'), 404
if __name__=='__main__':
    app.run(host='0.0.0.0',port=80)