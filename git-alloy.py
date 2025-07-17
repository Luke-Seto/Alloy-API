from flask import Flask, render_template, jsonify,request,g,redirect,flash,url_for,session
import requests
from requests.auth import HTTPBasicAuth


#Gets API key from txt file
with open("alloy.txt", "r") as file:
	api_key = file.read().strip()
	token, secret = api_key.split(':')
	print("Token:", token)
	print("Secret:", secret)


#Alloy Call
url = "https://sandbox.alloy.co/v1/evaluations"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}

# Flask constructor 
app = Flask(__name__) 
app.secret_key = '1001'

#Start Page
@app.route('/')
def index():
	return render_template("alloy.html")


#Triggers from the Form Submit
@app.route('/submit', methods=['GET', 'POST'])
def sub():
	#Trigger popup
	trigger_js = True
	#Get Form Info to pass to API
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
	try:
	#Alloy Send Reqeust to evaluations
		response = requests.post(url, json=payload, headers=headers,auth=HTTPBasicAuth(token,secret),)
		response = response.json()
	#Parse the JSON
		outcome= str(response['summary']['outcome'])
		outcome= str(outcome)
		print(outcome)
	except:
		#API Error Handling 
		outcome='failed'
		print(response.status_code +'Ran into an issue from the API' ) 

	return render_template("alloy.html", firstName=firstName, trigger_js =trigger_js,outcome=outcome,lastName=lastName)


if __name__=='__main__': 
	app.run(port=8009) 