#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64, glob, textwrap
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

rDownloadURL = {"main": "https://bitbucket.org/masoudgb/xtream-ui/raw/master/main_xui_masoudgb.zip", "sub": "https://bitbucket.org/masoudgb/xtream-ui/raw/master/sub_xui_masoudgb.zip"}
rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "mariadb-server", "libpng16-16", "python3-paramiko", "python-is-python3"]
rInstall = {"MAIN": "main", "LB": "sub"}
rUpdate = {"UPDATE": "update"}
rMySQLCnf = base64.b64decode("IyBYdHJlYW0gQ29kZXMgLSBVcGRhdGVkIGZvciBNYXJpYURCIDExLjUKCltjbGllbnRdCnBvcnQgPSAzMzA2Cgpb bXlzcWxkX3NhZmVdCm5pY2UgPSAwCgpb bXlzcWxkXQp1c2VyID0gbXlzcWwKcG9ydCA9IDc5OTkKYmFzZWRpciA9IC91c3IKZGF0YWRpciA9IC92YXIvbGliL215c3FsCnRtcGRpciA9IC90bXAKbGMtbWVzc2FnZXMtZGlyID0gL3Vzci9zaGFyZS9teXNxbApza2lwLWV4dGVybmFsLWxvY2tpbmcKc2tpcC1uYW1lLXJlc29sdmU9MQoKYmluZC1hZGRyZXNzID0gKgprZXlfYnVmZmVyX3NpemUgPSAxMjhNCgpteWlzYW0tcmVjb3Zlci1vcHRpb25zID0gQkFDS1VQCm1heF9hbGxvd2VkX3BhY2tldCA9IDY0TQptYXhfbGVuZ3RoX2Zvcl9zb3J0X2RhdGEgPSA4MTkyCnF1ZXJ5X2NhY2hlX2xpbWl0ID0gNE0KcXVlcnlfY2FjaGVfc2l6ZSA9IDAKcXVlcnlfY2FjaGVfdHlwZSA9IDAKCmV4cGlyZV9sb2dzX2RheXMgPSAxMAptYXhfYmlubG9nX3NpemUgPSAxMDBNCgptYXhfY29ubmVjdGlvbnMgPSAyMDAwCmJhY2tfbG9nID0gNDA5NgpvcGVuX2ZpbGVzX2xpbWl0ID0gMTYzODQKaW5ub2RiX29wZW5fZmlsZXMgPSAxNjM4NAptYXhfY29ubmVjdF9lcnJvcnMgPSAzMDcyCnRhYmxlX29wZW5fY2FjaGUgPSA0MDk2CnRhYmxlX2RlZmluaXRpb25fY2FjaGUgPSA0MDk2Cgp0bXBfdGFibGVfc2l6ZSA9IDFH bWF4X2hlYXBfdGFibGVfc2l6ZSA9IDFHCgppbm5vZGJfYnVmZmVyX3Bvb2xfc2l6ZSA9IDEyOE0KaW5ub2RiX2xvZ19maWxlX3NpemUgPSAyNTZNCmlubm9kYl9sb2dfYnVmZmVyX3NpemUgPSAxNk0KaW5ub2RiX2ZsdXNoX2xvZ19hdF90cnhfY29tbWl0ID0gMgppbm5vZGJfZmx1c2hfbWV0aG9kID0gT19ESVJFQ1QKcGVyZm9ybWFuY2Vfc2NoZW1hID0gT04KaW5ub2RiLWZpbGUtcGVyLXRhYmxlID0gMQppbm5vZGJfaW9fY2FwYWNpdHkgPSAyMDAwMAppbm5vZGJfcmVhZF9pb190aHJlYWRzID0gNjQKaW5ub2RiX3dyaXRlX2lvX3RocmVhZHMgPSA2NAppbm5vZGJfdGFibGVfbG9ja3MgPSAwCmlubm9kYl9sb2NrX3dhaXRfdGltZW91dCA9IDAKaW5ub2RiX2RlYWRsb2NrX2RldGVjdCA9IDAKCnNxbC1tb2RlID0gIk5PX0VOR0lORV9TVUJTVElUVVRJT04iCgpbbXlzcWxkdW1wXQpxdWljawpxdW90ZS1uYW1lcwptYXhfYWxsb3dlZF9wYWNrZXQgPSAxNk0=")

