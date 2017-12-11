# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from __future__ import print_function
from flask import Flask, render_template, request, url_for, flash
import ctypes  # An included library with Python install..
from functions import Mbox
import tkMessageBox
#Para conexiones ssh
import paramiko

# Initialize the Flask application
app = Flask(__name__)


def connect(host,user,password,port):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host,int(port),user,password)
    return client

# Define a route for the default URL, which loads the form
@app.route('/')
def form():

    return render_template('form_connect.html')

@app.route('/configfile/', methods=['POST'])
def configfile():

    global client

    if request.form["btn"] == "Send":

        client.exec_command("sudo /etc/init.d/myservice.sh stop")
        client.exec_command("sudo killall -9 python")

        #parsear las respuestas
        #Parsear los checkbox
        try:
            if request.form["detections_wifi"] == "True":
                enable_wifi_scan = "enable_wifi_scan = " + "True"

        except:
            enable_wifi_scan = "enable_wifi_scan = " + "False"


        try:
            if request.form["detections_bluetooth"] == "True":
                enable_bluetooth_scan = "enable_bluetooth_scan = " + "True"
        except:
            enable_bluetooth_scan = "enable_bluetooth_scan = " + "False"


        host = "host = " + request.form['host']
        comunication_port = "comunication_port = "+ request.form['comunication_port']
        date_sincronize_port = "date_sincronize_port = " + request.form['date_sincronize_port']
        dispositivo_id = "dispositivo_id = " + request.form["dispositivo_id"]

        command_port_date = "sed -i 's/date_sincronize_port = /" + date_sincronize_port + "/g' config.txt"
        command_port = "sed -i 's/comunication_port = /" + comunication_port + "/g' config.txt"
        command_host = "sed -i 's/host = /" + host + "/g' config.txt"
        command_dispositivo_id = "sed -i 's/dispositivo_id = /" + dispositivo_id + "/g' config.txt"
        enable_bluetooth_scan = "sed -i 's/enable_bluetooth_scan = /" + enable_bluetooth_scan + "/g' config.txt"
        enable_wifi_scan = "sed -i 's/enable_wifi_scan = /" + enable_wifi_scan + "/g' config.txt"
        client.exec_command(command_port)
        client.exec_command(command_port_date)
        client.exec_command(command_host)
        client.exec_command(command_dispositivo_id)
        client.exec_command(enable_bluetooth_scan)
        client.exec_command(enable_wifi_scan)
        return render_template('form_configfile.html')
    if request.form["btn"] == "Stop":
        # iniciar otra vez el servicio
        stdin, stdout, stderr = client.exec_command("sudo /etc/init.d/myservice.sh stop")
        if stdout.channel.recv_exit_status() == 0:
            Mbox("Estado del servicio", "El servicio se ha parado correctamente", 0x40)
        else:
            Mbox("Estado del servicio", "El servicio no se ha parado correctamente", 0x10)
        return render_template('form_configfile.html')
    if request.form["btn"] == "Start":
        #iniciar otra vez el servicio
        stdin, stdout, stderr = client.exec_command("sudo /etc/init.d/myservice.sh start")
        if stdout.channel.recv_exit_status() == 0:
            Mbox("Estado del servicio", "El servicio se ha iniciado correctamente", 0x40)
        else:
            Mbox("Estado del servicio", "El servicio no se ha iniciado correctamente", 0x10)
        return render_template('form_configfile.html')
        #Reiniciar el servicio
    if request.form["btn"] == "Restart":
        client.exec_command("sudo /etc/init.d/myservice.sh stop")
        client.exec_command("sudo killall -9 python")

        stdin, stdout, stderr = client.exec_command("sudo /etc/init.d/myservice.sh start")
        if stdout.channel.recv_exit_status() == 0:
            Mbox("Estado del servicio", "El servicio se ha iniciado correctamente", 0x40)
        else:
            Mbox("Estado del servicio", "El servicio no se ha iniciado correctamente", 0x10)
        return render_template('form_configfile.html')
    if request.form["btn"] == "State":

        stdin, stdout, stderr = client.exec_command("sudo /etc/init.d/myservice.sh status")
        if stdout.channel.recv_exit_status() == 0:
            Mbox("Estado del servicio","El servicio esta en marcha",0x40)
        else:
            Mbox("Estado del servicio", "El servicio no esta en marcha", 0x10)
        return render_template('form_configfile.html')
    if request.form["btn"] == "IP_Configure":
        return render_template('form_ip_configure.html')





# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/raspiconnect/', methods=['POST'])
def raspiconnect():
    global client
    try:
        host = request.form['host']
        user = request.form['user']


        password = request.form['password']
        port = request.form["port"]
        client = connect(host,user,password,port)
        return render_template('form_configfile.html')
    except:

        Mbox("Login incorrecto", "Error login", 0x10)
        return render_template('form_connect.html')

@app.route('/configurenetwork/', methods=['POST'])
def configurenetwork():
    Mbox("Login incorrecto", "Error login", 0x10)


# Run the app :)
if __name__ == '__main__':
  app.run(host="192.168.1.30")

