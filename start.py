# Данный  скрипт  не  содержит  реальных  данных, публикация производится с целью тестирования сдредств мониторинга
import os
import socket
import sys
import traceback
import paramiko

username = 'leak'
password = '3yQAcL2geJ'
hostname = 'leak.tcsbank.ru'
port = 22

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
except Exception as e:
    print("*** Connect failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)

try:
    t = paramiko.Transport(sock)
    try:
        t.start_client()
    except paramiko.SSHException:
        print("*** SSH negotiation failed.")
        sys.exit(1)

    path = os.path.join('keys', 'private_key')
    key = paramiko.RSAKey.from_private_key_file(path)
    t.auth_publickey(username, key)

    chan = t.open_session()
    chan.get_pty()
    chan.invoke_shell()
    print("*** Here we go!\n")
    chan.close()
    t.close()

except Exception as e:
    print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)
