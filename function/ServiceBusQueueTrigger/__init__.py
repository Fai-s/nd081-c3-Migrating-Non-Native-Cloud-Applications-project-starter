import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(dbname="techconfdb", user="azureuser@tech-postgre-server", password="@Password", host="tech-postgre-server.postgres.database.azure.com")
    cursor = conn.cursor()
    try:
        # TODO: Get notification message and subject from database using the notification_id
        notification = cursor.execute("SELECT message, subject FROM notification WHERE id={};".format(notification_id))
        
        # TODO: Get attendees email and name
        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cursor.fetchall()
        

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            Mail('{}, {}, {}'.format({'info@techconf.com'}, {attendee[2]}, {notification}))
        nDate = datetime.utcnow()
        notified = 'Notified {} attendees'.format(len(attendees))

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notified, nDate, notification_id))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection

        cursor.close()
        conn.close()