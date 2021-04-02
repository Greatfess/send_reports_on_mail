import os
import smtplib
import ssl
import sys
import traceback as tcb
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ERR_MAILING_LIST = []
MAILING_LIST = []
MAIL_LOGIN = os.getenv('MAIL_LOGIN')
MAIL_PASS = os.getenv('MAIL_PASS')
MAIL_ADDRESS = os.getenv('MAIL_ADDRESS')
SMTP_ADDRESS = os.getenv('SMTP_ADDRESS')
SMTP_PORT = os.getenv('SMTP_PORT', 587)


def send(htmltext, alias='Visible_name', to=ERR_MAILING_LIST,
         sbj='Report', path_to_attachment=None, filename='Report.xlsx'):
    try:
        cont = ssl._create_unverified_context(protocol=ssl.PROTOCOL_TLS_CLIENT)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sbj
        msg['From'] = alias

        html = f"""\
        <html>
            <head></head>
            <body>
            {htmltext}
            </body>
        </html>
        """
        msg.attach(MIMEText(html, 'html'))

        if path_to_attachment and os.path.exists(path_to_attachment):
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(path_to_attachment, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f'attachment; filename="{filename}"')
            msg.attach(part)

        with smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT) as smtpserver:
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(MAIL_LOGIN, MAIL_PASS)
            smtpserver.sendmail(MAIL_ADDRESS,
                                to,
                                msg.as_string())
            return 'report sent'
    except Exception as e:
        return f'Error: {str(e)}'


def send_error(exc_info):
    exc_type, exc_value, exc_tb = exc_info
    html = '<pre>'
    for err_line in tcb.format_exception(exc_type, exc_value, exc_tb):
        html += err_line.replace("\n", "&#10;&#13;")
    html += '</pre>'
    send(html, sbj="Error Report", to=ERR_MAILING_LIST)


if __name__ == "__main__":
    res = send("""Hello!
               This is a test report!""")
    print(res)

    try:
        raise Exception
    except Exception as e:
        send_error(sys.exc_info())
