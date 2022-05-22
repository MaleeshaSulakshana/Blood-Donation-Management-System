import os
import sys
from datetime import date, datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_admin_money_donations = Blueprint("app_admin_money_donations", __name__, url_prefix="/admin/money_donations",
                                      template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils as ut
import donation_queries as dq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_admin_money_donations.route('/')
def view_money_donations():

    selecteddate = request.args.get('month')

    if 'adminId' not in session:
        return redirect(url_for('index'))

    if selecteddate == None:
        today = date.today()
        month = today.strftime("%Y-%m")

    else:
        selected_date = datetime.strptime(selecteddate, '%Y-%m-%d')
        month = selected_date.strftime("%Y-%m")

    details = dq.get_donations(month)
    return render_template('admin/money_donations/view_money_donations.html', details=details, month=month)