rVersions = {
    "24.04": "noble",
    "26.04": "noble"
}

class col:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
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

def term_width():
    try:
        return shutil.get_terminal_size((60, 20)).columns
    except Exception:
        return 60

def printc(rText, rColour=col.BRIGHT_GREEN, rPadding=0, rLimit=None):
    width = term_width()
    box_w = min(36, max(30, width - 6))
    h_pad = 2 
    
    if rLimit is None:
        rLimit = box_w - (h_pad * 2)

    wrapped_lines = []
    for paragraph in rText.split('\n'):
        lines = textwrap.wrap(paragraph, width=rLimit)
        if not lines:
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(lines)

    total_inner_w = box_w + (h_pad * 2) - 2
    top = "%s┏%s┓%s" % (rColour, "━" * total_inner_w, col.ENDC)
    bot = "%s┗%s┛%s" % (rColour, "━" * total_inner_w, col.ENDC)
    
    print(top)
    
    for _ in range(rPadding):
        print("%s┃%s┃%s" % (rColour, " " * total_inner_w, col.ENDC))
        
    for line in wrapped_lines:
        pad_total = total_inner_w - len(line)
        left_space = (pad_total // 2)
        right_space = pad_total - left_space
        
        if left_space < h_pad:
            left_space = h_pad
            right_space = total_inner_w - len(line) - left_space
            
        print("%s┃%s%s%s%s┃%s" % (rColour, " "*left_space, line, " "*right_space, col.ENDC))
        
    for _ in range(rPadding):
        print("%s┃%s┃%s" % (rColour, " " * total_inner_w, col.ENDC))
        
    print(bot)
    print(" ")

def is_installed(package_name):
    try:
        subprocess.run(['dpkg', '-s', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def prepare(rType="MAIN"):
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
        except FileNotFoundError:
            pass

    printc("Updating Operating System")
    subprocess.run("apt-get update -y > /dev/null 2>&1", shell=True)
    subprocess.run("apt-get -y full-upgrade > /dev/null 2>&1", shell=True)

    if rType == "MAIN":
        printc("Install MariaDB 11.5 repository")
        subprocess.run("apt-get install -y software-properties-common > /dev/null 2>&1", shell=True)
        subprocess.run("curl -fsSL https://mariadb.org/mariadb_release_signing_key.asc | gpg --dearmor -o /usr/share/keyrings/mariadb-archive-keyring.gpg > /dev/null 2>&1", shell=True)
        subprocess.run(
            "echo y | sudo add-apt-repository -y 'deb [arch=amd64,arm64,ppc64el,s390x] [signed-by=/usr/share/keyrings/mariadb-archive-keyring.gpg] https://mirrors.xtom.com/mariadb/repo/11.5/ubuntu noble main' > /dev/null 2>&1",
            shell=True
        )
        subprocess.run("apt-get update -y > /dev/null 2>&1", shell=True)

    for rPackage in rPackages:
        if not is_installed(rPackage):
            printc(f"Installing {rPackage}")
            subprocess.run(f"apt-get install {rPackage} -y > /dev/null 2>&1", shell=True)

    if not is_installed("libssl1.1"):
        printc("Installing libssl1.1")
        subprocess.run("curl -L -o libssl1.1_1.1.0g-2ubuntu4_amd64.deb http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb > /dev/null 2>&1 && sudo dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb > /dev/null 2>&1 && rm -rf libssl1.1_1.1.0g-2ubuntu4_amd64.deb > /dev/null 2>&1", shell=True)

    if not is_installed("libzip5"):
        printc("Installing libzip5")
        subprocess.run("curl -L -o libzip5_1.5.1-0ubuntu1_amd64.deb http://archive.ubuntu.com/ubuntu/pool/universe/libz/libzip/libzip5_1.5.1-0ubuntu1_amd64.deb > /dev/null 2>&1 && sudo dpkg -i libzip5_1.5.1-0ubuntu1_amd64.deb > /dev/null 2>&1 && rm -rf libzip5_1.5.1-0ubuntu1_amd64.deb > /dev/null 2>&1", shell=True)

    subprocess.run("sudo apt-get install -f -y > /dev/null 2>&1", shell=True)

    python_installed = is_installed("python2.7")
    pip_installed = subprocess.run("pip2.7 --version > /dev/null 2>&1", shell=True).returncode == 0
    paramiko_installed = subprocess.run("pip2.7 show paramiko > /dev/null 2>&1", shell=True).returncode == 0

    if not python_installed or not pip_installed or not paramiko_installed:
        printc("Installing python2 & pip2 & paramiko")
        subprocess.run("sudo apt install -y build-essential checkinstall libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev curl tar > /dev/null 2>&1", shell=True)

        if not python_installed:
            subprocess.run("cd /usr/src && sudo curl -L -O https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz > /dev/null 2>&1 && sudo tar xzf Python-2.7.18.tgz > /dev/null 2>&1 && cd Python-2.7.18 && sudo ./configure --enable-optimizations > /dev/null 2>&1 && sudo make altinstall > /dev/null 2>&1", shell=True)

        if not pip_installed:
            subprocess.run("curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py > /dev/null 2>&1 && sudo python2.7 get-pip.py > /dev/null 2>&1", shell=True)

        if not paramiko_installed:
            subprocess.run("pip2.7 install paramiko > /dev/null 2>&1", shell=True)

    subprocess.run("apt-get install -f -y > /dev/null 2>&1", shell=True)

    try:
        subprocess.run("getent passwd xtreamcodes > /dev/null 2>&1", shell=True, check=True)
    except subprocess.CalledProcessError:
        printc("Creating user xtreamcodes")
        subprocess.run("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null 2>&1", shell=True)

    if not os.path.exists("/home/xtreamcodes"):
        os.mkdir("/home/xtreamcodes")

    return True

def install(rType="MAIN"):
    global rInstall, rDownloadURL
    printc("Downloading Software")
    
    try:
        rURL = rDownloadURL[rInstall[rType]]
    except KeyError:
        printc("Invalid download URL!", col.BRIGHT_RED)
        return False

    zip_file_path = "/tmp/xtreamcodes.zip"
    try:
        subprocess.run(['curl', '-L', '-s', '-o', zip_file_path, rURL], check=True)
    except subprocess.CalledProcessError:
        printc("Failed to download installation file!", col.BRIGHT_RED)
        return False

    if os.path.exists(zip_file_path):
        printc("Installing Software")
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall("/home/xtreamcodes/")
        except zipfile.BadZipFile:
            printc(f"Error: {zip_file_path} is not a valid zip file!", col.BRIGHT_RED)
            return False

        try:
            os.remove(zip_file_path)
        except OSError as e:
            printc(f"Error removing file {zip_file_path}: {e.strerror}")
        return True
    
    printc("Failed to download installation file!", col.BRIGHT_RED)
    return False

def update(rType="MAIN"):
    if rType == "UPDATE":
        rlink = "https://bitbucket.org/masoudgb/xtream-ui/raw/master/update.zip"
    else:
        rlink = "https://bitbucket.org/masoudgb/xtream-ui/raw/master/release_22f.zip"
        printc("Downloading Software Update")  
    os.system('curl -L -s -o "/tmp/update.zip" "%s"' % rlink)
    if os.path.exists("/tmp/update.zip"):
        try: is_ok = zipfile.ZipFile("/tmp/update.zip")
        except:
            printc("Invalid link or zip file is corrupted!", col.BRIGHT_RED)
            os.remove("/tmp/update.zip")
            return False
    rURL = rlink
    printc("Installing Admin Panel")
    if os.path.exists("/tmp/update.zip"):
        try: is_ok = zipfile.ZipFile("/tmp/update.zip")
        except:
            printc("Invalid link or zip file is corrupted!", col.BRIGHT_RED)
            os.remove("/tmp/update.zip")
            return False
        printc("Updating Software")
        os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null && rm -rf /home/xtreamcodes/iptv_xtream_codes/admin > /dev/null && rm -rf /home/xtreamcodes/iptv_xtream_codes/pytools > /dev/null && unzip /tmp/update.zip -d /tmp/update/ > /dev/null && cp -rf /tmp/update/XtreamUI-master/* /home/xtreamcodes/iptv_xtream_codes/ > /dev/null && rm -rf /tmp/update/XtreamUI-master > /dev/null && rm -rf /tmp/update > /dev/null && chown -R xtreamcodes:xtreamcodes /home/xtreamcodes/ > /dev/null && chmod +x /home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null && chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
        if not "sudo chmod 400 /home/xtreamcodes/iptv_xtream_codes/config" in open("/home/xtreamcodes/iptv_xtream_codes/permissions.sh").read(): os.system('echo "#!/bin/bash\nsudo chmod -R 777 /home/xtreamcodes 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/admin/ -type f -exec chmod 644 {} \\; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/admin/ -type d -exec chmod 755 {} \\; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/wwwdir/ -type f -exec chmod 644 {} \\; 2>/dev/null\nsudo find /home/xtreamcodes/iptv_xtream_codes/wwwdir/ -type d -exec chmod 755 {} \\; 2>/dev/null\nsudo chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx/sbin/nginx 2>/dev/null\nsudo chmod +x /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/sbin/nginx_rtmp 2>/dev/null\nsudo chmod 400 /home/xtreamcodes/iptv_xtream_codes/config 2>/dev/null" > /home/xtreamcodes/iptv_xtream_codes/permissions.sh')
        os.system("/home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null")
        try: os.remove("/tmp/update.zip")
        except: pass
        return True
    printc("Failed to download installation file!", col.BRIGHT_RED)
    return False

def mysql(rUsername, rPassword):
    global rMySQLCnf
    printc("Configuring MySQL")
    rCreate = True
    if os.path.exists("/etc/mysql/my.cnf"):
        if open("/etc/mysql/my.cnf", "r").read(14) == "# Xtream Codes": rCreate = False
    if rCreate:
        shutil.copy("/etc/mysql/my.cnf", "/etc/mysql/my.cnf.xc")
        rFile = open("/etc/mysql/my.cnf", "wb")
        rFile.write(rMySQLCnf)
        rFile.close()
        os.system("systemctl restart mariadb > /dev/null")
        os.system('mysql -u root -e "SET GLOBAL innodb_log_file_size=268435456;" > /dev/null 2>&1')
    for i in range(5):
        rMySQLRoot = ""
        print(" ")
        if len(rMySQLRoot) > 0: rExtra = " -p%s" % rMySQLRoot
        else: rExtra = ""
        rDrop = True
        try:
            if rDrop:
                os.system('mysql -u root%s -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;" > /dev/null' % rExtra)
                os.system('mysql -u root%s -e "USE xtream_iptvpro; DROP USER IF EXISTS \'%s\'@\'%%\';" > /dev/null' % (rExtra, rUsername))
                os.system("mysql -u root%s xtream_iptvpro < /home/xtreamcodes/iptv_xtream_codes/database.sql > /dev/null" % rExtra)
                os.system('mysql -u root%s -e "USE xtream_iptvpro; UPDATE settings SET live_streaming_pass = \'%s\', unique_id = \'%s\', crypt_load_balancing = \'%s\';" > /dev/null' % (rExtra, generate(20), generate(10), generate(20)))
                os.system('mysql -u root%s -e "USE xtream_iptvpro; REPLACE INTO streaming_servers (id, server_name, domain_name, server_ip, vpn_ip, ssh_password, ssh_port, diff_time_main, http_broadcast_port, total_clients, system_os, network_interface, latency, status, enable_geoip, geoip_countries, last_check_ago, can_delete, server_hardware, total_services, persistent_connections, rtmp_port, geoip_type, isp_names, isp_type, enable_isp, boost_fpm, http_ports_add, network_guaranteed_speed, https_broadcast_port, https_ports_add, whitelist_ips, watchdog_data, timeshift_only) VALUES (1, \'Main Server\', \'\', \'%s\', \'\', NULL, NULL, 0, 25461, 1000, \'%s\', \'eth0\', 0, 1, 0, \'\', 0, 0, \'{}\', 3, 0, 25462, \'low_priority\', \'\', \'low_priority\', 0, 1, \'\', 1000, 25463, \'\', \'[\"127.0.0.1\",\"\"]\', \'{}\', 0);" > /dev/null' % (rExtra, getIP(), getVersion()))
                os.system('mysql -u root%s -e "USE xtream_iptvpro; REPLACE INTO reg_users (id, username, password, email, member_group_id, verified, status) VALUES (1, \'admin\', \'\\$6\\$rounds=20000\\$xtreamcodes\\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\', \'admin@website.com\', 1, 1, 1);" > /dev/null'  % rExtra)
                os.system('mysql -u root%s -e "CREATE USER \'%s\'@\'%%\' IDENTIFIED BY \'%s\'; GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO \'%s\'@\'%%\' WITH GRANT OPTION; GRANT SELECT, LOCK TABLES ON *.* TO \'%s\'@\'%%\';FLUSH PRIVILEGES;" > /dev/null' % (rExtra, rUsername, rPassword, rUsername, rUsername))
                os.system('mysql -u root%s -e "USE xtream_iptvpro; CREATE TABLE IF NOT EXISTS dashboard_statistics (id int(11) NOT NULL AUTO_INCREMENT, type varchar(16) NOT NULL DEFAULT \'\', time int(16) NOT NULL DEFAULT \'0\', count int(16) NOT NULL DEFAULT \'0\', PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=latin1; INSERT INTO dashboard_statistics (type, time, count) VALUES(\'conns\', UNIX_TIMESTAMP(), 0),(\'users\', UNIX_TIMESTAMP(), 0);" > /dev/null' % rExtra)
            try: os.remove("/home/xtreamcodes/iptv_xtream_codes/database.sql")
            except: pass
            return True
        except: printc("Invalid password! Try again", col.BRIGHT_RED)
    return False

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        rDecrypt = decrypt()
        rHost = rDecrypt["host"]
        rPassword = rDecrypt["db_pass"]
        rServerID = int(rDecrypt["server_id"])
        rUsername = rDecrypt["db_user"]
        rDatabase = rDecrypt["db_name"]
        rPort = int(rDecrypt["db_port"])
    printc("Encrypting")
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass

    rf = open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb')
    lestring=''.join(chr(ord(c)^ord(k)) for c,k in zip('{"host":"%s","db_user":"%s","db_pass":"%s","db_name":"%s","server_id":"%d", "db_port":"%d"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
    rf.write(base64.b64encode(bytes(lestring, 'ascii')))
    rf.close()


def decrypt():
    rConfigPath = "/home/xtreamcodes/iptv_xtream_codes/config"
    try: return json.loads(''.join(chr(c^ord(k)) for c,k in zip(base64.b64decode(open(rConfigPath, 'rb').read()), cycle('5709650b0d7806074842c6de575025b1'))))
    except: return None

def configure():
    printc("Configuring System")
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    if not "xtreamcodes" in open("/etc/sudoers").read():
        os.system('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables, /usr/bin/chattr" >> /etc/sudoers')
    if not os.path.exists("/etc/init.d/xtreamcodes"):
        rFile = open("/etc/init.d/xtreamcodes", "w")
        rFile.write("#! /bin/bash\n/home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        rFile.close()
        os.system("chmod +x /etc/init.d/xtreamcodes > /dev/null")
        os.system("systemctl daemon-reload > /dev/null")
    try: os.remove("/usr/bin/ffmpeg")
    except: pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb"): os.system("curl -L -s -o /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb https://bitbucket.org/masoudgb/xtream-ui/raw/master/GeoLite2.mmdb")
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php"): os.system("curl -L -s -o /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php https://bitbucket.org/masoudgb/xtream-ui/raw/master/pid_monitor.php")
    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("chattr -ai /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sudo chmod 0777 /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
    os.system("mount -a")
    os.system("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config > /dev/null")
    os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not "xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    if not "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" in open("/etc/crontab").read(): os.system('echo "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" >> /etc/crontab')

def start(first=True):
    if first: printc("Starting Xtream Codes")
    else: printc("Restarting Xtream Codes")
    os.system("/home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
    
def modifyNginx():
    printc("Modifying Nginx")
    rPath = "/home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf"
    rPrevData = open(rPath, "r").read()

    if "listen 25500;" not in rPrevData:
        shutil.copy(rPath, f"{rPath}.xc")

        new_server_block = """
    server {
        listen 25500;
        index index.php index.html index.htm;
        root /home/xtreamcodes/iptv_xtream_codes/admin/;

        location ~ \\.php$ {
            limit_req zone=one burst=8;
            try_files $uri =404;
            fastcgi_index index.php;
            fastcgi_pass php;
            include fastcgi_params;
            fastcgi_buffering on;
            fastcgi_buffers 96 32k;
            fastcgi_buffer_size 32k;
            fastcgi_max_temp_file_size 0;
            fastcgi_keep_conn on;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param SCRIPT_NAME $fastcgi_script_name;
        }
    }
"""

        http_start_index = rPrevData.find("http {")
        if http_start_index != -1:
            http_end_index = rPrevData.rfind("}", http_start_index)
            rData = rPrevData[:http_end_index] + new_server_block + "\n}" + rPrevData[http_end_index+1:]

            with open(rPath, "w") as rFile:
                rFile.write(rData)

if __name__ == "__main__":
    try: rVersion = os.popen('lsb_release -sr').read().strip()
    except: rVersion = None
    if not rVersion in rVersions:
        printc("It can only be installed on Ubuntu 24.04 / 26.04")
        sys.exit(1)
    printc("X-UI installer Ubuntu %s - Masoud-Gb" % rVersion, col.GREEN, 1)
    print(" ")
    
    input_prompt = "  Installation Type [%sMAIN%s, %sLB%s, %sUPDATE%s]: " % (col.BRIGHT_GREEN, col.ENDC, col.BRIGHT_GREEN, col.ENDC, col.BRIGHT_GREEN, col.ENDC)
    rType = input(input_prompt)
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
                printc("Installation completed!", col.GREEN, 1)
                if rType.upper() == "MAIN":
                    printc("MySQL pass: %s" % rPassword, col.BRIGHT_YELLOW)
                    printc("Admin UI: http://%s:25500" % getIP(), col.BRIGHT_YELLOW)
                    printc("Login: admin/admin", col.BRIGHT_YELLOW)
                    rFile = open("/root/credentials.txt", "w")
                    rFile.write("MySQL password: %s\n" % rPassword)
                    rFile.write("Admin UI Wan IP: http://%s:25500\n" % getIP())
                    rFile.write("Admin UI default login is admin/admin\n")
                    rFile.close()
            else: printc("Installation cancelled", col.BRIGHT_RED)
        else: printc("Invalid entries", col.BRIGHT_RED)
    elif rType.upper() == "UPDATE":
        if os.path.exists("/home/xtreamcodes/iptv_xtream_codes/wwwdir/api.php"):
            printc("Update To Xtream-UI CKMOD 41 ? Y/N?", col.BRIGHT_YELLOW)
            if input("  ").upper() == "Y":
                if not update(rType.upper()): sys.exit(1)
                printc("Installation completed!", col.GREEN, 1)
                start()
            else: printc("Install Xtream Codes Main first!", col.BRIGHT_RED)
    else: printc("Invalid installation type", col.BRIGHT_RED)
