import os
import sys
import random
import hashlib
from datetime import datetime, date
import paypalrestsdk
from flask import Flask, render_template, redirect, jsonify, url_for, request, session

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))
sys.path.append(os.path.abspath('python/detection'))

sys.path.append(os.path.abspath('routes/'))
sys.path.append(os.path.abspath('routes/admin'))
sys.path.append(os.path.abspath('routes/organization'))
sys.path.append(os.path.abspath('routes/hospital'))

# import Predictions
import users_queries as uq
import organizations_queries as oq
import donation_queries as dq
import campaigns_queries as cq
import appointments_queries as aq
import emergency_queries as eq
import donation_details_queries as ddq

import diabetes_prediction as detection

import utils

# Import admin route files
from app_admin import app_admin
from app_admin_organization import app_admin_organization
from app_admin_campaign import app_admin_campaign
from app_admin_donor import app_admin_donor
from app_admin_money_donations import app_admin_money_donations
from app_admin_hospital import app_admin_hospital
from app_admin_admin import app_admin_admin
from app_admin_profile import app_admin_profile
from app_admin_emergency import app_admin_emergency

# Import organization route files
from app_organization import app_organization
from app_organization_profile import app_organization_profile
from app_organization_donor import app_organization_donor
from app_organization_campaign import app_organization_campaign

# Import hospital route files
from app_hospital import app_hospital
from app_hospital_profile import app_hospital_profile
from app_hospital_donor import app_hospital_donor
from app_hospital_campaign import app_hospital_campaign
from app_hospital_emergency import app_hospital_emergency

app = Flask(__name__)

# Blueprints admin
app.register_blueprint(app_admin)
app.register_blueprint(app_admin_organization)
app.register_blueprint(app_admin_campaign)
app.register_blueprint(app_admin_donor)
app.register_blueprint(app_admin_money_donations)
app.register_blueprint(app_admin_hospital)
app.register_blueprint(app_admin_admin)
app.register_blueprint(app_admin_profile)
app.register_blueprint(app_admin_emergency)

# Blueprints organization
app.register_blueprint(app_organization)
app.register_blueprint(app_organization_profile)
app.register_blueprint(app_organization_donor)
app.register_blueprint(app_organization_campaign)

# Blueprints hospital
app.register_blueprint(app_hospital)
app.register_blueprint(app_hospital_profile)
app.register_blueprint(app_hospital_donor)
app.register_blueprint(app_hospital_campaign)
app.register_blueprint(app_hospital_emergency)

app.secret_key = "Blood_Donation"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Paypal config
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AUtF6tURfnKEvFxcpm469SO7UBoSOvFS1fi3SRPifKPe5Dwn7ubjcpi-dJEfAY2_AeAga3Im5139GNwd",
    "client_secret": "EPeqL9L5Dd7HFUeAYkReyA0057Z8h5dh7AFAqBBa5mIFf6NNMTJ_HPkjfnUON4tWI4Pilcv03JPUKAAF"})


# Create the folder structure
def genarate_folder():
    # Get date and time
    date_time = datetime.now()
    date_time = str(date_time.strftime("%d_%m_%Y_%H_%M_%S"))

    # Get random number
    random_no = str(random.randint(100000, 999999))

    # Paths
    folder_name = date_time + "_" + random_no + "/"
    folder_path = os.path.join(APP_ROOT, 'upload_images/')
    input_img = os.path.join(folder_path, folder_name)
    uploaded_img_path = os.path.join(input_img, 'images/')

    # Genarate folders
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    if not os.path.isdir(input_img):
        os.mkdir(input_img)

    if not os.path.isdir(uploaded_img_path):
        os.mkdir(uploaded_img_path)

    return input_img, uploaded_img_path


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/campaigns')
def campaigns():

    today = date.today().strftime("%Y-%m-%d")
    details = cq.get_up_coming_campaigns(today)
    return render_template('campaigns.html', details=details)


@app.route('/organizations')
def organizations():

    today = date.today().strftime("%Y-%m-%d")
    details = oq.get_all_organizations(1)
    return render_template('organizations.html', details=details)


@app.route('/appointments')
def appointments():

    today = date.today().strftime("%Y-%m-%d")
    details = aq.all_upcoming_appointments(session['userId'], today)
    return render_template('appointments.html', details=details)


@app.route('/emergency')
def emergency():

    details = eq.get_all_emergency_needs()
    return render_template('emergency.html', details=details)


@app.route('/campaign-details')
def campaign_details():

    id = request.args['id']
    email = ''
    if 'userId' in session:
        email = session['userId']

    details = cq.get_campaigns_details(id)
    donor = uq.get_donor_details(email)

    is_exist = str(aq.is_appointment_exist(id, email)[0][0])

    return render_template('campaign-details.html', details=details, donor=donor, is_exist=is_exist)


# Route for sign up page
@app.route('/sign-up')
def sign_up():
    if 'userId' in session:
        return redirect('/index')
    else:
        return render_template('sign-up.html')


# Route for sign up organization page
@app.route('/sign-up-organization')
def sign_up_organization():
    if 'userId' in session:
        return redirect('/index')
    else:
        return render_template('sign-up-organization.html')


