from flask import Flask, render_template, request, Blueprint
from constant import db_path
import sqlite3
from resultDB import getComment

maintenance_module = Blueprint("maintenance", __name__, static_folder='./static')

@maintenance_module.route('/maintenance', methods=['POST'])
def maintenance():
    user_id = int(request.form.get('user_id'))
    command = request.form.get('command')
    if (command == 'retrieve' or command == 'new'):
        if (command == 'retrieve'):
            try:
                qid = int(request.form.get('number'))
            except:
                return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='問題番号が入力されていません。',
                                   )
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            sql = "SELECT CATEGORY,LEVEL,Q,A1,A2,A3,A4,CID1 FROM knowledge_base WHERE " \
              "NUMBER == " + str(qid) + ";"
            try:
                c.execute(sql)
                print("Success!")
            except Exception as e:
                return render_template('error2.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
            else:
                items = c.fetchall()
                n = len(items)
                if n < 1:
                    return render_template('error3.html',
                                       user_id=user_id,
                                       error_message='該当する演習問題はありません。',
                                       )
                category = items[0][0]
                level = items[0][1]
                question = items[0][2]
                answer = items[0][3]
                choice1 = items[0][4]
                choice2 = items[0][5]
                choice3 = items[0][6]
                cid = items[0][7]
                try:
                    comments = getComment(cid)
                except:
                    error_message = '該当する解説がありません。解説番号＝' + str(cid)
                    return render_template('error3.html',
                                       user_id=user_id,
                                       error_message=error_message,
                                       )
        else:
            qid = 0
            category = 0
            level = 0
            question = ""
            answer = ""
            choice1 = ""
            choice2 = ""
            choice3 = ""
            cid = 0
            comments = ""

        return render_template('question.html',
                               user_id=user_id,
                               qid = qid,
                               category = category,
                               level = level,
                               question = question,
                               answer = answer,
                               choice1 = choice1,
                               choice2 = choice2,
                               choice3 = choice3,
                               cid = cid,
                               comments = comments
                               )
    elif (command == 'confirm'):
        old_comments = ''
        qid = int(request.form.get('qid'))
        try:
            category = int(request.form.get('category'))
            level = int(request.form.get('level'))
        except:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='領域、カテゴリに適切な値が入力されていません。',
                                   )
        question = request.form.get('question')
        answer = request.form.get('answer')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        qid = int(request.form.get('qid'))  #必要？
        try:
            cid = int(request.form.get('cid'))
        except:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='解説番号に適切な値が入力されていません。',
                                   )
        comments = request.form.get('comments')
        try:
            flag = int(request.form.get('flag'))
        except:
            flag = 0
        else:
            flag = 1
        if (category < 1 or level < 1):
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='領域、カテゴリに適切な値が入力されていません。',
                                   )
        if (question == '' or answer == '' or choice1 == '' or
                choice2 == '' or choice3 == ''):
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='問題文、選択肢に適切な文字列が記されていません。',
                                   )
        if (flag == 1 ):
            if (cid <= 0 or comments == ''):
                return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='解説番号か解説が適切ではありません。',
                                   )
            else:
                try:
                    old_comments = getComment(cid)
                except:
                    old_comments =''
                else:
                    if(old_comments == comments):
                        flag = 3
                    else:
                        flag = 2
        return render_template('qconfirm.html',
                               user_id=user_id,
                               qid=qid,
                               category = category,
                               level = level,
                               question=question,
                               answer=answer,
                               choice1=choice1,
                               choice2=choice2,
                               choice3=choice3,
                               cid=cid,
                               comments=comments,
                               flag=flag,
                               old_comments=old_comments,
                               )
    elif(command == 'update'):
        qid = int(request.form.get('qid'))
        category = int(request.form.get('category'))
        level = int(request.form.get('level'))
        question = request.form.get('question')
        answer = request.form.get('answer')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        cid = int(request.form.get('cid'))
        comments = request.form.get('comments')
        flag = int(request.form.get('flag'))
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        if (qid != 0):
            sql = 'UPDATE knowledge_base SET CATEGORY=?,LEVEL=?,Q=?,A1=?,A2=?,A3=?,A4=?,CID1=? WHERE NUMBER = ' + str(qid)
        else:
            sql = 'INSERT INTO knowledge_base (CATEGORY,LEVEL,Q,A1,A2,A3,A4,CID1) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        try:
            if (qid == 0):
                conn.execute(sql, [category,level,question, answer, choice1, choice2, choice3,cid])
            else:
                conn.execute(sql, [category,level,question, answer, choice1, choice2, choice3,cid])
            conn.commit()
            if (qid == 0):
                sql = 'select NUMBER from knowledge_base where cid1 = ' + str(cid) + ';'
                c.execute(sql)
                result = c.fetchall()
                qid = result[0][0]
            if(flag == 1):
                conn.execute(
                    'INSERT INTO comments_table ( comment_id, comment ) ' +
                    'VALUES (?, ?)', [cid, comments])
                conn.commit()
            elif(flag == 2):
                sql = "UPDATE comments_table SET COMMENT = '" + comments \
                      + "' WHERE COMMENT_ID = " + str(cid) + ";"
                conn.execute(sql)
                conn.commit()
            conn.close()
            print("Success!")
        except Exception as e:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        else:
            message = "問題番号＝" + str(qid) + "で登録（更新）しました。"
            return render_template('success3.html',
                               user_id=user_id,
                               message = message,
                               )
    elif(command == 'delete'):
        qid = int(request.form.get('qid'))
        question = request.form.get('question')
        answer = request.form.get('answer')
        choice1 = request.form.get('choice1')
        choice2 = request.form.get('choice2')
        choice3 = request.form.get('choice3')
        cid = int(request.form.get('cid'))
        comments = request.form.get('comments')
        flag = 1

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        sql = 'SELECT number from knowledge_base where cid1 = ' + str(cid) + ';'
        try:
            c.execute(sql)
            result = c.fetchall()
        except:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        else:
            n = len(result)
            if n < 1:
                message = '解説がないので、演習問題だけ削除します。よろしいですか？'
                flag = 0
            elif n == 1:
                message = '演習問題と解説を削除します。'
                flag = 1
            else:
                message = '解説は他の演習問題も参照しているので、演習問題だけ削除して解説は削除しません。よろしいですか？'
                flag = 0
            return render_template('del_check.html',
                                   user_id=user_id,
                                   qid=qid,
                                   question=question,
                                   answer=answer,
                                   choice1=choice1,
                                   choice2=choice2,
                                   choice3=choice3,
                                   cid=cid,
                                   comments=comments,
                                   message=message,
                                   flag=flag,
                                   )
    elif(command == 'deletey'):
        qid = int(request.form.get('qid'))
        cid = int(request.form.get('cid'))
        flag = int(request.form.get('flag'))
        conn = sqlite3.connect(db_path)

        sql = 'DELETE from knowledge_base where number = ' + str(qid) + ';'
        try:
            conn.execute(sql)
            if flag == 1:
                sql = 'DELETE from comments_table where comment_id = ' + str(cid) + ';'
                conn.execute(sql)
            conn.commit()
        except:
            return render_template('error3.html',
                                   user_id=user_id,
                                   error_message='エラーが発生しました。',
                                   )
        else:
            message = "問題番号＝" + str(qid) + "を削除しました。"
            return render_template('success3.html',
                                   user_id=user_id,
                                   message=message,
                                   )
        conn.close()
    else:
        return render_template('error2.html',
                               user_id=user_id,
                               error_message='要求を処理できませんでした。',
                               )

