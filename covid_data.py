import pandas as pd
from datetime import datetime
from threading import Timer

url = "https://www.mygov.in/covid-19"
# Assign the table data to a Pandas dataframe
table = pd.read_html(url)[0]
table.to_excel("data_today.xlsx", sheet_name='Covid_data_today', engine='xlsxwriter')
# Call for next day using date time
x = datetime.today()
y = x.replace(day=x.day+1, hour=11, minute=15, second=0, microsecond=0)
delta_t = y-x

secs = delta_t.seconds+30
# The webpage URL whose table we want to extract
def covid_data():
    url1 = "https://www.mygov.in/covid-19"
    data = pd.read_html(url1)[0]
    data.to_excel("data_tomorrow.xlsx", sheet_name='Covid_data_tomorrow', engine='xlsxwriter')
    df1 = pd.read_excel('data_today.xlsx', sheet_name='Covid_data_today')
    df2 = pd.read_excel('data_tomorrow.xlsx', sheet_name='Covid_data_tomorrow')
    confirmed = df2['Confirmed'] - df1['Confirmed']
    active = df2['Active'] - df1['Active']
    recovered = df2['Recovered'] - df1['Recovered']
    deceased = df2['Deceased'] - df1['Deceased']
    df3 = pd.DataFrame(df1['State/UTs'])
    df4 = pd.DataFrame(confirmed)
    df5 = pd.DataFrame(active)
    df6 = pd.DataFrame(recovered)
    df7 = pd.DataFrame(deceased)
    import openpyxl
    import xlsxwriter
    openpyxl.load_workbook('total.xlsx')
    book = 'total.xlsx'
    with pd.ExcelWriter(book) as writer:
        xlsxwriter.book = openpyxl.load_workbook(book)
        df3.to_excel(writer, sheet_name='total', startrow=0, startcol=1, index=False)
        df4.to_excel(writer, sheet_name='total', startrow=0, startcol=2, index=False)
        df5.to_excel(writer, sheet_name='total', startrow=0, startcol=3, index=False)
        df6.to_excel(writer, sheet_name='total', startrow=0, startcol=4, index=False)
        df7.to_excel(writer, sheet_name='total', startrow=0, startcol=5, index=False)

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    mail_content = '''Hello,
    This is a test mail.
    In this mail we are sending some attachments.
    The mail is sent using Python SMTP library.
    Thank You
    '''
    # The mail addresses and password
    sender_address = 'add sender email'
    import config1
    sender_pass = getattr(config1, 'password', 'default value if not found')
    receiver_address = 'add receiver email'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Covid Data added today.'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'xlsx'))
    attach_file_name = 'total.xlsx'
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'vnd.ms-excel')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

t = Timer(secs, covid_data)
t.start()

