import os
import sys
import hashlib
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin_admin = Blueprint("app_admin_admin", __name__, url_prefix="/admin/admin",
                            template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import admin_queries as aq
import users_queries as uq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_admin_admin.route('/')
def view_admins():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    details = aq.get_all_admins(session['adminId'])
    return render_template('admin/admin/view_admins.html', details=details)


@app_admin_admin.route('/add')
def add_admins():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    return render_template('admin/admin/add_admin.html')


# Route for add admin
@app_admin_admin.route('/add_admin_details', methods=['GET', 'POST'])
def add_admin_details():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            email = request.form.get('email')
            psw = request.form.get('psw')

            if (len(name) == 0 or len(email) == 0 or len(psw) == 0):

                return jsonify({'error': "Fields are empty!"})
            elif ut.validate_email(email) == False:
                return jsonify({'error': "Email not valid. Please check your email!"})

            else:
                psw = hashlib.md5(psw.encode()).hexdigest()

                data = {
                    'name': name,
                    'email': email,
                    'psw': psw
                }

                # Check email already exist
                is_exist = uq.is_exist_email(email)
                if is_exist[0][0] > 0:
                    return jsonify({'error': "Email already exist!"})

                else:
                    is_created = aq.admin_registration(data)
                    if is_created > 0:
                        return jsonify({'success': "Admin account has been created. Please sign in!"})

                    else:
                        return jsonify({'error': "Admin account not created. Please try again!"})

    return jsonify({'redirect': url_for('index')})


@app_admin_admin.route('/remove_admin', methods=['GET', 'POST'])
def remove_admin():

    email = request.form.get('id')

    is_updated = aq.remove_admin(email)
    if is_updated > 0:
        return jsonify({'success': "Admin Remove successfull!"})

    else:
        return jsonify({'error': "Admin Remove not successfull. Please try again!"})
