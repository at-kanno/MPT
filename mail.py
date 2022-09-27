from constant import db_path, cc_email, bcc_email, from_email, cset, servername, \
     LOGIN_URL, PASS3_MASSAGE, NEW_ACCOUNT_MESSAGE1,NEW_ACCOUNT_MESSAGE2, END_MESSAGE

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ssl
import sqlite3

def sendMail(to_name, to_email, message):

    rcpt = cc_email.split(",") + bcc_email.split(",") + [to_email]

# MIMETextを作成
    if message == '合格です。':
        message = to_name + '様\n\n' + PASS3_MASSAGE + END_MESSAGE
        subject = "【アーク】ITIL４MP移行　修了試験（合格）のお知らせ"
    else:
        message = to_name + '様\n\n' + NEW_ACCOUNT_MESSAGE1 \
                  + message + NEW_ACCOUNT_MESSAGE2 + END_MESSAGE
        subject = '【アーク】模擬試験システム　ログイン名とパスワードのご案内'

    msg = MIMEText(message, 'plain', cset)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Cc"] = cc_email

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT MAIL_ADR, PASSWORD FROM USER_TABLE where USER_ID = 5;'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

    account = items[0][0]
    password = items[0][1]

# サーバを指定する
    server = smtplib.SMTP_SSL(servername, 465, context=ssl.create_default_context())
    server.set_debuglevel(True)
    if server.has_extn('STARTTLS'):
        server.starttls()

# 認証を行う
    server.login(account, password)
# メールを送信する
    sendToList = to_email.split(',')
    server.sendmail(from_email, rcpt, msg.as_string())
#    server.send_message(msg)
# 閉じる
    return server.quit()
