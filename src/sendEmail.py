import smtplib
import os
import ssl
from colorama import Fore
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from getRecruiters import add_recruiter_to_DB, get_connection 
from getRecruitersOnlyCv import add_recruiter_only_cv

load_dotenv()

connection = get_connection()

email_sender = os.environ.get('EMAIL_SENDER')
email_password = os.environ.get('EMAIL_PASSWORD')
cv_path = "E:\PythonProjects\mailAutomate\CV-LucioGastellu.pdf"

def get_all_recruiters(table: str): 
    with connection:
        with connection.cursor() as cursor:
            query = f'SELECT * FROM {table} ORDER BY id'
            cursor.execute(query, )
            recruiters = cursor.fetchall()
            return recruiters

def get_info_about_companies_recruiters():
    recruiters = get_all_recruiters('recruiters.recruiter')

    with connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM recruiters.recruiter WHERE check_email_status = 'Waiting'"
            cursor.execute(query)
            receptors = cursor.fetchall()

    for recruiter in recruiters:
        # Si el estado del mail esta en "Waiting" que lo actualice a "Sent" en la BD
        if recruiter[6] == 'Waiting':
            with connection:
                with connection.cursor() as cursor:
                    query = f"UPDATE recruiters.recruiter SET check_email_status = 'Sent' WHERE id = {recruiter[0]}"
                    cursor.execute(query)    
            continue
    
    return receptors

def get_info_about_onlyCV_recruiters():
    recruiters = get_all_recruiters('recruiters.only_cv_to_recruiter')
    
    with connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM recruiters.only_cv_to_recruiter WHERE check_email_status = 'Waiting'"
            cursor.execute(query)
            receptors = cursor.fetchall()
            
    for recruiter in recruiters:
        if recruiter[4] == 'Waiting':
            with connection:
                with connection.cursor() as cursor:
                    query = f"UPDATE recruiters.only_cv_to_recruiter SET check_email_status = 'Sent' WHERE id = {recruiter[0]}"
                    cursor.execute(query)
            continue
    
    return receptors

