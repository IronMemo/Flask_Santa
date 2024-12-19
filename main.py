import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

def send_bulk_emails(smtp_server, port, sender_email, sender_password, subject, body, recipient_list):
    # Set up the SMTP server
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, sender_password)
    
    # Iterate over the recipient list and send emails
    for recipient in recipient_list:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server.sendmail(sender_email, recipient, msg.as_string())
    
    # Quit the SMTP server
    server.quit()

# Read email addresses from CSV file
def read_emails_from_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        recipient_list = [row[0] for row in csv_reader if row]  # Verifică dacă rândul nu este gol
    return recipient_list

# Exemplu de utilizare
smtp_server = 'smtp.gmail.com'
port = 587
sender_email = 'dascaludumitru.pfa@gmail.com'
sender_password = 'cijamghfqjptujdd'
subject = 'Ofertă de preț pentru expedierea pachetelor cu UPS'
body = '''Bună ziua,

Numele meu este Dascalu Dumitru și fac parte din echipa UPS.

Dacă sunteți interesat să primiți o ofertă de preț pentru expedierea pachetelor prin UPS, vă rugăm să ne trimiteți un răspuns la acest email cu următoarele informații:

Numele persoanei de contact/factorului de decizie
Numărul de telefon
Adresa companiei și codul poștal
Informații despre volumul estimat de expediere
Orice alte detalii relevante

Best Regards,
Dascalu Dumitru
UPS Customer Service Representative

UPS România Str. Aurel Vlaicu nr. 11C
Aeroportul Internațional Henri Coandă Otopeni 075150,
județul Ilfov, România Tel.: +4021 233 88 77
E-mail: ddascalu@ups.com dascaludumitru.pfa@gmail.com'''
csv_file_path = 'emails.csv'

recipient_list = read_emails_from_csv(csv_file_path)

send_bulk_emails(smtp_server, port, sender_email, sender_password, subject, body, recipient_list)

print("Bulk emails sent successfully.")