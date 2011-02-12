#!/usr/bin/env python
# -*- coding: utf-8; -*-

import flask, json, smtplib, re, threading
from email.mime.text import MIMEText

email_regex = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')

PATH='/home/g/gimnkegru/public_html/vizitka/hall'

app = flask.Flask(__name__)

@app.route('/')
def show():
    log = []
    with open('%s/log.json' % PATH, 'r') as f:
        for line in f:
            log.append(json.loads(line))

    return flask.render_template('posts.html', posts=log)

def post_mail(post):
    message = MIMEText(post['content'].encode('utf-8'))
    message['Subject'] = post['topic'].encode('utf-8')
    message['To'] = 'post@gimn-keg.ru'
    message['From'] = post['email']

    connection = smtplib.SMTP('smtp.spaceweb.ru')
    connection.connect()
    connection.login('gimn-keg.ru+post', 'ubvyfpbz')
    
    connection.sendmail('post@gimn-keg.ru', ['post@gimn-keg.ru'], message.as_string())

def do_post():
    post = {}
    errors = []
    field_map = [('author', u'Не указано имя!'),
                ('email', u'Не указан E-Mail'),
                ('topic', u'Не указана тема сообщения'),
                ('content', u'Отправлено пустое сообщение')]
    
    for field in field_map:
        post[field[0]] = flask.request.form.get(field[0], '')
        if post[field[0]] == '':
            errors.append(field[1])

    if not email_regex.match(post['email']) and post['email']:
        errors.append(u'Неверный e-mail')

    if errors != []:
        return flask.render_template('error.html', errors=errors)

    with open('%s/log.json' % PATH, 'a') as f:
        f.writelines([json.dumps(post, encoding='utf-8')])
        
  #  try:
 #       post_mail(post)
   # except:
    #   pass

    return flask.render_template('ok.html', name=post['author'])

@app.route('/post', methods=['GET', 'POST'])
def post():
    if flask.request.method == 'GET':
        return flask.render_template('post.html', url=flask.url_for('post'))
    elif flask.request.method == 'POST':
        return do_post()

if __name__ == '__main__':
    app.run()
