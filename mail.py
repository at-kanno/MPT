import sqlite3, os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ssl

#SECOND_TEST = "修了試験"
SECOND_TETST = "実力確認試験"

PASS3_MASSAGE = "おめでとうございます。合格です。\n頑張ってこられた成果が出ました。\n" \
    + "これより、本試験（認定試験）の手配を行います。\n　" \
    + "試験実施機関のPeopleCer社tから連絡がありますので、その内容に従い、都合のよい日時を設定してください。"

base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'

def sendMail(to_name, to_email, message):

# 送受信先
    cc_email = "at.kanno@icloud.com"
    bcc_email = "atsushi.kanno@nifty.com"
#    cc_email = "ark@gigamall.ne.jp"
#    bcc_email = "hiroko@mail.co.jp,miyauchi.ark@gmail.com,kanno@olivenet.co.jp"
    from_email = "ITIL4 Exercise System"
    rcpt = cc_email.split(",") + bcc_email.split(",") + [to_email]

    cset = 'utf-8'
# MIMETextを作成
    message = to_name + "様、\n\n" + PASS3_MASSAGE + "\n\n株式会社アーク"
    msg = MIMEText(message, 'plain', cset)
    msg["Subject"] = SECOND_TEST + '【合格】'
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

    servername = "smtp.gmail.com"

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
