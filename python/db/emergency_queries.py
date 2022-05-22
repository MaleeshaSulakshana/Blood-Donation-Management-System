import db_connector as dbConn


# Function for add_emergency_need
def add_emergency_need(data):
    conn = dbConn.db_connector()

    title = data['title']
    desc = data['desc']
    today = data['today']
    hospital_id = data['hospital_id']

    query = ''
    row_count = 0

    query = ''' INSERT INTO emergency_needs (title, description, date, hospital_id) VALUES (%s, %s, %s, %s) '''
    values = (str(title), str(desc), str(today), str(hospital_id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for get all emergency_needs
def get_all_emergency_needs():
    conn = dbConn.db_connector()

    query = ''' SELECT emergency_needs.id, title, description, date, hospital_id, name, number, address FROM emergency_needs 
                INNER JOIN hospitals_details ON hospitals_details.email = emergency_needs.hospital_id '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get all emergency_needs
def get_emergency_needs_limit_10(email):
    conn = dbConn.db_connector()

    query = ''' SELECT id, title, description, date, hospital_id FROM emergency_needs WHERE hospital_id = %s ORDER BY id DESC LIMIT 10'''

    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get emergency_need details
def get_hospital_emergency_need_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT id, title, description, date, hospital_id FROM emergency_needs WHERE hospital_id = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get emergency_need details by id
def get_emergency_need_details_by_id(id):
    conn = dbConn.db_connector()

    query = ''' SELECT id, title, description, date, hospital_id FROM emergency_needs WHERE id = %s '''
    values = (int(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for remove emergency_need
def remove_emergency_need(id):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' DELETE FROM emergency_needs WHERE id = %s '''
    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count
