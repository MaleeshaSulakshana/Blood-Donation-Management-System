import db_connector as dbConn


# Function for appointments registration
def appointments_registration(data):
    conn = dbConn.db_connector()

    campaign_id = data['campaign_id']
    donor = data['donor']

    query = ''
    row_count = 0

    query = ''' INSERT INTO appointments (campaign_id, donor) VALUES (%s, %s) '''
    values = (int(campaign_id), str(donor))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for check appointment is exist
def is_appointment_exist(campaign_id, donor):
    conn = dbConn.db_connector()

    query = ''' SELECT COUNT(id) FROM appointments WHERE campaign_id = %s AND donor = %s '''

    values = (int(campaign_id), str(donor))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Get all appointments by campaign
def all_appointments_by_campaign(campaign_id, donor):
    conn = dbConn.db_connector()

    query = ''' SELECT id, campaign_id, donor, full_name, phone_number FROM appointments
                INNER JOIN users_details ON users_details.email = appointments.donor WHERE campaign_id = %s AND donor = %s '''

    values = (int(campaign_id), str(donor))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def all_appointments_by_campaign_id(campaign_id):
    conn = dbConn.db_connector()

    query = ''' SELECT appointments.id, campaign_id, donor, full_name, phone_number FROM appointments
                INNER JOIN users_details ON users_details.email = appointments.donor WHERE campaign_id = %s '''

    values = (int(campaign_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Get all appointments by campaign
def all_upcoming_appointments(donor, date):
    conn = dbConn.db_connector()

    query = ''' SELECT appointments.id, appointments.campaign_id, donor, full_name, phone_number, campaigns.name, venue, campaigns.date, campaigns.thumbnail FROM appointments
                INNER JOIN users_details ON users_details.email = appointments.donor
                INNER JOIN campaigns ON appointments.campaign_id = campaigns.campaign_id WHERE donor = %s AND campaigns.date = %s OR campaigns.date > %s '''

    values = (str(donor), str(date), str(date))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get all appointments
def get_all_appointments():
    conn = dbConn.db_connector()

    query = ''' SELECT id, campaign_id, donor, full_name, phone_number FROM appointments
                INNER JOIN users_details ON users_details.email = appointments.donor ORDER BY id DESC'''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_appointments_count(campaign_id):
    conn = dbConn.db_connector()

    query = ''' SELECT COUNT(id) FROM appointments WHERE campaign_id = %s '''

    values = (int(campaign_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for remove appointments
def remove_appointment(campaign_id, donor):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' DELETE FROM appointments WHERE campaign_id = %s AND donor = %s '''

    values = (int(campaign_id), str(donor))

    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count
