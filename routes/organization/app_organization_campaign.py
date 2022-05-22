import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

app_organization_campaign = Blueprint("app_organization_campaign", __name__, url_prefix="/organization/campaign",
                                      template_folder='templates', static_folder='../../static')

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import campaigns_queries as cq
import appointments_queries as aq
import donation_details_queries as ddq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


@app_organization_campaign.route('/add')
def add_campaign():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        return render_template('organization/campaign/add_campaigns.html')


@app_organization_campaign.route('/pending')
def pending_campaign():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        campaigns = cq.get_all_campaigns(0, session['organizationId'])
        return render_template('organization/campaign/pending_campaigns.html', campaigns=campaigns)


@app_organization_campaign.route('/approved')
def approved_campaign():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        today = datetime.now().strftime("%Y-%m-%d")
        campaigns = cq.get_up_coming_campaigns_by_organization(
            today, session['organizationId'])
        return render_template('organization/campaign/approved_campaigns.html', campaigns=campaigns)


@app_organization_campaign.route('/view')
def view():
    if 'organizationId' not in session:
        return redirect(url_for('index'))

    else:
        id = request.args['id']
        details = cq.get_campaigns_details(id)
        appointments = aq.all_appointments_by_campaign_id(id)
        donations = ddq.donor_details_by_campaign(id)
        today = str(datetime.now().strftime("%Y-%m-%d"))
        campaign_date = str(details[0][3])

        a = datetime.strptime(today, "%Y-%m-%d")
        b = datetime.strptime(campaign_date, "%Y-%m-%d")
        delta = b - a
        day_count = delta.days

        return render_template('organization/campaign/view_campaign_details.html', details=details, appointments=appointments, donations=donations, day_count=day_count)


# Route for add campaign
@app_organization_campaign.route('/add_campaign_details', methods=['GET', 'POST'])
def add_campaign_details():

    if request.method == "POST":

        if 'organizationId' not in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            venue = request.form.get('venue')
            date = request.form.get('date')
            stime = request.form.get('stime')
            etime = request.form.get('etime')
            lat = request.form.get('lat')
            long = request.form.get('long')
            desc = request.form.get('desc')
            thumbnail = request.files.get('thumbnail')

            past = datetime.strptime(date, "%Y-%m-%d")
            present = datetime.now()
            is_valid_date = past.date() < present.date()

            cast_stime = float(str(stime.replace(":", ".")))
            cast_etime = float(str(etime.replace(":", ".")))
            time_period = cast_etime - cast_stime

            is_valid_time = float(time_period) > float(0)

            if (len(name) == 0 or len(venue) == 0 or len(date) == 0 or len(stime) == 0 or
                    len(etime) == 0 or len(lat) == 0 or len(long) == 0 or len(desc) == 0 or thumbnail == None):

                return jsonify({'error': "Fields are empty!"})

            if is_valid_date != False:
                return jsonify({'error': "Please enter valid date!"})

            if is_valid_time != True:
                return jsonify({'error': "Please enter valid time slots!"})

            else:

                campaign_id = ut.random_number_with_date()
                email = session['organizationId']

                # Save uploaded images and get file names
                save_folder = os.path.join(
                    root, '../static/campaign_images/')
                thumbnail_name, extention = ut.file_save(
                    thumbnail, save_folder, campaign_id)

                data = {
                    'name': name,
                    'venue': venue,
                    'date': date,
                    'stime': stime,
                    'etime': etime,
                    'lat': lat,
                    'lon': long,
                    'description': desc,
                    'campaign_id': campaign_id,
                    'organization_id': email,
                    'thumbnail': thumbnail_name,
                    'is_approved': 0
                }

                is_created = cq.campaigns_registration(data)
                if is_created > 0:
                    return jsonify({'success': "Campaign registered successfull!"})

                else:
                    return jsonify({'error': "Campaign registered not successfull. Please try again!"})

    return jsonify({'redirect': url_for('index')})


@app_organization_campaign.route('/remove_campaign', methods=['GET', 'POST'])
def remove_campaign():

    id = request.form.get('id')

    is_removed = cq.remove_campaign(id)
    if is_removed > 0:
        return jsonify({'success': "Campaign removed successfull!"})

    else:
        return jsonify({'error': "Campaign removed not successfull. Please try again!"})
