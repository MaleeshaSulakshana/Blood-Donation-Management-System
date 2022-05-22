import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin_campaign = Blueprint("app_admin_campaign", __name__, url_prefix="/admin/campaign",
                               template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils as ut
import campaigns_queries as cq
import appointments_queries as aq
import donation_details_queries as ddq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_admin_campaign.route('/pending')
def campaign_pending():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        campaigns = cq.get_all_campaigns(0)
        return render_template('admin/campaign/pending_campaigns.html', campaigns=campaigns)


@app_admin_campaign.route('/approved')
def campaign_approved():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        today = datetime.now().strftime("%Y-%m-%d")
        campaigns = cq.get_up_coming_campaigns(today)
        return render_template('admin/campaign/approved_campaigns.html', campaigns=campaigns)


@app_admin_campaign.route('/completed')
def campaign_completed():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        today = datetime.now().strftime("%Y-%m-%d")
        campaigns = cq.get_completed_campaigns(today)
        return render_template('admin/campaign/completed_campaigns.html', campaigns=campaigns)


@app_admin_campaign.route('/view')
def view():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        id = request.args['id']
        details = cq.get_campaigns_details(id)
        appointments = aq.all_appointments_by_campaign_id(id)
        donations = ddq.donor_details_by_campaign(id)
        return render_template('admin/campaign/view_campaign_details.html', details=details, appointments=appointments, donations=donations)


@app_admin_campaign.route('/update_campaign_approval', methods=['GET', 'POST'])
def update_user_approval():

    id = request.form.get('id')

    is_updated = cq.update_campaigns_approval(id)
    if is_updated > 0:
        return jsonify({'success': "Campaign approved successfull!"})

    else:
        return jsonify({'error': "Campaign approved not successfull. Please try again!"})
