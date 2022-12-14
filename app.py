#from crypt import methods
import flask
from flask import Flask , render_template , url_for , request , jsonify , redirect , session, g
import tensorflow
import jinja2
from datetime import datetime
import joblib
import DiabetesMain as dia
import Heart_Disease_Main as hrt
import Mental_Health_Main as mlh
import Stroke_Main as stm
import sqlite3
import Cluster_Main as CM

app = Flask(__name__)
app.secret_key = "URRSWE_1234"

# for home page clear
@app.route("/")
def home():
   return render_template("index.html")

@app.route("/health_tips.html") 
def fun_11():
    return render_template('health_tips.html')

@app.route("/health_tips.html" ,methods = ['POST', 'GET'])
def fun_12():
        TotalSteps = request.form["TotalSteps"]
        TotalDistance = request.form["TotalDistance"]
        VeryActiveDistance = request.form["VeryActiveDistance"]
        VeryActiveMinutes = request.form["VeryActiveMinutes"]
        SedentaryMinutes = request.form["SedentaryMinutes"]
        Calories = request.form["Calories"]
        WeightKg = request.form["WeightKg"]
        BMI = request.form["BMI"]
        Value = request.form["Value"]
        AverageIntensity = request.form["AverageIntensity"]
        TotalTimeInBed = request.form["TotalTimeInBed"]

        res = CM.tips_pred(TotalSteps,TotalDistance,VeryActiveDistance,VeryActiveMinutes,SedentaryMinutes,Calories,WeightKg,BMI,Value,AverageIntensity,TotalTimeInBed)
        X=str(res)

        
        if (X=='[0]'):
            X='You need to maintain a good diet'
        elif(X=='[1]'):
            X='You are maintaining an average lifestyle, keep up with it'
        elif(X=='[2]'):
            X='You need to maintain a diet and need to increase your workout hours'
        else:
            X='You need to maintain a good diet with good workout hours, we recommend you to consult a dietician for the same.'
        return render_template("health_tips.html",data_pred=X)

#for choice page
@app.route("/choice.html")
def diagnose():
    return render_template("choice.html")

#for diabeties form
@app.route('/dia_form.html')
def dispform():
    return render_template("dia_form.html")
#form k badd ka isko link krna h main prediction model se

def get_diaDB():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database_  = sqlite3.connect("dia_pred.db")
        cursor_dia = db.cursor()
    return cursor_dia

