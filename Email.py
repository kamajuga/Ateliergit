import smtplib
from unidecode import unidecode


def send_mail(unknown_text):
    gmail_user = 'kotamajuga@gmail.com'
    gmail_password = '@Julius619Gauth2Kotan'

    sent_from = gmail_user
    to = ['kotannoujulius@gmail.com']
    subject = unidecode('Nouveau texte ajouté dans la categorie autre.')
    body = unidecode('Nouveau text ajouté a la categorie AUTRE {}'.format(unknown_text))

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ %(sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        #print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)

if __name__=="__main__":
    send_mail("bonjour")
