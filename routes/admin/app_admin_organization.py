import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin_organization = Blueprint("app_admin_organization", __name__, url_prefix="/admin/organization",
                                   template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils as ut
import organizations_queries as oq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_admin_organization.route('/pending')
def organization_pending():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        details = oq.get_all_organizations(0)
        return render_template('admin/organization/pending_organization.html', details=details)


@app_admin_organization.route('/approved')
def organization_approved():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        details = oq.get_all_organizations(1)
        return render_template('admin/organization/approved_organization.html', details=details)


@app_admin_organization.route('/view')
def view():
    if 'adminId' not in session:
        return redirect(url_for('index'))

    else:
        id = request.args['id']
        details = oq.get_organization_account_details(id)
        return render_template('admin/organization/view_organization_details.html', details=details)


@app_admin_organization.route('/update_organization_approval', methods=['GET', 'POST'])
def update_user_approval():

    id = request.form.get('id')

    is_updated = oq.update_organization_approval(id)
    if is_updated > 0:
        return jsonify({'success': "Organization approved successfull!"})

    else:
        return jsonify({'error': "Organization approved not successfull. Please try again!"})
