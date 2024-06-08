#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

rDownloadURL = {"main": "https://bitbucket.org/xoceunder/x-ui/raw/master/main_xui_xoceunder.tar.gz", "sub": "https://bitbucket.org/xoceunder/x-ui/raw/master/sub_xui_xoceunder.tar.gz"}
rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "mariadb-server", "libpng16-16", "python3-paramiko", "python-is-python3"]
install_commands = [
    "wget http://archive.ubuntu.com/ubuntu/pool/universe/libz/libzip/libzip5_1.5.1-0ubuntu1_amd64.deb",
    "sudo dpkg -i libzip5_1.5.1-0ubuntu1_amd64.deb",
    "sudo apt-get install -f"
]
rInstall = {"MAIN": "main", "LB": "sub"}
rUpdate = {"UPDATE": "update"}
rMySQLCnf = base64.b64decode("IyBYdHJlYW0gQ29kZXMKCltjbGllbnRdCnBvcnQgICAgICAgICAgICA9IDMzMDYKCltteXNxbGRfc2FmZV0KbmljZSAgICAgICAgICAgID0gMAoKW215c3FsZF0KdXNlciAgICAgICAgICAgID0gbXlzcWwKcG9ydCAgICAgICAgICAgID0gNzk5OQpiYXNlZGlyICAgICAgICAgPSAvdXNyCmRhdGFkaXIgICAgICAgICA9IC92YXIvbGliL215c3FsCnRtcGRpciAgICAgICAgICA9IC90bXAKbGMtbWVzc2FnZXMtZGlyID0gL3Vzci9zaGFyZS9teXNxbApza2lwLWV4dGVybmFsLWxvY2tpbmcKc2tpcC1uYW1lLXJlc29sdmU9MQoKYmluZC1hZGRyZXNzICAgICAgICAgICAgPSAqCmtleV9idWZmZXJfc2l6ZSA9IDEyOE0KCm15aXNhbV9zb3J0X2J1ZmZlcl9zaXplID0gNE0KbWF4X2FsbG93ZWRfcGFja2V0ICAgICAgPSA2NE0KbXlpc2FtLXJlY292ZXItb3B0aW9ucyA9IEJBQ0tVUAptYXhfbGVuZ3RoX2Zvcl9zb3J0X2RhdGEgPSA4MTkyCnF1ZXJ5X2NhY2hlX2xpbWl0ICAgICAgID0gNE0KcXVlcnlfY2FjaGVfc2l6ZSAgICAgICAgPSAwCnF1ZXJ5X2NhY2hlX3R5cGUJPSAwCgpleHBpcmVfbG9nc19kYXlzICAgICAgICA9IDEwCm1heF9iaW5sb2dfc2l6ZSAgICAgICAgID0gMTAwTQoKbWF4X2Nvbm5lY3Rpb25zICA9IDIwMDAgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbSAKYmFja19sb2cgPSA0MDk2Cm9wZW5fZmlsZXNfbGltaXQgPSAxNjM4NAppbm5vZGJfb3Blbl9maWxlcyA9IDE2Mzg0Cm1heF9jb25uZWN0X2Vycm9ycyA9IDMwNzIKdGFibGVfb3Blbl9jYWNoZSA9IDQwOTYKdGFibGVfZGVmaW5pdGlvbl9jYWNoZSA9IDQwOTYKCgp0bXBfdGFibGVfc2l6ZSA9IDFHCm1heF9oZWFwX3RhYmxlX3NpemUgPSAxRwoKaW5ub2RiX2J1ZmZlcl9wb29sX3NpemUgPSAxMkcgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbQppbm5vZGJfYnVmZmVyX3Bvb2xfaW5zdGFuY2VzID0gMQppbm5vZGJfcmVhZF9pb190aHJlYWRzID0gNjQKaW5ub2RiX3dyaXRlX2lvX3RocmVhZHMgPSA2NAppbm5vZGJfdGhyZWFkX2NvbmN1cnJlbmN5ID0gMAppbm5vZGJfZmx1c2hfbG9nX2F0X3RyeF9jb21taXQgPSAwCmlubm9kYl9mbHVzaF9tZXRob2QgPSBPX0RJUkVDVApwZXJmb3JtYW5jZV9zY2hlbWEgPSBPTgppbm5vZGItZmlsZS1wZXItdGFibGUgPSAxCmlubm9kYl9pb19jYXBhY2l0eT0yMDAwMAppbm5vZGJfdGFibGVfbG9ja3MgPSAwCmlubm9kYl9sb2NrX3dhaXRfdGltZW91dCA9IDAKaW5ub2RiX2RlYWRsb2NrX2RldGVjdCA9IDAKaW5ub2RiX2xvZ19maWxlX3NpemUgPSA1MTJNCgpzcWwtbW9kZT0iTk9fRU5HSU5FX1NVQlNUSVRVVElPTiIKCltteXNxbGR1bXBdCnF1aWNrCnF1b3RlLW5hbWVzCm1heF9hbGxvd2VkX3BhY2tldCAgICAgID0gMTZNCgpbbXlzcWxdCgpbaXNhbWNoa10Ka2V5X2J1ZmZlcl9zaXplICAgICAgICAgICAgICA9IDE2TQo=")

