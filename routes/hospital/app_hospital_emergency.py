import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_hospital_emergency = Blueprint("app_hospital_emergency", __name__, url_prefix="/hospital/emergency",
                                   template_folder='templates', static_folder='../../static')


sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

# import utils
import emergency_queries as eq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_hospital_emergency.route('/needs')
def needs():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        email = session['hospitalId']
        details = eq.get_hospital_emergency_need_details(email)
        return render_template('hospital/emergency/view_emergency_needs.html', details=details)


@app_hospital_emergency.route('/add')
def add():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        return render_template('hospital/emergency/add_emergency_need.html')


@app_hospital_emergency.route('/view')
def view():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        id = request.args['id']
        details = eq.get_emergency_need_details_by_id(int(id))
        return render_template('hospital/emergency/view_emergency_need_details.html', details=details)


# Route for add campaign
@app_hospital_emergency.route('/add_emergency_need', methods=['GET', 'POST'])
def add_emergency_need():

    if request.method == "POST":

        if 'hospitalId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            title = request.form.get('title')
            desc = request.form.get('desc')

            today = datetime.now().strftime("%Y-%m-%d")

            if (len(title) == 0 or len(desc) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                hospital_id = session['hospitalId']

                data = {
                    'title': title,
                    'desc': desc,
                    'today': today,
                    'hospital_id': hospital_id
                }

                is_created = eq.add_emergency_need(data)
                if is_created > 0:
                    return jsonify({'success': "Emergency need added successfull!"})

                else:
                    return jsonify({'error': "Emergency need added not successfull. Please try again!"})

    return jsonify({'redirect': url_for('index')})


@app_hospital_emergency.route('/remove', methods=['GET', 'POST'])
def remove():

    id = request.form.get('id')
    is_removed = eq.remove_emergency_need(int(id))

    if is_removed > 0:
        return jsonify({'success': "Emergency need remove successfull!"})

    else:
        return jsonify({'error': "Emergency need remove not successfull. Please try again!"})
