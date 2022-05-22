import db_connector as dbConn


# Function for admin registration
def admin_registration(data):
    conn = dbConn.db_connector()

    email = data['email']
    psw = data['psw']
    account_type = 1
    name = data['name']
    is_approved = 1

    query = ''
    row_count = 0

    query = ''' INSERT INTO users (email, psw, account_type, is_approved) VALUES (%s, %s, %s, %s) '''
    values = (str(email), str(psw), str(account_type), int(is_approved))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    if cur.rowcount > 0:

        query = ''' INSERT INTO admins_details (email, name) VALUES (%s, %s) '''
        values = (str(email), str(name))
        cur = conn.cursor()
        cur.execute(query, values)

        conn.commit()
        row_count = cur.rowcount

    return row_count


# Function for get all admins
def get_all_admins(email):
    conn = dbConn.db_connector()

    query = ''' SELECT email, name FROM admins_details WHERE email != %s '''

    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get profile details
def get_admin_account_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT email, name FROM admins_details WHERE email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update admin details
def update_admin_details(data):
    conn = dbConn.db_connector()

    email = data['email']
    name = data['name']

    query = ''
    row_count = 0

    query = ''' UPDATE admins_details SET name = %s WHERE email = %s '''
    values = (str(name), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update admin psw
def update_admin_psw(email, psw):
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


# Function for remove admin
def remove_admin(email):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' DELETE FROM users WHERE email = %s '''
    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()

    query = ''' DELETE FROM admins_details WHERE email = %s '''
    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()

    row_count = cur.rowcount

    return row_count
