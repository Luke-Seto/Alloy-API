from flask import Flask, render_template, jsonify,request,g,redirect,flash,url_for,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import requests

#Alloy Call
url = "https://sandbox.alloy.co/v1/evaluations"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
	#Add ALLoy API Key
    "authorization": "Basic"
}

app = Flask(__name__) # Flask constructor 
app.secret_key = '1001'

#Start Page
@app.route('/')
def index():
	return render_template("alloy.html")
#Form Submit
@app.route('/submit', methods=['GET', 'POST'])
def sub():
	#Trigger popup
	trigger_js = True
	#Form
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	ssn = request.form['ssn']
	email = request.form['email']
	addressLine1 = request.form['addressLine1']
	addressLine2 = request.form['addressLine2']
	city = request.form['city']
	state = request.form['state']
	zipCode = request.form['zipCode']
	country = request.form['country']
	dateOfBirth = request.form['dateOfBirth']
	#firstName= str(firstName)
	#Create Alloy Payload
	payload = {
	"name_first": firstName,
	"name_last": lastName,
    "document_ssn": ssn,
    "email_address": email,
        "address": {
            "line1": addressLine1,
            "line2": addressLine2,
            "city": city,
            "state": state,
            "postal_code": zipCode,
            "country_code": country
        },
	"birth_date":dateOfBirth
    }
	#Alloy Send Reqeust to evaluations
	response = requests.post(url, json=payload, headers=headers)
	response = response.json()
	#Pull the out come
	outcome= str(response['summary']['outcome'])
	outcome= str(outcome)
	print(outcome) 	
	return render_template("alloy.html", firstName=firstName, trigger_js =trigger_js,outcome=outcome,lastName=lastName)


if __name__=='__main__': 
	app.run(port=8009) 
