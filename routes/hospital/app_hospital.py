import os
import sys
import hashlib
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

from routes.hospital.app_hospital_profile import emergency_needs

app_hospital = Blueprint("app_hospital", __name__, url_prefix="/hospital",
                         template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import emergency_queries as eq
import organizations_queries as oq
import campaigns_queries as cq
import hospital_queries as hq
import users_queries as uq
import donation_queries as mdq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for hospital dashboard page
@app_hospital.route('/')
@app_hospital.route('/index')
def index():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:

        email = session['hospitalId']

        today = datetime.now().strftime("%Y-%m-%d")

        campaigns_count = len(cq.get_all_campaigns(1))
        donors_count = uq.get_donors_count(1)[0][0]
        emergency_needs_count = len(
            eq.get_hospital_emergency_need_details(email))

        up_coming_events = cq.get_up_coming_campaigns_limit_5(today)
        today_events = cq.get_today_campaigns_limit_5(today)
        emergency_needs = eq.get_emergency_needs_limit_10(email)

        return render_template('hospital/index.html', up_coming_events=up_coming_events, today_events=today_events, donors_count=donors_count,
                               campaigns_count=campaigns_count, emergency_needs_count=emergency_needs_count, emergency_needs=emergency_needs)


# Route for sign out
@app_hospital.route('/sign-out')
def organization_signout():
    if 'hospitalId' in session:
        session.pop('hospitalId', None)

    return redirect(url_for('index'))
