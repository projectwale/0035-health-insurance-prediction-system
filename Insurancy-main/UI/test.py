#pip install scikit-learn==1.2.2
# pip install rasa==2.0.2
# rasa run actions
# rasa run --cors "*" --enable-api
# pip install rasa-nlu==0.11.5
# greenlet==0.4.16
# pip install slackclient==1.3.1

# rasa train

from flask import Flask, render_template, request, session, url_for, redirect,flash,jsonify
import pymysql
from werkzeug.utils import secure_filename
import pathlib
import os
import pickle
import numpy as np
from mark_attendance import mark_your_attendance
from sklearn.ensemble import RandomForestRegressor
import json
import requests
from register import register_yourself

app = Flask(__name__)
app.secret_key = 'any random string'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/profile/'
app.config['UPLOADED_PHOTOS_DEST1'] = 'static/Insurance/'
output=[]#("message stark","hi")]


def calculate_insurance_score(age, gender, bmi, children, smoke, region):
    # Initialize base score
    score = 0
    
    # Age: Older individuals might have higher insurance scores
    score += age * 0.1
    
    # Gender: Male might have a different risk factor compared to female
    if gender == 1:  # Assuming 1 for male, 0 for female
        score += 5
    
    # BMI: Higher BMI might indicate higher health risks
    score += bmi * 0.3
    
    # Number of children: More children might indicate more responsibilities and potentially more stress
    score += children * 2
    
    # Smoking: Smoking increases health risks significantly
    if smoke == 1:
        score += 10
    
    # Region: Different regions might have different health risks
    if region == 1:  # Assuming different values represent different regions
        score += 3
    
    return score



def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="0035_health_insurance")
    return connection


def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        
        
                
con = dbConnection()
cursor = con.cursor()

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/index',methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route('/contact',methods=["GET","POST"])
def contact():
    
   return render_template('contact.html')

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    # username=session.get('uname')
    session.pop('userid',None)
    return redirect(url_for('main'))

@app.route('/about',methods=["GET","POST"])
def about():
    return render_template('about.html')



@app.route('/login', methods=["GET","POST"])
def login():
    msg = ''
    if request.method == "POST":
        # session.pop('user',None)
        email = request.form.get("email")
        password = request.form.get("Password")
        # print(mobno+password)

        marked,studentName = mark_your_attendance()
        if(marked == True):
            con = dbConnection()
            cursor = con.cursor()
            result_count = cursor.execute('SELECT * FROM registration WHERE Name=%s and Email = %s AND Password = %s',
                                        (studentName, email, password))
            res=cursor.fetchone()

        if result_count > 0:
            print(result_count)
            session['name']=res[1]
            session['id']=res[0]
            session['userid']=res[0]
            return redirect(url_for('index'))
        else:
            flash("You are not registered yet")
            print(result_count)
            msg = 'Incorrect username/password!'
            return redirect(url_for('login'))
        return redirect(url_for('login'))
    return render_template('login.html')




@app.route('/register',methods=["GET","POST"])  
def register():
    print("in")
    if request.method == "POST":
        print("hiii")
        name = request.form.get("name")
        Email = request.form.get("Email")
        Phone = request.form.get("Phone")
        Password = request.form.get("Password")
        Address = request.form.get("Address")
    
      
        marked = register_yourself(str(name),str(Email),str(Phone),str(Password),str(Address))
        print(marked)
        print("Registration Successful")
        message = "Registration successfully added by admin side"+" "+"username is-"+name
        
        return message
      
        
 
    return render_template('register.html')

