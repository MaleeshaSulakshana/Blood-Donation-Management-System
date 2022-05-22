import db_connector as dbConn


# Function for campaigns registration
def campaigns_registration(data):
    conn = dbConn.db_connector()

    campaign_id = data['campaign_id']
    organization_id = data['organization_id']
    name = data['name']
    venue = data['venue']
    date = data['date']
    stime = data['stime']
    etime = data['etime']
    lat = data['lat']
    lon = data['lon']
    description = data['description']
    thumbnail = data['thumbnail']
    is_approved = data['is_approved']

    query = ''
    row_count = 0

    query = ''' INSERT INTO campaigns (campaign_id, organization_id, name, venue, date, start_time, 
                                    end_time, lat, lon, description, thumbnail, is_approved) VALUES 
                                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
    values = (int(campaign_id), str(organization_id), str(name), str(venue), str(date), str(stime),
              str(etime), str(lat), str(lon), str(description), str(thumbnail), int(is_approved))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all campaigns
def get_all_campaigns(approval, organization_id=""):
    conn = dbConn.db_connector()

    if organization_id == "":
        query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                        end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = %s 
                                        ORDER BY id DESC'''

        values = (int(approval),)

    else:
        query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                    end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = %s 
                                    AND organization_id = %s
                                    ORDER BY id DESC'''

        values = (int(approval), str(organization_id))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_completed_campaigns(date):
    conn = dbConn.db_connector()

    query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1
                                AND date > %s
                                ORDER BY id DESC'''

    values = (str(date),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_up_coming_campaigns(date):
    conn = dbConn.db_connector()

    query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1
                                AND date > %s
                                ORDER BY id DESC'''

    values = (str(date),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_up_coming_campaigns_by_organization(date, organization_id):
    conn = dbConn.db_connector()

    query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1
                                AND date > %s AND organization_id = %s
                                ORDER BY id DESC'''

    values = (str(date), str(organization_id))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_completed_campaigns_by_organization(date, organization_id):
    conn = dbConn.db_connector()

    query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1
                                AND date < %s AND organization_id = %s
                                ORDER BY id DESC'''

    values = (str(date), str(organization_id))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_up_coming_campaigns_limit_5(date, organization_id=""):
    conn = dbConn.db_connector()

    if organization_id == "":
        query = ''' SELECT campaign_id, name, venue, date FROM campaigns WHERE is_approved = 1 AND date > %s 
                                    ORDER BY date ASC LIMIT 5'''

        values = (str(date),)

    else:
        query = ''' SELECT campaign_id, name, venue, date FROM campaigns WHERE is_approved = 1 AND date > %s 
                                    AND organization_id = %s
                                    ORDER BY date ASC LIMIT 5 '''

        values = (str(date), str(organization_id))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# def get_up_coming_campaigns(date):
#     conn = dbConn.db_connector()
#     query = ''' SELECT campaign_id, name, venue, date, start_time,
#                                         end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1 AND date > %s
#                                 ORDER BY date ASC LIMIT 5'''

#     values = (str(date),)

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


def get_completed_campaigns(date, organization_id=""):
    conn = dbConn.db_connector()

    if organization_id == "":
        query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                        end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1 AND date < %s 
                                    ORDER BY date DESC'''

        values = (str(date),)

    else:
        query = ''' SELECT campaign_id, name, venue, date, start_time, 
                                        end_time, lat, lon, description, thumbnail FROM campaigns WHERE is_approved = 1 AND date < %s 
                                    AND organization_id = %s
                                    ORDER BY date DESC '''

        values = (str(date), str(organization_id))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_today_campaigns_limit_5(date, organization_id=""):
    conn = dbConn.db_connector()

    if organization_id == "":
        query = ''' SELECT campaign_id, name, venue, date FROM campaigns WHERE is_approved = 1 AND date = %s 
                                    ORDER BY date ASC LIMIT 5'''

        values = (str(date),)

    else:
        query = ''' SELECT campaign_id, name, venue, date FROM campaigns WHERE is_approved = 1 AND date = %s 
                                    AND organization_id = %s
                                    ORDER BY date ASC LIMIT 5 '''

        values = (str(date), str(organization_id))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_campaigns_count(approval, email):
    conn = dbConn.db_connector()

    query = ''' SELECT COUNT(campaign_id) FROM campaigns WHERE is_approved = %s AND organization_id = %s '''

    values = (int(approval), str(email))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get details
def get_campaigns_details(campaign_id):
    conn = dbConn.db_connector()

    query = ''' SELECT campaign_id, campaigns.name, venue, date, start_time, 
                                    end_time, lat, lon, description, thumbnail, is_approved, organizations_details.name FROM campaigns 
                                    INNER JOIN organizations_details ON campaigns.organization_id = organizations_details.email WHERE campaign_id = %s '''
    values = (int(campaign_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update campaigns  approval
def update_campaigns_approval(campaign_id):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE campaigns SET is_approved = 1 WHERE campaign_id = %s '''
    values = (int(campaign_id),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update campaigns rejection
def update_campaigns_rejection(campaign_id):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE campaigns SET is_approved = 2 WHERE campaign_id = %s '''
    values = (int(campaign_id),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for remove campaign
def remove_campaign(campaign_id):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' DELETE FROM campaigns WHERE campaign_id = %s '''
    values = (int(campaign_id),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count