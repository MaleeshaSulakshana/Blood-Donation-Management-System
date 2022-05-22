import db_connector as dbConn


# Function for organization registration
def organization_registration(data):
    conn = dbConn.db_connector()

    email = data['email']
    psw = data['psw']
    account_type = 2
    name = data['name']
    hod = data['hod']
    location = data['location']
    number = data['number']
    is_approved = data['is_approved']

    query = ''
    row_count = 0

    query = ''' INSERT INTO users (email, psw, account_type, is_approved) VALUES (%s, %s, %s, %s) '''
    values = (str(email), str(psw), str(account_type), int(is_approved))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    if cur.rowcount > 0:

        query = ''' INSERT INTO organizations_details (email, name, hod, location, number) VALUES (%s, %s, %s, %s, %s) '''
        values = (str(email), str(name), str(
            hod), str(location), str(number))
        cur = conn.cursor()
        cur.execute(query, values)

        conn.commit()
        row_count = cur.rowcount

    return row_count


# Function for get all organizations
def get_all_organizations(is_approved):
    conn = dbConn.db_connector()

    query = ''' SELECT users.email, name, hod, location, number FROM organizations_details 
                INNER JOIN users ON users.email = organizations_details.email
                WHERE is_approved = %s '''

    values = (int(is_approved),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get profile details
def get_organization_account_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT users.email, name, hod, location, number, users.is_approved  FROM organizations_details
                    INNER JOIN users ON users.email = organizations_details.email WHERE users.email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update organization details
def update_organizations_details(data):
    conn = dbConn.db_connector()

    name = data['name']
    hod = data['hod']
    location = data['location']
    number = data['phone']
    email = data['email']

    query = ''
    row_count = 0

    query = ''' UPDATE organizations_details SET name = %s, hod = %s, location = %s, number = %s WHERE email = %s '''
    values = (str(name), str(hod),
              str(location), str(number), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update organization psw
def update_organization_psw(email, psw):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE users SET psw = %s WHERE email = %s '''
    values = (str(psw), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update organization  approval
def update_organization_approval(email):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE users SET is_approved = 1 WHERE email = %s '''
    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count
