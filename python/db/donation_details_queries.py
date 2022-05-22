import db_connector as dbConn


# Function for donation_details registration
def add_donation_details(data):
    conn = dbConn.db_connector()

    email = data['email']
    campaign_id = data['campaign_id']
    units = data['units']

    query = ''
    row_count = 0

    query = ''' INSERT INTO donation_details (campaign_id, donor_email, units) VALUES (%s, %s, %s) '''
    values = (int(campaign_id), str(email), int(units))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Get all donation_details by campaign
def all_donation_details_by_donor(email):
    conn = dbConn.db_connector()

    query = ''' SELECT campaigns.campaign_id, donor_email, units, name, date FROM donation_details
                INNER JOIN campaigns ON campaigns.campaign_id = donation_details.campaign_id 
                WHERE donor_email = %s '''

    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def donor_details_by_campaign(campaign_id):
    conn = dbConn.db_connector()

    query = ''' SELECT campaigns.campaign_id, donor_email, units, campaigns.name, date, users_details.full_name, gender, nic, phone_number FROM donation_details
                INNER JOIN campaigns ON campaigns.campaign_id = donation_details.campaign_id 
                INNER JOIN users_details ON users_details.email = donation_details.donor_email 
                WHERE campaigns.campaign_id = %s '''

    values = (int(campaign_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()
