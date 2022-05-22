import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_hospital_profile = Blueprint("app_hospital_profile", __name__, url_prefix="/hospital/profile",
                                 template_folder='templates', static_folder='../../static')


sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

# import utils
import hospital_queries as hq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_hospital_profile.route('/view')
def view_profile():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        email = session['hospitalId']
        details = hq.get_hospital_account_details(email)
        return render_template('hospital/profile/view_profile.html', details=details)


@app_hospital_profile.route('/password_change')
def password_change():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        return render_template('hospital/profile/psw_change.html')


@app_hospital_profile.route('/emergency_needs')
def emergency_needs():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        return render_template('hospital/emergency/emergency_needs.html')


@app_hospital_profile.route('/update_account_details', methods=['GET', 'POST'])
def update_account_details():

    if request.method == "POST":

        if 'hospitalId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')

            email = session['hospitalId']

            if (len(name) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                data = {
                    'name': name,
                    'email': email
                }

                # Update
                is_updated = hq.update_hospital_details(data)
                if is_updated > 0:
                    return jsonify({'success': "Account details has been updated!"})

                else:
                    return jsonify({'error': "Account details not updated. Please try again!"})

    return jsonify({'redirect': url_for('account')})


# Route for update user psw
@app_hospital_profile.route('/update_psw', methods=['GET', 'POST'])
def update_psw():

    if request.method == "POST":

        if 'hospitalId' not in session:
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
                email = session["hospitalId"]
                is_updated = hq.update_hospital_psw(email, psw)
                if is_updated > 0:
                    return jsonify({'success': "Account password has been updated!"})

                else:
                    return jsonify({'error': "Account password not updated. Please try again!"})

    return jsonify({'redirect': url_for('account')})
