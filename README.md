# **Snippet for send reports on emails**

It can:
- send text with html tags
- send errors with traceback
- attach a file to email

# Parameters
## Reqiured:
- htmltext - a string with/without html tags 
## Optional:
- alias - visible name of sender in email
- to - list of recievers emals
- sbj - email subject
- path_to_attachment - path to file
- filename - you can rename file in attachment

# Examples
Before using this snippet you must fill the constants in send_mail.py or in os environment variables:
```python
ERR_MAILING_LIST = []
MAILING_LIST = []
MAIL_LOGIN = os.getenv('MAIL_LOGIN')
MAIL_PASS = os.getenv('MAIL_PASS')
MAIL_ADDRESS = os.getenv('MAIL_ADDRESS')
SMTP_ADDRESS = os.getenv('SMTP_ADDRESS')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
```
```python
res = send("""Hello!
           This is a test report!""")
print(res)

try:
    raise Exception
except Exception as e:
    send_error(sys.exc_info())
```
