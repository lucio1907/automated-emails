import os
from getRecruiters import connection

def add_recruiter_only_cv(connection_db: connection):
    while True:
        os.system('cls')
        recruiter_name = input('Recruiter name: ').capitalize()
        recruiter_lastname = input('Recruiter lastname: ').capitalize()
        recruiter_email = input('Recruiter email: ')
        user_selection = input('Would you like to add another one? [y/n]: ').lower()

        with connection_db:
            with connection_db.cursor() as cursor:
                query = 'INSERT INTO recruiters.only_cv_to_recruiter (name, lastname, email) VALUES (%s, %s, %s)'
                values = (recruiter_name.strip(), recruiter_lastname.strip(), recruiter_email.strip())
                cursor.execute(query, values)
                os.system('cls')
                print('Recruiter added successfully')

        if 'n' in user_selection:
            break