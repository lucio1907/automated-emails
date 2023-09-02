import os
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv

load_dotenv()

def get_connection() -> connection:
    connection = psycopg2.connect(
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_NAME')
    )
    return connection

def add_recruiter_to_DB(connection: connection):
    while True:    
        os.system('cls')
        recruiter_name = input('Recruiter name: ').capitalize()
        recruiter_email = input('Recruiter email: ').strip()
        recruiter_phone = input('Recruiter phone (optional): ').capitalize()
        recruiter_company = input('Recruiter company: ').capitalize()
        job_position = input('Job position: ').capitalize()
        user_selection = input('Would you like to add another one? [y/n]: ').lower()

        if recruiter_phone == '':
            with connection:
                with connection.cursor() as cursor:
                    query = 'INSERT INTO recruiters.recruiter (name, email, company, job_position) VALUES (%s, %s, %s, %s)'
                    values = (recruiter_name.strip(), recruiter_email.strip(), recruiter_company.strip(), job_position.strip())
                    cursor.execute(query, values)
            os.system('cls')
            print('Recruiter added successfully')
        else:
            with connection:
                with connection.cursor() as cursor:
                    query = 'INSERT INTO recruiters.recruiter (name, email, phone, company, job_position) VALUES (%s, %s, %s, %s, %s)'
                    values = (recruiter_name.strip(), recruiter_email.strip(), recruiter_phone.strip(), recruiter_company.strip(), job_position.strip())
                    cursor.execute(query, values)
            os.system('cls')
            print('Recruiter added successfully')

        if user_selection == 'n':
            break