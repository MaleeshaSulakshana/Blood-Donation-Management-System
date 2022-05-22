import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_organization_donor = Blueprint("app_organization_donor", __name__, url_prefix="/organization/donor",
                                   template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import users_queries as uq
import donation_details_queries as ddq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_organization_donor.route('/pending')
def pending_donor():

    if 'organizationId' not in session:
        return redirect(url_for('index'))

    donors = uq.get_all_users_donors(0)
    return render_template('organization/donor/pending_donors.html', donors=donors)


@app_organization_donor.route('/approved')
def approved_donor():

    if 'organizationId' not in session:
        return redirect(url_for('index'))

    donors = uq.get_all_users_donors(1)
    return render_template('organization/donor/approved_donors.html', donors=donors)


@app_organization_donor.route('/view-donor-details')
def view_donor_details():

    id = request.args['id']
    campaign_id = request.args.get('campaign', None)

    if 'organizationId' not in session:
        return redirect(url_for('index'))

    details = uq.get_donor_details(id)
    donations = ddq.all_donation_details_by_donor(id)
    return render_template('organization/donor/view_donor_details.html', details=details, donations=donations, campaign_id=campaign_id)


@app_organization_donor.route('/update_user_approval', methods=['GET', 'POST'])
def update_user_approval():

    id = request.form.get('id')

    is_updated = uq.update_user_approval(id)
    if is_updated > 0:
        return jsonify({'success': "User approved successfull!"})

    else:
        return jsonify({'error': "User approved not successfull. Please try again!"})


@app_organization_donor.route('/add_donation_details', methods=['GET', 'POST'])
def add_donation_details():

    campaign_id = request.form.get('campaign_id')
    units = request.form.get('units')
    donor_email = request.form.get('donor_email')

    data = {
        'email': donor_email,
        'campaign_id': campaign_id,
        'units': units
    }

    is_added = ddq.add_donation_details(data)
    if is_added > 0:
        return jsonify({'success': "Blood donation details added!"})

    else:
        return jsonify({'error': "Blood donation details not added. Please try again!"})
