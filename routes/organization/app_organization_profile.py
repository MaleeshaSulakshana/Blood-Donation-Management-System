import os
import sys
import hashlib
from datetime import date
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_organization_profile = Blueprint("app_organization_profile", __name__, url_prefix="/organization/profile",
                                     template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import organizations_queries as oq
import campaigns_queries as cq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_organization_profile.route('/')
def view_profile():

    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        email = session['organizationId']

        details = oq.get_organization_account_details(email)
        return render_template('organization/profile/view_profile.html', details=details)


@app_organization_profile.route('/password_change')
def password_change():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        return render_template('organization/profile/psw_change.html')


@app_organization_profile.route('/history')
def history():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        email = session['organizationId']
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")

        campaigns = cq.get_completed_campaigns(
            date_str, session['organizationId'])
        return render_template('organization/profile/view_history.html', campaigns=campaigns)


@app_organization_profile.route('/update_organization_details', methods=['GET', 'POST'])
def update_organization_details():

    if request.method == "POST":

        if 'organizationId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            hod = request.form.get('hod')
            location = request.form.get('location')
            phone = request.form.get('phone')

            email = session['organizationId']

            if (len(name) == 0 or len(hod) == 0 or len(location) == 0 or
                    len(phone) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif (len(phone) != 10 or phone.isnumeric() == False):
                return jsonify({'error': "Please check mobile number!"})

            else:

                data = {
                    'name': name,
                    'hod': hod,
                    'location': location,
                    'phone': phone,
                    'email': email
                }

                # Update
                is_updated = oq.update_organization_details(data)
                if is_updated > 0:
                    return jsonify({'success': "Account details has been updated!"})

                else:
                    return jsonify({'error': "Account details not updated. Please try again!"})

    return jsonify({'redirect': url_for('account')})


# Route for update user psw
@app_organization_profile.route('/update_psw', methods=['GET', 'POST'])
def update_psw():

    if request.method == "POST":

        if 'organizationId' not in session:
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
                email = session["organizationId"]
                is_updated = oq.update_organization_psw(email, psw)
                if is_updated > 0:
                    return jsonify({'success': "Account password has been updated!"})

                else:
                    return jsonify({'error': "Account password not updated. Please try again!"})

    return jsonify({'redirect': url_for('account')})
