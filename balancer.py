#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

rDownloadURL = "https://bitbucket.org/masoudgb/xtream-ui/raw/master/sub_xui_masoudgb.zip"
rPackages = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc"]

def is_installed(package_name):
    result = subprocess.run(f"dpkg -s {package_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def install_libzip5():
    if not is_installed("libzip5"):
        print("Installing libzip5")
        try:
            subprocess.run("wget http://archive.ubuntu.com/ubuntu/pool/universe/libz/libzip/libzip5_1.5.1-0ubuntu1_amd64.deb -q", shell=True, check=True)
            subprocess.run("sudo dpkg -i libzip5_1.5.1-0ubuntu1_amd64.deb -q", shell=True, check=True)
            subprocess.run("rm libzip5_1.5.1-0ubuntu1_amd64.deb", shell=True, check=True)  # Clean up
        except subprocess.CalledProcessError as e:
            print(f"Error installing libzip5: {e}")

if __name__ == "__main__":
    install_libzip5()
def getVersion():
    try:
        return subprocess.check_output("lsb_release -d".split()).split(b":")[-1].strip().decode()
    except subprocess.CalledProcessError as e:
        print(f"Error getting version: {e}")
        return ""

def prepare():
    global rPackages
    lock_files = ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]
    for rFile in lock_files:
        try:
            os.remove(rFile)
        except OSError as e:
            print(f"Error removing lock file {rFile}: {e}")
    subprocess.run("apt-get update -q", shell=True, check=True)
    for rPackage in rPackages:
        subprocess.run(f"apt-get install {rPackage} -y -q", shell=True, check=True)
    subprocess.run("apt-get install -y -q", shell=True, check=True)  # Clean up above
    subprocess.run("adduser --system --shell /bin/false --group --disabled-login xtreamcodes -q", shell=True, check=True)
    if not os.path.exists("/home/xtreamcodes"):
        os.mkdir("/home/xtreamcodes")
    return True

def install():
    global rInstall, rDownloadURL
    rURL = rDownloadURL

    zip_file_path = "/tmp/xtreamcodes.zip"
    subprocess.run(f'wget -q -O "{zip_file_path}" "{rURL}"', shell=True, check=True)

    if os.path.exists(zip_file_path):
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall("/home/xtreamcodes/")
        except zipfile.BadZipFile:
            print(f"Error: {zip_file_path} is not a valid zip file!")
            return False

        try:
            os.remove(zip_file_path)
        except OSError as e:
            print(f"Error removing downloaded file: {e}")
        return True

    return False


def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    try:
        os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except OSError:
        pass
    with open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb') as rf:
        lestring = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(
            '{"host":"%s","db_user":"%s","db_pass":"%s","db_name":"%s","server_id":"%d", "db_port":"%d"}' %
            (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1')))
        rf.write(base64.b64encode(bytes(lestring, 'ascii')))

def configure():
    if "/home/xtreamcodes/iptv_xtream_codes/" not in open("/etc/fstab").read():
        with open("/etc/fstab", "a") as rFile:
            rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
    if "xtreamcodes" not in open("/etc/sudoers").read():
        subprocess.run('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables" >> /etc/sudoers', shell=True, check=True)
    if not os.path.exists("/etc/init.d/xtreamcodes"):
        with open("/etc/init.d/xtreamcodes", "w") as rFile:
            rFile.write("#! /bin/bash\n/home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        subprocess.run("chmod +x /etc/init.d/xtreamcodes -q", shell=True, check=True)
    try:
        os.remove("/usr/bin/ffmpeg")
    except OSError:
        pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"):
        os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    subprocess.run("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/", shell=True, check=True)
    subprocess.run("chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb -q", shell=True, check=True)
    subprocess.run("wget -q https://bitbucket.org/masoudgb/xtream-ui/raw/master/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb", shell=True, check=True)
    subprocess.run("wget -q https://bitbucket.org/masoudgb/xtream-ui/raw/master/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php", shell=True, check=True)
    subprocess.run("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes -q", shell=True, check=True)
    subprocess.run("chmod -R 0777 /home/xtreamcodes -q", shell=True, check=True)
    subprocess.run("chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb -q", shell=True, check=True)
    subprocess.run("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh", shell=True, check=True)
    subprocess.run("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh -q", shell=True, check=True)
    subprocess.run("mount -a", shell=True, check=True)
    subprocess.run("chmod 0700 /home/xtreamcodes/iptv_xtream_codes/config -q", shell=True, check=True)
    subprocess.run("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php", shell=True, check=True)
    if "api.xtream-codes.com" not in open("/etc/hosts").read():
        subprocess.run('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts', shell=True, check=True)
    if "downloads.xtream-codes.com" not in open("/etc/hosts").read():
        subprocess.run('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts', shell=True, check=True)
    if "xtream-codes.com" not in open("/etc/hosts").read():
        subprocess.run('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts', shell=True, check=True)
    if "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" not in open("/etc/crontab").read():
        subprocess.run('echo "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" >> /etc/crontab', shell=True, check=True)

def start():
    subprocess.run("/home/xtreamcodes/iptv_xtream_codes/start_services.sh -q", shell=True, check=True)

def setPorts(rPorts):
    subprocess.run(f"sed -i 's/listen 25461;/listen {rPorts[0]};/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf", shell=True, check=True)
    subprocess.run(f"sed -i 's/:25461/:{rPorts[0]}/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf", shell=True, check=True)
    subprocess.run(f"sed -i 's/listen 25463 ssl;/listen {rPorts[1]} ssl;/g' /home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf", shell=True, check=True)
    subprocess.run(f"sed -i 's/listen 25462;/listen {rPorts[2]};/g' /home/xtreamcodes/iptv_xtream_codes/nginx_rtmp/conf/nginx.conf", shell=True, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: script.py <host> <port> <username> <password> <database> <server_id> [port1 port2 port3]")
        sys.exit(1)

    rHost = sys.argv[1]
    rPort = int(sys.argv[2])
    rUsername = sys.argv[3]
    rPassword = sys.argv[4]
    rDatabase = sys.argv[5]
    rServerID = int(sys.argv[6])

    try:
        rPorts = [int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])]
    except IndexError:
        rPorts = None

    if prepare():
        if not install():
            sys.exit(1)
        encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
        configure()
        if rPorts:
            setPorts(rPorts)
        start()
    else:
        sys.exit(1)
