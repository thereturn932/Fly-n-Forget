import paramiko
import pysftp as sftp
import os

client = paramiko.SSHClient()

def connect(_host, _user, _pwd):
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(_host, username=_user, password=_pwd)
    ftp = sftp.Connection(host = _host, username=_user, password=_pwd)
    return ftp

def move_files(ftp):
    filelist = os.listdir('images')
    for fileName in filelist:
        ftp.put("images/"+fileName,'/home/pi/FlynForget/images/' + fileName)
    ftp.put("waypoints.txt",'/home/pi/FlynForget/waypoints.txt')

def start_search(_ip = '192.168.137.171', _user = 'pi', _pass = 'raspberry'):
    print('Connecting Device...')
    ftp = connect(_ip, _user, _pass)
    print('Connected!')
    stdin, stdout, stderr = client.exec_command('rm -r /home/pi/FlynForget/images/*')
    move_files(ftp)
    print('Files Moved')
    stdin, stdout, stderr = client.exec_command('python /home/pi/FlynForget/start_system.py')
    print(stdout)
