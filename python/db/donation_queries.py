import db_connector as dbConn


# Function for insert donations
def insert_donation(data):
    conn = dbConn.db_connector()

    email = data['email']
    name = data['name']
    amount = data['amount']
    date = data['date']
    payment_id = data['payment_id']

    query = ''
    row_count = 0

    query = ''' INSERT INTO donations (email, name, amount, date, payment_id) VALUES (%s, %s, %s, %s, %s) '''
    values = (str(email), str(name), str(amount), str(date), str(payment_id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all donations
def get_donations(month=""):
    conn = dbConn.db_connector()

    query = ''

    if month != "":
        query = """ SELECT id, email, name, amount, date FROM donations WHERE date LIKE  '%""" + \
            month + """%' ORDER BY id DESC """
    else:
        query = ''' SELECT id, email, name, amount, date FROM donations ORDER BY id DESC '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_donations_amount(month=""):
    conn = dbConn.db_connector()

    query = ''

    if month != "":
        query = """ SELECT SUM(amount) FROM donations WHERE date LIKE  '%""" + \
            month + """%' ORDER BY id DESC """
    else:
        query = ''' SELECT SUM(amount) FROM donations ORDER BY id DESC '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()
