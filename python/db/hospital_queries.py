import db_connector as dbConn


# Function for hospital registration
def hospital_registration(data):
    conn = dbConn.db_connector()

    name = data['name']
    address = data['address']
    number = data['number']
    email = data['email']
    psw = data['psw']
    account_type = 3
    is_approved = 1

    query = ''
    row_count = 0

    query = ''' INSERT INTO users (email, psw, account_type, is_approved) VALUES (%s, %s, %s, %s) '''
    values = (str(email), str(psw), str(account_type), int(is_approved))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    if cur.rowcount > 0:

        query = ''' INSERT INTO hospitals_details (email, name, address, number) VALUES (%s, %s, %s, %s) '''
        values = (str(email), str(name), str(address), str(number))
        cur = conn.cursor()
        cur.execute(query, values)

        conn.commit()
        row_count = cur.rowcount

    return row_count


# Function for get all hospitals
def get_all_hospitals():
    conn = dbConn.db_connector()

    query = ''' SELECT users.email, name, address, number FROM users INNER JOIN hospitals_details 
                ON users.email = hospitals_details.email WHERE users.account_type = 3 '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get profile details
def get_hospital_account_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT users.email, name, address, number FROM users INNER JOIN hospitals_details 
                ON users.email = hospitals_details.email WHERE users.email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update hospital details
def update_hospital_details(data):
    conn = dbConn.db_connector()

    email = data['email']
    name = data['name']

    query = ''
    row_count = 0

    query = ''' UPDATE hospitals_details SET name = %s WHERE email = %s '''
    values = (str(name), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update hospital psw
def update_hospital_psw(email, psw):
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


# Function for remove hospital
def remove_hospital(email):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' DELETE FROM users WHERE email = %s '''
    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()

    query = ''' DELETE FROM hospitals_details WHERE email = %s '''
    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()

    row_count = cur.rowcount

    return row_count
