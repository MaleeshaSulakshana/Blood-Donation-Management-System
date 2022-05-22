import os
import sys
from datetime import datetime, date
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_organization = Blueprint("app_organization", __name__, url_prefix="/organization",
                             template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('../../python/db'))

import utils
import organizations_queries as oq
import users_queries as uq
import campaigns_queries as cq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for organization dashboard page
@app_organization.route('/')
@app_organization.route('/index')
def organization_index():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        email = session['organizationId']
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")

        approved_donor_count = uq.get_donors_count(1)[0][0]
        pending_donor_count = uq.get_donors_count(0)[0][0]
        pending_campaign_count = cq.get_campaigns_count(0, email)[0][0]
        today = datetime.now().strftime("%Y-%m-%d")
        completed_campaign_count = len(
            cq.get_completed_campaigns_by_organization(today, email))

        up_coming_events = cq.get_up_coming_campaigns_by_organization(
            today, email)
        today_events = cq.get_today_campaigns_limit_5(date_str, email)
        pending_users = uq.get_all_users_donors(0, "yes")

        return render_template('organization/index.html', approved_donor=approved_donor_count, pending_donor=pending_donor_count,
                               pending_campaign=pending_campaign_count, completed_campaign=completed_campaign_count,
                               up_coming_events=up_coming_events, today_events=today_events, pending_users=pending_users)


# Route for sign out
@app_organization.route('/organization-sign-out')
def organization_signout():
    if 'organizationId' in session:
        session.pop('organizationId', None)

    return redirect(url_for('index'))
