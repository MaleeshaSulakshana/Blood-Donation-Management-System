import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_hospital_campaign = Blueprint("app_hospital_campaign", __name__, url_prefix="/hospital/campaign",
                                  template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import campaigns_queries as cq


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_hospital_campaign.route('/')
def campaigns():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        campaigns = cq.get_all_campaigns(1)
        return render_template('hospital/campaign/campaigns.html', campaigns=campaigns)


@app_hospital_campaign.route('/view')
def view():
    if 'hospitalId' not in session:
        return redirect(url_for('index'))

    else:
        id = request.args['id']
        details = cq.get_campaigns_details(id)
        return render_template('hospital/campaign/view_campaign_details.html', details=details)
