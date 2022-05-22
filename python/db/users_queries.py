import db_connector as dbConn


# Function for check exist email
def is_exist_email(email):
    conn = dbConn.db_connector()

    query = ''' SELECT count(email) FROM users WHERE email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for login
def login(email, psw):
    conn = dbConn.db_connector()

    query = ''' SELECT id, email, account_type FROM users WHERE email = %s AND psw = %s AND is_approved = 1 '''
    values = (str(email), str(psw))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for registration
def registration(data):
    conn = dbConn.db_connector()

    email = data['email']
    psw = data['psw']
    account_type = 4
    full_name = data['full_name']
    dob = data['dob']
    gender = data['gender']
    blood_type = data['blood_type']
    phone_number = data['phone_number']
    nic = data['nic']
    is_approved = data['is_approved']

    query = ''
    row_count = 0

    query = ''' INSERT INTO users (email, psw, account_type, is_approved) VALUES (%s, %s, %s, %s) '''
    values = (str(email), str(psw), str(account_type), int(is_approved))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    if cur.rowcount > 0:

        query = ''' INSERT INTO users_details (email, full_name, dob, gender, blood_type, phone_number, nic) VALUES (%s, %s, %s, %s, %s, %s, %s) '''
        values = (str(email), str(full_name), str(dob), str(gender),
                  str(blood_type), str(phone_number), str(nic))
        cur = conn.cursor()
        cur.execute(query, values)

        conn.commit()
        row_count = cur.rowcount

    return row_count


# Function for get all users
def get_all_users_donors(is_approved, is_limit=""):
    conn = dbConn.db_connector()

    query = ''' SELECT users.id, users.email, full_name, dob, gender, blood_type, phone_number, nic FROM users 
                    INNER JOIN users_details ON users.email = users_details.email WHERE users.is_approved = %s '''

    if is_limit != "":
        query += '''LIMIT 10'''

    values = (str(is_approved),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_donors_count(is_approved):
    conn = dbConn.db_connector()

    query = ''' SELECT COUNT(users.id) FROM users 
                    INNER JOIN users_details ON users.email = users_details.email WHERE users.is_approved = %s '''

    values = (str(is_approved),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get donor details
def get_donor_details(email):
    conn = dbConn.db_connector()

    query = """ SELECT users.id, users.email, full_name, dob, gender, blood_type, phone_number, nic, users.is_approved FROM users 
                    INNER JOIN users_details ON users.email = users_details.email WHERE users.email = %s """
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get profile details
def get_account_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT email, full_name, dob, gender, blood_type, phone_number, nic FROM users_details WHERE email = '%s' '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update user details
def update_user_details(data):
    conn = dbConn.db_connector()

    email = data['email']
    name = data['name']
    dob = data['dob']
    number = data['number']

    query = ''
    row_count = 0

    query = ''' UPDATE users_details SET full_name = %s, dob = %s, phone_number = %s WHERE email = %s '''
    values = (str(name), str(dob), str(number), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update user psw
def update_user_psw(email, psw):
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


# Function for update user  approval
def update_user_approval(id):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE users SET is_approved = 1 WHERE id = %s '''
    values = (str(id),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count