@app.route('/dia_form.html', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        
        bmi = request.form["BMI"]
        Income = request.form["Income"]
        PhysHlth = request.form["PhysHlth"]
        Age = request.form["Age"]
        GenHlth = request.form["GenHlth"]
        HighBP = request.form["HighBP"]
        HighChol = request.form["HighChol"]
        Smoker = request.form["Smoker"]
        Stroke = request.form["Stroke"]
        HeartDiseaseorAttack = request.form["HeartDisease"]
        PhysActivity = request.form["PhysActivity"]
        Veggies = request.form["Veggies"]
        HvyAlcoholConsump = request.form["HeavyAlcoholConsump"]
        DiffWalk = request.form["DiffWalk"]
        Sex = request.form["Sex"]

        X=dia.Predict_dia(bmi,Income,PhysHlth,Age,GenHlth,HighBP,HighChol,Smoker,Stroke,HeartDiseaseorAttack,PhysActivity,Veggies,HvyAlcoholConsump,DiffWalk,Sex)
        res = str(X)

        if(res=='[0]'):
            return render_template('Diabetes1.html')
        else:
            return render_template("Diabetes2.html")

@app.route('/bg.html')
def resultpage_dia():
    return render_template("bg.html")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database',None)
    if db is not None:
        db.close()

@app.route('/Stroke_Form.html')
def resultpage_Stroke():
    return render_template("Stroke_Form.html")

@app.route("/Stroke_Form.html", methods = ["POST","GET"])
def fun1():
    if request.method =="POST":
        gender = request.form.get("gender")
        age = request.form["age"]
        hypertension = request.form.get("hypertension")
        heart_disease = request.form.get("heart_disease")
        ever_married = request.form.get("ever_married")
        work_type = request.form.get("work_type")
        Residence_type = request.form.get("Residence_type")
        avg_glucose_level = request.form["avg_glucose_level"]
        bmi = request.form["bmi"]
        smoking_status = request.form.get("smoking_status")
        
        w = stm.Predictions(gender, age, hypertension, heart_disease, ever_married,work_type,Residence_type,avg_glucose_level,bmi,smoking_status)
    
        res1 = str(w)
        if(res1 == 'tf.Tensor([[0.]], shape=(1, 1), dtype=float32)'):
            return render_template('stroke1.html')
        else:
            return render_template("stroke2.html")

@app.route("/Mental_Form.html")
def mental():
    return render_template("Mental_Form.html")
@app.route("/Mental_Form.html" , methods = ['POST','GET'])
def mental1():
        Age = request.form['Age']
        Gender =  request.form.get("Gender")
        Country = request.form.get("Country")
        self_employed = request.form.get("self_employed")
        family_history = request.form.get("family_history")
        treatment = request.form.get("treatment")
        work_interfere = request.form.get("work_interfere")
        no_employees = request.form.get("no_employees")
        remote_work = request.form.get("remote_work")
        tech_company = request.form.get('tech_company')
        benefits = request.form.get("benefits")
        care_options = request.form.get("care_options")
        wellness_program = request.form.get("wellness_program")
        seek_help = request.form.get("seek_help")
        anonymity = request.form.get("anonymity")
        leave = request.form.get("leave")
        phys_health_consequence = request.form.get("phys_health_consequence")
        coworkers = request.form.get("coworkers")
        supervisor = request.form.get("supervisor")
        mental_health_interview = request.form.get("mental_health_interview")
        phys_health_interview = request.form.get("phys_health_interview")
        mental_vs_physical = request.form.get("mental_vs_physical")
        obs_consequence = request.form.get("obs_consequence")

        Y = mlh.predict(Age,Gender,Country,self_employed,family_history,treatment,work_interfere,no_employees,remote_work,tech_company,benefits,care_options,wellness_program,seek_help,anonymity,leave,phys_health_consequence,coworkers,supervisor,mental_health_interview,phys_health_interview,mental_vs_physical,obs_consequence)
        res3 = str(Y)

        if(res3=='[0]'):
            return render_template('Mental1.html') 
        elif(res3=='[1]'):
            return render_template('Mental2.html')
        else:
            return render_template('Mental3.html')

     

@app.route("/Heart_Form.html")
def fun():
    return render_template("Heart_Form.html")    

@app.route("/Heart_Form.html",methods = ["POST" , "GET"])
def heart():
       
        cp = request.form["cp"]
        age = request.form["Age"]
        sex = request.form["Sex"] 
        trestbps = request.form["Resting_Blood_Pressure"]
        chol = request.form["Cholestoral"]
        fbs = request.form["Fasting Blood Sugar"]
        restecg = request.form["Resting ECG"]
        thalatc = request.form["Max Heart Rate"]
        exang = request.form["Exercise_induced_angina"]
        Oldpeak  = request.form["ST_Depression"]
        slope = request.form["Slope_of_peak_exercise"]
        ca= request.form["ca"]
        thal=request.form["thal"]
        z = hrt.Predictions_hrt(age,cp,age,sex,trestbps,chol,fbs,restecg,thalatc,exang,Oldpeak,slope,ca,thal)   
        res = str(z)
        if(res == '[0]'):
            return render_template('Heart1.html')
        else:
            return render_template("Heart2.html")


     

if __name__ == "__main__":
    app.run(debug = True)   


@app.teardown_appcontext
def close_connection1(exception):
    db = getattr(g, '_database',None)
    if db is not None:
        db.close()

#for form access
#@app.route("/form.html")
#def form():
#   return render_template("form.html")
#after form filling and for giving result
#@app.route("/result") 
#def result():
#   return request("Diabetes.ipynb") 






















#html k files k reference proper ---------------------------------------------->done
#form k elements k name dena proper na------------------------------------------->baki
#<input type="radio" name="gender" id="dot-------------------------------------baki
#index.html k badd new page pr redirect result k liye 
#home page will redirect to choice.html ------------------------------------>done
#button will redirect to disease page -----------------------------------.done
#diab ka route usme form hoga fill krna and save it ------------>baki
#analysis k badd info pass hoga in form of dict -------------------->baki
# result on new page . ------------.baki
#



#vs code todo download. --------------->done
#html page banana with 4 options and shall go to form and bharne k badd diagnose button work ------------>done
#diagnose route new request.form form save in sql alchemy ---------->not required
#sqllite better abhi k liye.
#request.form= dictionary (json hota h)
# access krne k