rVersions = {
    "24.04": "noble"
}

class col:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m' # orange on some systems
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def generate(length=19): return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getVersion():
    try: return os.popen("lsb_release -d").read().split(":")[-1].strip()
    except: return ""

def printc(rText, rColour=col.BRIGHT_GREEN, rPadding=0, rLimit=46):
    print("%s ┌─────────────────────────────────────────────────┐ %s" % (rColour, col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    array = [rText[i:i+rLimit] for i in range(0, len(rText), rLimit)]
    for i in array : print("%s │ %s%s%s │ %s" % (rColour, " "*round(23-(len(i)/2)), i, " "*round(46-(22-(len(i)/2))-len(i)), col.ENDC))
    for i in range(rPadding): print("%s │                                                 │ %s" % (rColour, col.ENDC))
    print("%s └─────────────────────────────────────────────────┘ %s" % (rColour, col.ENDC))
    print(" ")

def prepare(rType="MAIN"):
    global rPackages
    idef prepare(rType="MAIN"):
    global rPackages
    if rType != "MAIN": 
        rPackages = rPackages[:-1]
    printc("Preparing Installation")
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        shutil.copyfile('/home/xtreamcodes/iptv_xtream_codes/config', '/tmp/config.xtmp')
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):    
        os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
    
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try: 
            os.remove(rFile)
        except: 
            pass
    
    printc("Updating Operating System")
    os.system("apt-get update > /dev/null")
    os.system("apt-get -y full-upgrade > /dev/null")
    
    if rType == "MAIN":
import os
import sys
import random
import string
import hashlib

class col:
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    RESET = '\033[0m'

def printc(message, color=col.RESET):
    print(f"{color}{message}{col.RESET}")

def generate(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def prepare(rType="MAIN"):
    printc("Preparing system for installation...")
    os.system("apt update -y")
    os.system("apt upgrade -y")
    os.system("apt install -y software-properties-common")
    os.system("add-apt-repository ppa:ondrej/php -y")
    os.system("apt update -y")
    os.system("apt install -y apache2 mysql-server php7.4 php7.4-fpm php7.4-cli php7.4-mysql php7.4-mbstring php7.4-curl php7.4-xml php7.4-zip")
    os.system("a2enmod php7.4")
    os.system("service apache2 restart")
    return True

def install(rType="MAIN"):
    printc("Installing Xtream Codes...")
    os.system("useradd -m -s /bin/bash xtreamcodes")
    os.system("usermod -aG sudo xtreamcodes")
    os.system("wget -O /home/xtreamcodes/iptv_xtream_codes.zip https://example.com/iptv_xtream_codes.zip")
    os.system("unzip /home/xtreamcodes/iptv_xtream_codes.zip -d /home/xtreamcodes/")
    return True

def mysql(rUsername, rPassword):
    printc("Configuring MySQL...")
    os.system(f"mysql -e \"CREATE USER '{rUsername}'@'localhost' IDENTIFIED BY '{rPassword}';\"")
    os.system(f"mysql -e \"GRANT ALL PRIVILEGES ON *.* TO '{rUsername}'@'localhost' WITH GRANT OPTION;\"")
    os.system(f"mysql -e \"FLUSH PRIVILEGES;\"")
    return True

def encrypt(rPassword):
    printc("Encrypting configuration...")
    hashed_password = hashlib.sha256(rPassword.encode()).hexdigest()
    with open("/home/xtreamcodes/iptv_xtream_codes/config", "w") as config_file:
        config_file.write(f"password={hashed_password}\n")
    return True

def configure():
    printc("Finalizing configuration...")
    with open("/etc/fstab", "a") as rFile:
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\n")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/timeshift tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\n")
    os.system("sysctl -w net.core.somaxconn=65535 > /dev/null")
    os.system("sysctl -w fs.file-max=2097152 > /dev/null")
    os.system("echo '* soft nofile 512000\n* hard nofile 512000\nroot soft nofile 512000\nroot hard nofile 512000' >> /etc/security/limits.conf")
    os.system("echo 'fs.file-max=2097152\nnet.ipv4.ip_local_port_range=1024 65000\nnet.core.somaxconn=65535\nnet.core.netdev_max_backlog=262144\nnet.ipv4.tcp_max_syn_backlog=262144\nnet.ipv4.tcp_tw_reuse=1\nnet.ipv4.tcp_fin_timeout=15\nnet.ipv4.tcp_keepalive_time=300\nnet.ipv4.ip_forward=1\nnet.ipv4.conf.default.rp_filter=0\nnet.ipv4.conf.all.rp_filter=0\nnet.core.rmem_max=134217728\nnet.core.wmem_max=134217728\nnet.ipv4.tcp_rmem=10240 87380 134217728\nnet.ipv4.tcp_wmem=10240 87380 134217728' >> /etc/sysctl.conf")
    os.system("sysctl -p > /dev/null")
    os.system("echo 'xtreamcodes soft nofile 512000\nxtreamcodes hard nofile 512000' >> /etc/security/limits.conf")
    os.system("echo 'session required pam_limits.so' >> /etc/pam.d/common-session")
    os.system("chown -R xtreamcodes:xtreamcodes /home/xtreamcodes")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx/sbin/nginx")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/sbin/nginx_rtmp")
    return True

