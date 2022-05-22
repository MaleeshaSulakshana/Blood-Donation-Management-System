import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin_hospital = Blueprint("app_admin_hospital", __name__, url_prefix="/admin/hospital",
                               template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import hospital_queries as hq
import users_queries as uq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_admin_hospital.route('/')
def view_hospitals():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        details = hq.get_all_hospitals()
        return render_template('admin/hospital/view_hospitals.html', details=details)


@app_admin_hospital.route('/add')
def add_hospital():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        return render_template('admin/hospital/add_hospital.html')


@app_admin_hospital.route('/view')
def view():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        id = request.args['id']
        details = hq.get_hospital_account_details(id)
        return render_template('admin/hospital/view_hospital_details.html', details=details)


# Route for add hospital
@app_admin_hospital.route('/add_hospital_details', methods=['GET', 'POST'])
def add_hospital_details():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            address = request.form.get('address')
            number = request.form.get('number')
            email = request.form.get('email')
            psw = request.form.get('psw')

            if (len(name) == 0 or len(address) == 0 or len(number) == 0 or len(email) == 0 or len(psw) == 0):

                return jsonify({'error': "Fields are empty!"})
            elif ut.validate_email(email) == False:
                return jsonify({'error': "Email not valid. Please check your email!"})

            else:
                psw = hashlib.md5(psw.encode()).hexdigest()

                data = {
                    'name': name,
                    'address': address,
                    'number': number,
                    'email': email,
                    'psw': psw
                }

                # Check email already exist
                is_exist = uq.is_exist_email(email)
                if is_exist[0][0] > 0:
                    return jsonify({'error': "Email already exist!"})

                else:
                    is_created = hq.hospital_registration(data)
                    if is_created > 0:
                        return jsonify({'success': "Hospital account has been created. Please sign in!"})

                    else:
                        return jsonify({'error': "Hospital account not created. Please try again!"})

    return jsonify({'redirect': url_for('index')})


@app_admin_hospital.route('/remove', methods=['GET', 'POST'])
def remove():

    email = request.form.get('id')
    is_removed = hq.remove_hospital(email)

    if is_removed > 0:
        return jsonify({'success': "Hospital Remove successfull!"})

    else:
        return jsonify({'error': "Hospital Remove not successfull. Please try again!"})