@app.route('/service',methods=["GET","POST"])
def service():
    userid=session['userid']
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM registration WHERE Id = %s ', (userid))
    data1 = cursor.fetchone()
    print(data1)
    
    if request.method == 'POST':
       print("jhdjk")
       # Fetching values from the form
       age = int(request.form['age'])
       gender = int(request.form['Gender'])
       bmi = float(request.form['BMI'])
       childrence = int(request.form['Childrence'])
       smoke = int(request.form['Smoke'])
       region = int(request.form['Region'])

       # Now you have the form values, and you can use them for prediction or any other logic

       # Example: Printing the fetched values
       print("Age:", age)
       print("Gender:", gender)
       print("BMI:", bmi)
       print("Childrence:", childrence)
       print("Smoke:", smoke)
       print("Region:", region)
       
       features = [int(age),int(gender),int(bmi),int(childrence),int(smoke),int(region)]
       
       # print(features)
       
       Pkl_Filename = "rf_tuned.pkl" 
       with open(Pkl_Filename, 'rb') as file:  
           rf_tuned_loaded = pickle.load(file)
       
       pred=rf_tuned_loaded.predict(np.array(features).reshape(1,6))[0]
       print(pred)
       
       message = "Expected amount is " + str(pred)
       
       insurance_score = calculate_insurance_score(int(age), int(gender), int(bmi), int(childrence), int(smoke), int(region))
       print("Health Insurance Score:", insurance_score)  
        
      
       return jsonify({'pred': pred, 'massage': message,'insurance_score': insurance_score})
       
       
    return render_template('service.html',data1=data1)

####################################################################CHATBOT############################################################
@app.route('/getRequest1', methods=['POST'])
def getRequest1():
    print("GET")
    if request.method =='POST':
        print("Post")
     
        data = request.get_json()
        userText = data.get('userMessage')
   
        print(userText)
        data = json.dumps({"sender": "Rasa","message": userText})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
        res = res.json()
        print()
        print("Output")
        print(res)
        print()
        val = res[0]['text']
        output.append(val)
        print()
        print("val")
        print(val)
        print()
        responses = val
        print("=====================")
        print(responses)
        print("=====================")
        
        return responses
  

################################################################################################################################

@app.route('/Admin',methods=["GET","POST"])
def Admin():
    
    return render_template('Admin.html')

@app.route('/dashadmin',methods=["GET","POST"])
def dashadmin():
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM insurance')
    data = cursor.fetchall()
    print(data)
    return render_template('dashadmin.html',data=data)

@app.route('/addinsurance',methods=["GET","POST"])
def addinsurance():
    
    return render_template('addinsurance.html')


@app.route('/addin',methods=["GET","POST"])  
def addin():
    print("in")
    if request.method == "POST":
        print("hiii")
        name = request.form.get("NAME")
        insurancecost = request.form.get("insurancecost")
        insurancetype = request.form.get("insurancetype")
        
        Phone = request.form.get("Phone")
        Address = request.form.get("Address")
        usermassge = request.form.get("usermassge")
        
        uploadimg = request.files['file']
        
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM insurance WHERE name = %s', (name))
        res = cursor.fetchone()
        
        

        
        if not res:
            filename_secure = secure_filename(uploadimg.filename)
            uploadimg.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST1'], filename_secure))
            filenamepath = os.path.join(app.config['UPLOADED_PHOTOS_DEST1'], filename_secure)
            
            sql = "INSERT INTO insurance(name, insurancecost, insurancetype, Phone, Address,usermassge,filenamepath) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (name, insurancecost, insurancetype, Phone, Address,usermassge,filenamepath)
            cursor.execute(sql, val)
            con.commit()
    
            message = " AgencyName insurance was successfully added by the admin side. AgencyName: " + name
            # return redirect(url_for('index'))
            return jsonify({'message': message})
          
            
        else:
            message = " AgencyName insurance  not  added by admin side. AgencyName: " + name
            dbClose()
            # return redirect(url_for('index'))
            return jsonify({'message': message})
        
        
@app.route('/Recomdate', methods=['GET'])
def my_route():
    pred = request.args.get('pred')
    score = request.args.get('score')
    
    print()
    print("pred:",pred)
    print()
    print("score:",score)
    print()
    
   # Fetch insurance records where the insurance cost is less than the predicted value
    fetch_query = 'SELECT * FROM insurance WHERE insurancecost < %s'
    cursor.execute(fetch_query, (pred,))
    data = cursor.fetchall()
    print(data)

    return render_template('insurance.html',data=data,score=score,pred=pred)        

if __name__ == '__main__':
    # app.run(debug=True)
    app.run('0.0.0.0')