def main():
    printc("Xtream Codes IPTV Installation Script")
    rUsername = "xtreamcodes"
    rPassword = generate(10)
    rType = "MAIN"
    rAction = "INSTALL"
    
    if len(sys.argv) > 1:
        for rArg in sys.argv[1:]:
            if rArg.upper() == "SUB":
                rType = "LB"
            if rArg.upper() == "UPDATE":
                rAction = "UPDATE"

    if rAction == "UPDATE":
        if update(rType):
            printc("Update Complete")
    else:
        if prepare(rType):
            if install(rType):
                if mysql(rUsername, rPassword):
                    encrypt(rPassword=rPassword)
                    configure()
                    printc("Installation Complete")
                else:
                    printc("MySQL Configuration Failed", col.BRIGHT_RED)
            else:
                printc("Installation Failed", col.BRIGHT_RED)
        else:
            printc("Preparation Failed", col.BRIGHT_RED)

if __name__ == "__main__":
    main()
    try: rVersion = os.popen('lsb_release -sr').read().strip()
    except: rVersion = None
    if not rVersion in rVersions:
        printc("Unsupported Operating System, Works only on Ubuntu Server 24")
        sys.exit(1)
    printc("X-UI 22f Ubuntu %s Installer - Masoud Gb" % rVersion, col.GREEN, 2)
    print(" ")
    rType = input("  Installation Type [MAIN, LB, UPDATE]: ")
    print(" ")
    if rType.upper() in ["MAIN", "LB"]:
        if rType.upper() == "LB":
            rHost = input("  Main Server IP Address: ")
            rPassword = input("  MySQL Password: ")
            try: rServerID = int(input("  Load Balancer Server ID: "))
            except: rServerID = -1
            print(" ")
        else:
            rHost = "127.0.0.1"
            rPassword = generate()
            rServerID = 1
        rUsername = "user_iptvpro"
        rDatabase = "xtream_iptvpro"
        rPort = 7999
        if len(rHost) > 0 and len(rPassword) > 0 and rServerID > -1:
            printc("Start installation? Y/N", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                print(" ")
                rRet = prepare(rType.upper())
                if not install(rType.upper()): sys.exit(1)
                if rType.upper() == "MAIN":
                    if not mysql(rUsername, rPassword): sys.exit(1)
                encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
                configure()
                if rType.upper() == "MAIN": 
                    modifyNginx()
                    update(rType.upper())
                start()
                printc("Installation completed!", col.GREEN, 2)
                if rType.upper() == "MAIN":
                    printc("Please store your MySQL password: %s" % rPassword, col.BRIGHT_YELLOW)
                    printc("Admin UI Wan IP: http://%s:25500" % getIP(), col.BRIGHT_YELLOW)
                    printc("Admin UI default login is admin/admin", col.BRIGHT_YELLOW)
                    printc("Save Credentials is file to /root/credentials.txt", col.BRIGHT_YELLOW)
                    rFile = open("/root/credentials.txt", "w")
                    rFile.write("MySQL password: %s\n" % rPassword)
                    rFile.write("Admin UI Wan IP: http://%s:25500\n" % getIP())
                    rFile.write("Admin UI default login is admin/admin\n")
                    rFile.close()
            else: printc("Installation cancelled", col.BRIGHT_RED)
        else: printc("Invalid entries", col.BRIGHT_RED)
    elif rType.upper() == "UPDATE":
        if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/wwwdir/api.php"):
            printc("Update Admin Panel? Y/N?", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                if not update(rType.upper()): sys.exit(1)
                printc("Installation completed!", col.GREEN, 2)
                start()
            else: printc("Install Xtream Codes Main first!", col.BRIGHT_RED)
    else: printc("Invalid installation type", col.BRIGHT_RED)
