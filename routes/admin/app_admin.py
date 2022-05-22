import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin = Blueprint("app_admin", __name__, url_prefix="/admin",
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


# Route for admin page
@app_admin.route('/')
@app_admin.route('/index')
def index():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    month = datetime.now().strftime("%Y-%m")
    today = datetime.now().strftime("%Y-%m-%d")

    approved_organizations_count = len(oq.get_all_organizations(1))
    pending_organizations_count = len(oq.get_all_organizations(0))
    approved_campaigns_count = len(cq.get_all_campaigns(1))
    pending_campaigns_count = len(cq.get_all_campaigns(0))
    donors_count = uq.get_donors_count(1)[0][0]
    hospitals_count = len(hq.get_all_hospitals())
    hospitals_count = len(hq.get_all_hospitals())

    sum_of_donations = mdq.get_donations_amount()[0][0]

    up_coming_events = cq.get_up_coming_campaigns_limit_5(today)
    today_events = cq.get_today_campaigns_limit_5(today)
    pending_users = uq.get_all_users_donors(0, "yes")

    return render_template('admin/index.html', approved_organizations_count=approved_organizations_count,
                           pending_organizations_count=pending_organizations_count, approved_campaigns_count=approved_campaigns_count,
                           pending_campaigns_count=pending_campaigns_count, donors_count=donors_count, hospitals_count=hospitals_count,
                           sum_of_donations=sum_of_donations, up_coming_events=up_coming_events, today_events=today_events, pending_users=pending_users)


# Route for sign out
@app_admin.route('/admin-sign-out')
def organization_signout():
    if 'adminId' in session:
        session.pop('adminId', None)

    return redirect(url_for('index'))
