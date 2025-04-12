# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import requests

headers = {
    "User-Agent": "Mozilla/5.0"  # Pretend you're a browser
}

app = Flask(__name__)


def check(email):
    url = "https://7zkadh4clc.execute-api.ap-south-1.amazonaws.com/plasma/getData?email=" + email
    status = requests.request("GET", url)
    print(status.json())
    return status.json()


@app.route('/registration')
def home():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    print(x)
    params = "name=" + x[0] + "&email=" + x[1] + "&phone=" + x[2] + "&city=" + x[3] + "&infect=" + x[4] + "&blood=" + x[
        5] + "&password=" + x[6]

    if ('errorType' in check(x[1])):
        url = "https://7zkadh4clc.execute-api.ap-south-1.amazonaws.com/plasma/registration?" + params
        response = requests.get(url)
        return render_template('register.html', pred="Registration Successful, please login using your details")
    else:
        return render_template('register.html', pred="You are already a member, please login using your details")


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/loginpage', methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    print(user, passw)
    data = check(user)
    if ('errorType' in data):
        return render_template('login.html', pred="The username is not found, recheck the spelling or please register.")
    else:
        if (passw == data['password']):
            return redirect(url_for('stats'))
        else:
            return render_template('login.html', pred="Login unsuccessful. You have entered the wrong password.")


@app.route('/stats')
def stats():
    url = "https://7zkadh4clc.execute-api.ap-south-1.amazonaws.com/plasma/getBloodGroupsData"
    response = requests.get(url)
    r = response.json()
    print(r)
    return render_template('stats.html', b=sum(r), b1=str(r[0]), b2=str(r[1]), b3=str(r[2]), b4=str(r[3]), b5=str(r[4]),
                           b6=str(r[5]), b7=str(r[6]), b8=str(r[7]))


@app.route('/requester')
def requester():
    return render_template('request.html')


@app.route('/requested', methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    # print(bloodgrp)
    url = "https://7zkadh4clc.execute-api.ap-south-1.amazonaws.com/plasma/requestOnBloodGroup?blood=" + bloodgrp
    status = requests.request("GET", url)
    a = status.json()
    phone = []

    for i in a:
        phone_number = str(i['phone']).strip()

        sms8_url = f"https://app.sms8.io/services/send.php?key=135005afeefa5f0fbf5ee697c17d7fbaa9bfb88f&message=Greetings+Sir/+Madam.+I+am+from+KLH+Plasma+Donor+Team.+I+need+plasma+of+your+Group+in+Emergency.+Please+kindly+contact%3A+9515387483&devices=2479&type=sms&prioritize=0&number={phone_number}"

        result = requests.get(sms8_url, headers=headers)
        print(f"Sent to {phone_number}: {result.status_code}, Response: {result.text}")

        phone.append(phone_number)

    print(phone)

    return render_template('request.html', pred="Your request is sent to the concerned people.")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