def send_emails_to_companies_recruiters(receptors: list):
    for i in range(0, len(receptors)):
        subject = f'Posición: {receptors[i][5]}'
        body = f"""
            Hola {receptors[i][1]}! Un gusto poder dirigirme hacia usted/es,

            Me presento, mi nombre es Lucio Gastellu y soy desarrollador de software con conocimientos en:

            Frontend: HTML, CSS, JavaScript, React Js, Next Js, Tailwind CSS
            Backend: Node.js, Express.js, TypeScript, Python, Java, MongoDB, PostgreSQL

            Mi pasión es crear soluciones web innovadoras y funcionales. Me enfoco en mejorar la experiencia del usuario y desarrollar aplicaciones rápidas y escalables.

            Me gustaría invitarle a que eche un vistazo a mis perfiles:
            Linkedin: https://www.linkedin.com/in/luciogastellu/
            Github: https://github.com/lucio1907
            Portafolio: https://personal-portfolio-lucio1907.vercel.app/

            Me encantaría poder unirme a su equipo y contribuir al éxito de sus proyectos.

            Muchas gracias por tomarse el tiempo de leerme! 
            
            Atentamente,
            Lucio Gastellu - Software Developer
        """
        
        # Crear el objeto EmailMessage
        em = MIMEMultipart()
        em['From'] = email_sender
        em['To'] = receptors[i][2]
        em['Subject'] = subject
        em.attach(MIMEText(body, 'plain'))

        with open(cv_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((file).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=CV-LucioGastellu.pdf")
        em.attach(part)  # Adjuntar el archivo al objeto em

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, receptors[i][2], em.as_string())

    os.system('cls')
    return print('Emails sent successfully')

def check_companies_emails(receptors: list):
    if len(receptors) > 0:
        print('Sending...')
        send_emails_to_companies_recruiters(receptors)
    else:
        print("No emails to send, please add a recruiter if you wanna send such email")

def send_emails_to_onlyCV_recruiters(receptors: list): 
    for i in range(0, len(receptors)):
        subject = 'CV actualizado Lucio Gastellu'
        body = f"""
            Hola {receptors[i][1]}! Un gusto poder dirigirme hacia usted,

            Mi nombre es Lucio Gastellu, un apasionado desarrollador de software con un enfoque en la creación de soluciones web innovadoras y funcionales.
            Mi experiencia abarca tanto el Frontend como el Backend, lo que me permite diseñar aplicaciones rápidas y escalables que mejoran la experiencia del usuario.

            En Frontend, tengo conocimientos sólidos en HTML, CSS y JavaScript, y utilizo bibliotecas como React Js con Next Js y Tailwind CSS para crear interfaces de usuario modernas e interactivas.

            En Backend, tengo conocimientos sólidos en Node.js, Express.js y TypeScript, lo que me permite desarrollar API robustas y servidores web eficientes.
            Además, utilizo bases de datos NoSQL como MongoDB y SQL como PostgreSQL para diseñar sistemas de almacenamiento de datos eficientes.
            También suelo utilizar Python para crear scripts de automatización o software.

            Mi objetivo es siempre alcanzar la excelencia en cada proyecto en el que participo.

            Si deseas conocer más sobre mis proyectos anteriores, puedes visitar mis perfiles en línea:

            Linkedin: https://www.linkedin.com/in/luciogastellu/
            Github: https://github.com/lucio1907
            Portafolio: https://personal-portfolio-lucio1907.vercel.app/

            Gracias por tomarte el tiempo de conocerme. Si tenes alguna pregunta o estás interesado/a en conocer más sobre mi, no dudes en contactarme. Estoy emocionado de contribuir con mis habilidades y experiencia para crear soluciones exitosas.

            Atentamente,
            Lucio Gastellu - Software Developer
        """

        em = MIMEMultipart()
        em['From'] = email_sender
        em['To'] = receptors[i][3]
        em['Subject'] = subject
        em.attach(MIMEText(body, 'plain'))

        with open(cv_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((file).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=CV-LucioGastellu.pdf")
        em.attach(part)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, receptors[i][3], em.as_string())
    
    os.system('cls')
    return print('Emails sent successfully')

def check_onlyCV_emails(receptors: list):
    if len(receptors) > 0:
        print('Sending...')
        send_emails_to_onlyCV_recruiters(receptors)
    else:
        print("No emails to send, please add a recruiter if you wanna send such email") 

def print_colored_box(text):
    lines = text.split('\n')
    box_width = max(len(line) for line in lines) + 4

    # Imprimir la parte superior del cuadro
    print(Fore.YELLOW + " " + "=" * (box_width - 2))
    
    # Imprimir el contenido del cuadro con los bordes laterales
    for line in lines:
        print(Fore.YELLOW + f"|{Fore.RESET} {line.ljust(box_width - 4)} {Fore.YELLOW}|")

    # Imprimir la parte inferior del cuadro
    print(Fore.YELLOW + " " + "=" * (box_width - 2))

def main(): 
    connection = get_connection()    
    while True:
        os.system('cls')
        text_inside_box = f"""
{Fore.GREEN}=========== ADD RECRUITERS ==========={Fore.RESET}

1) Add companies recruiters to DB
2) Add only CV recruiters to DB
              
{Fore.LIGHTCYAN_EX}============= SEND EMAILS ============{Fore.RESET}

3) Send emails to companies recruiters
4) Send emails to only CV recruiters
5) Send both (companies & only recruiters)

{Fore.RED}=========== FINISH PROGRAM ==========={Fore.RESET}

6) End program
"""     
        print_colored_box(text_inside_box)
        
        user_input = input('Select an option: ')
        if user_input.isdigit():
            user_selection = int(user_input)
            try:
                if user_selection == 1: 
                    add_recruiter_to_DB(connection)
                elif user_selection == 2:
                    add_recruiter_only_cv(connection)
                elif user_selection == 3:
                    receptors = get_info_about_companies_recruiters()
                    check_companies_emails(receptors)
                elif user_selection == 4:
                    receptors = get_info_about_onlyCV_recruiters()
                    check_onlyCV_emails(receptors)
                elif user_selection == 5:
                    companies_receptors = get_info_about_companies_recruiters()
                    recruiters_receptors = get_info_about_onlyCV_recruiters()
                    check_companies_emails(companies_receptors)
                    check_onlyCV_emails(recruiters_receptors)
                elif user_selection == 6:
                    os.system('cls')
                    print('Thanks for use this program!')
                    break
            except ValueError as e:
                print(f'An error has occurred: {e}')
        else:
            print('Invalid input. Please enter a number.')

        input("Press Enter to continue...")

if __name__ == '__main__':
    main()