# Route for sign in page
@app.route('/sign-in')
def sign_in():
    if 'userId' in session:
        return redirect('/index')
    else:
        return render_template('sign-in.html')


# Route for profile page
@app.route('/account')
def account():
    if 'userId' not in session:
        return redirect('/sign-in')
    else:

        email = session['userId']
        details = uq.get_donor_details(email)
        donations = ddq.all_donation_details_by_donor(email)

        return render_template('account.html', details=details, donations=donations)


# Route for profile psw change page
@app.route('/psw-change')
def psw_change():
    if 'userId' not in session:
        return redirect('/sign-in')
    else:
        email = session['userId']
        details = uq.get_donor_details(email)
        return render_template('psw-change.html', details=details)


# Route for money donation page
@app.route('/money-donation')
def money_donation():
    return render_template('money-donation.html')


# Route for get campaigns
@app.route('/all_campaigns', methods=['GET', 'POST'])
def all_campaigns():

    today = date.today().strftime("%Y-%m-%d")
    details = cq.get_up_coming_campaigns(today)
    return jsonify(details)


# Route for register
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():

    if request.method == "POST":

        if 'userId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            email = request.form.get('email')
            dob = request.form.get('dob')
            gender = request.form.get('gender')
            b_type = request.form.get('b_type')
            number = request.form.get('number')
            nic = request.form.get('nic')
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(name) == 0 or len(email) == 0 or len(dob) == 0 or
                len(gender) == 0 or len(b_type) == 0 or len(number) == 0 or
                    len(nic) == 0 or len(psw) == 0 or len(cpsw) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            elif utils.validate_email(email) == False:
                return jsonify({'error': "Email not valid. Please check your email!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()
                data = {
                    'email': email,
                    'psw': psw,
                    'full_name': name,
                    'dob': dob,
                    'gender': gender,
                    'blood_type': b_type,
                    'phone_number': number,
                    'nic': nic,
                    'is_approved': 0
                }

                # Check email already exist
                is_exist = uq.is_exist_email(email)
                if is_exist[0][0] > 0:
                    return jsonify({'error': "Email already exist!"})

                else:
                    is_created = uq.registration(data)
                    if is_created > 0:
                        return jsonify({'success': "Account has been created. Please sign in!"})

                    else:
                        return jsonify({'error': "Account not created. Please try again!"})

    return jsonify({'redirect': url_for('sign-up')})


# Route for register
@app.route('/organization_register', methods=['GET', 'POST'])
def organization_register():

    if request.method == "POST":

        if 'userId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            email = request.form.get('email')
            hod = request.form.get('hod')
            location = request.form.get('location')
            number = request.form.get('number')
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(name) == 0 or len(email) == 0 or len(hod) == 0 or
                    len(location) == 0 or len(number) == 0 or len(psw) == 0 or len(cpsw) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            elif utils.validate_email(email) == False:
                return jsonify({'error': "Email not valid. Please check your email!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()
                data = {
                    'name': name,
                    'email': email,
                    'hod': hod,
                    'location': location,
                    'number': number,
                    'psw': psw,
                    'is_approved': 0
                }

                # Check email already exist
                is_exist = uq.is_exist_email(email)
                if is_exist[0][0] > 0:
                    return jsonify({'error': "Email already exist!"})

                else:
                    is_created = oq.organization_registration(data)
                    if is_created > 0:
                        return jsonify({'success': "Organization account has been created. Please sign in!"})

                    else:
                        return jsonify({'error': "Organization account not created. Please try again!"})

    return jsonify({'redirect': url_for('sign_up_organization')})


# Route for login user
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if request.method == "POST":

        if 'userId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            email = request.form.get('email')
            psw = request.form.get('psw')

            if (len(email) == 0 or len(psw) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                # Check email already exist
                details = uq.login(email, psw)
                if len(details) > 0:
                    if int(details[0][2]) == 4:
                        session['userId'] = str(details[0][1])
                        return jsonify({'redirect': url_for('index')})

                    elif int(details[0][2]) == 3:
                        session['hospitalId'] = str(details[0][1])
                        return jsonify({'redirect': url_for('app_hospital.index')})

                    elif int(details[0][2]) == 2:
                        session['organizationId'] = str(details[0][1])
                        return jsonify({'redirect': url_for('app_organization.organization_index')})

                    elif int(details[0][2]) == 1:
                        session['adminId'] = str(details[0][1])
                        return jsonify({'redirect': url_for('app_admin.index')})

                else:
                    return jsonify({'error': "Sign in failed. Please try again!"})

    return jsonify({'redirect': url_for('sign-in')})


# Route for sign out
@app.route('/sign-out')
def signout():
    if 'userId' in session:
        session.pop('userId', None)

    return redirect(url_for('index'))


# Route for get account details
@app.route('/account_details', methods=['GET', 'POST'])
def account_details():

    if 'userId' not in session:
        return jsonify({'redirect': url_for('index')})

    else:
        email = session['userId']
        details = uq.get_account_details(email)
        data = {}

        if (len(details) > 0):
            data = {
                'email': details[0][0],
                'full_name': details[0][1],
                'dob': details[0][2],
                'gender': details[0][3],
                'blood_type': details[0][4],
                'phone_number': details[0][5],
                'nic': details[0][6]
            }

    return jsonify({'data': data})


# Route for update user details
@app.route('/update_user_details', methods=['GET', 'POST'])
def update_user_details():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            dob = request.form.get('dob')
            number = request.form.get('number')

            if (len(name) == 0 or len(dob) == 0 or len(number) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif (len(number) != 10 or number.isnumeric() == False):
                return jsonify({'error': "Please check mobile number!"})

            else:

                data = {
                    'name': name,
                    'email': session['userId'],
                    'dob': dob,
                    'number': number
                }

                # Update
                is_updated = uq.update_user_details(data)
                if is_updated > 0:
                    return jsonify({'success': "Account details has been updated!"})

                else:
                    return jsonify({'error': "Account details not updated. Please try again!"})

    return jsonify({'redirect': url_for('account')})


# Route for update user psw
@app.route('/update_user_psw', methods=['GET', 'POST'])
def update_user_psw():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(psw) == 0 or len(cpsw) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            else:

                # Update
                psw = hashlib.md5(psw.encode()).hexdigest()
                is_updated = uq.update_user_psw(session['userId'], psw)
                if is_updated > 0:
                    return jsonify({'success': "Account password has been updated!"})

                else:
                    return jsonify({'error': "Account password not updated. Please try again!"})

    return jsonify({'redirect': url_for('account')})


# Payment gateway for donation
@app.route('/payment', methods=['GET', 'POST'])
def payment():

    amount = request.form['amount']

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "amount": {
                "total": amount,
                "currency": "USD"},
            "description": "Meal master 30 days subscription payment."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id, 'amount': amount})


@app.route('/execute', methods=['POST'])
def execute():

    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):

        print('Execute success!')
        success = True

        name = request.form['name']
        email = request.form['email']
        amount = request.form['amount']
        payment_id = request.form['paymentID']
        today_date = datetime.today().strftime('%Y-%m-%d')

        data = {
            'name': name,
            'email': email,
            'amount': amount,
            'date': today_date,
            'payment_id': payment_id
        }

        is_submitted = dq.insert_donation(data)
        if is_submitted > 0:
            return jsonify({'success': "Payment Successfull.!"})

        else:
            return jsonify({'error': "Payment not successfull. Please try again!"})

    else:
        print(payment.error)
        return jsonify({'error': "Payment not successfull. Please try again!"})


# Route for add appointment
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            campaign_id = request.form.get('campaign_id')
            donor = request.form.get('donor')

            data = {
                'campaign_id': int(campaign_id),
                'donor': str(donor)
            }

            # Check email already exist
            is_exist = aq.is_appointment_exist(campaign_id, donor)
            if is_exist[0][0] > 0:
                return jsonify({'error': "Your appointment already exist!"})

            else:
                is_created = aq.appointments_registration(data)
                if is_created > 0:
                    return jsonify({'success': "Appointment created successfully!"})

                else:
                    return jsonify({'error': "Appointment created not successfully. Please try again!"})

    return jsonify({'redirect': url_for('sign-up')})


# Route for remove appointment
@app.route('/remove_appointment', methods=['GET', 'POST'])
def remove_appointment():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            campaign_id = request.form.get('campaign_id')
            donor = request.form.get('donor')

            # Check email already exist
            is_exist = aq.is_appointment_exist(campaign_id, donor)
            if is_exist[0][0] < 1:
                return jsonify({'error': "Your appointment not exist!"})

            else:
                is_removed = aq.remove_appointment(
                    int(campaign_id), str(donor))
                if is_removed > 0:
                    return jsonify({'success': "Appointment removed successfully!"})

                else:
                    return jsonify({'error': "Appointment removed not successfully. Please try again!"})

    return jsonify({'redirect': url_for('sign-up')})


# Route for detect diabetic
@app.route('/detect_diabetic', methods=['GET', 'POST'])
def detect_diabetic():

    if request.method == "POST":

        pregnancies = request.form.get('pregnancies')
        glucose = request.form.get('glucose')
        blood_pressure = request.form.get('blood_pressure')
        skin_thickness = request.form.get('skin_thickness')
        insulin = request.form.get('insulin')
        bmi = request.form.get('bmi')
        diabetes_pedigree_function = request.form.get(
            'diabetes_pedigree_function')
        age = request.form.get('age')

        if (len(pregnancies) == 0 or len(glucose) == 0 or len(blood_pressure) == 0 or
            len(skin_thickness) == 0 or len(insulin) == 0 or len(bmi) == 0 or
                len(diabetes_pedigree_function) == 0 or len(age) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            prediction = detection.detect_diabetes(
                pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age)

            return jsonify({'prediction': prediction})


# Main
if __name__ == '__main__':
    # host = "192.168.1.3"
    host = "0.0.0.0"
    port = "5000"
    app.run(host=host, port=port, debug=True)
