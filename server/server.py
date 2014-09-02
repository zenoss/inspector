#!/usr/bin/env python

import os
import sqlite3
import sys
import signal

import bottle as b
b.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 128 #128MB max file size

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, 'static')
b.TEMPLATE_PATH = [os.path.join(ROOT_PATH, 'templates')]

PID = os.getpid()

db = sqlite3.connect("inspector.sqlitedb")
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS inspections(token TEXT PRIMARY KEY, 
               time STRING, hostname STRING)''')
cur.execute('''CREATE TABLE IF NOT EXISTS results(token TEXT, time STRING, 
               script TEXT, stdout TEXT, stderr TEXT)''')

db.commit()

@b.route('/static/<filename>')
@b.route('/static/<static_path:path>/<filename>')
def static(filename, static_path=""):
    return b.static_file(filename, os.path.join(STATIC_PATH, static_path))

@b.post('/insert')
def insert():
    time = b.request.forms.get('time')
    hostname = b.request.forms.get('hostname')
    token = b.request.forms.get('token')
    script = b.request.forms.get('script')
    stdout = b.request.forms.get('stdout')
    stderr = b.request.forms.get('stderr')
    cur.execute('''INSERT OR IGNORE INTO inspections(time, hostname, token) VALUES (?, ?, ?)''',
        (time, hostname, token))
    cur.execute('''INSERT INTO results(time, token, script, stdout, stderr) VALUES (?, ?, ?, ?, ?)''',
        (time, token, script.split('.')[0], stdout, stderr))
    db.commit()

@b.route('/')
def index():
    cur.execute('''SELECT token, hostname, time FROM inspections ORDER BY time DESC LIMIT 100''')
    rows = cur.fetchall()
    return b.template('index.tpl', rows=rows)

@b.route('/inspection/<token>')
def inspection(token):
    cur.execute('''SELECT script, time, stdout, stderr, token FROM results WHERE token=? ORDER BY script ASC''',
        (token,))
    rows = sorted(cur.fetchall(), key=lambda x: x[0])
    return b.template('inspection.tpl', rows=rows)

@b.route('/selfupdate')
def selfupdate():
    os.system('cd %s; git pull; rm -rf server/static/inspector.tar.gz; tar -czvf server/static/inspector.tar.gz inspector' % \
        os.path.join(ROOT_PATH, '..'))
    os.kill(PID, signal.SIGTERM)
    os.kill(PID, signal.SIGKILL)

def main():
    b.run(host='0.0.0.0', port="8080", reloader=False)

if __name__ == '__main__':
    main()

db.close()
