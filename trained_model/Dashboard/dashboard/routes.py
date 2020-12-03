from dashboard import app
from flask import render_template, flash, redirect, url_for, send_from_directory, request, abort
from werkzeug.utils import secure_filename
from os import path
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

current_file = "default.png"
alert = "Waiting for personnel to enter..."
count = 0
status = "Room is under occupancy limit"
alert_class = "normal"

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global current_file, alert, status, count, alert_class
    if request.method == 'POST':
        file_upload = request.files['file']
        filename = secure_filename(file_upload.filename)
        if filename != '':
            file_ext = path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                current_file = "default.png"
                abort(400)
            current_file = filename
            file_upload.save(path.join("dashboard/" + app.config['UPLOAD_PATH'], filename))
            client = socket(AF_INET, SOCK_STREAM)
            client.connect(("127.0.0.1", 12000))
            sleep(1)
            client.send(current_file.encode("UTF-8"))
            data = client.recv(1024)
            result = data.decode("UTF8")
            print(result)
            if result == "True": 
                print("Mask detected")
                alert = "Mask detected!"
                alert_class = "normal"
            else:
                print("No mask detected")
                alert = "Warning: Mask not detected!"
                alert_class = "warning"
            
            count += 1
            if count == 10:
                status = "Room has reached maximum capacity"
            elif count > 10:
                status = "Room has exceeded maximum capacity"
            
        return redirect(url_for('index'))
    return render_template('index.html', current_file=current_file, count=count, alert=alert, status=status, alert_class=alert_class)

@app.route('/static/images/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
    
