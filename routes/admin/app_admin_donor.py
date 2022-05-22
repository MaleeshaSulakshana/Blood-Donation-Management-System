import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin_donor = Blueprint("app_admin_donor", __name__, url_prefix="/admin/donor",
                            template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils as ut
import users_queries as uq
import donation_details_queries as ddq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_admin_donor.route('/')
def view_donors():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    donors = uq.get_all_users_donors(1)
    return render_template('admin/donor/view_donors.html', donors=donors)


@app_admin_donor.route('/view-donor-details')
def view_donor_details():

    id = request.args['id']

    if 'adminId' not in session:
        return redirect(url_for('index'))

    details = uq.get_donor_details(id)
    donations = ddq.all_donation_details_by_donor(id)
    return render_template('admin/donor/view_donor_details.html', details=details, donations=donations)
