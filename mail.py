import sqlite3, os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ssl

LOGIN_URL = 'http://54.163.203.19:5000/'
PASS3_MASSAGE = 'おめでとうございます。合格です。\n頑張ってこられた成果が出ました。\n\n' \
    + '修了試験と提出課題の２つをクリアすることで、PeopleCertの本試験を受験することができます。\n' \
    + 'まだ課題を提出していない場合は、提出をお願いします。\n\n' \
    + '受験要件を満たしたことがアークで確認できましたら、バウチャー（ITIL本試験受験権利コード)を発行します。\n\n' \
    + '試験実施機関のPeopleCert社から連絡がありますので、その内容に従い、都合のよい受験日時を予約登録してください。'

NEW_ACCOUNT_MESSAGE1 = '模擬試験システムのアカウントを作成しました。\n\n' \
    + '模擬試験システムには、以下のURLからログインしてください。\n  ' + LOGIN_URL + \
    '\nログイン名は、研修お申込み時に記載のメールアドレスです。\n\n初期パスワードは「'
NEW_ACCOUNT_MESSAGE2 = '」です。\nパスワードの変更は、システムの管理画面から可能です。\n\n' + \
    'ご不明な点がございましたら、遠慮なくご連絡ください。'

END_MESSAGE = '\n\n株式会社アーク\nTEL：03-5577-5311\n代表email: ark@gigamall.ne.jp\n' + \
    '\n本メールにご返信いただいても対応できません。\n上記メールアドレスにご連絡ください。'

base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'

def sendMail(to_name, to_email, message):

# 送受信先
#    cc_email = "at.kanno@icloud.com"
#    bcc_email = "atsushi.kanno@nifty.com"
    cc_email = "ark@gigamall.ne.jp"
    bcc_email = "hiroko@mail.co.jp,miyauchi.ark@gmail.com,kanno@olivenet.co.jp"
    from_email = "ITIL4 Exercise System"
    rcpt = cc_email.split(",") + bcc_email.split(",") + [to_email]

    cset = 'utf-8'
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
