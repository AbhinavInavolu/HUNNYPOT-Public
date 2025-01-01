from utils.constants import HOSTNAME, USERNAME, PASSWORD, PORT

from scp import SCPClient
import paramiko


def connect_ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD, port=PORT)

    return ssh

def zip_backup(ssh):
    _, stdout, _ = ssh.exec_command("zip -r mitm_logs.zip mitm_logs")
    stdout.channel.recv_exit_status()

    _, stdout, _ = ssh.exec_command("zip all_scripts.zip *.sh")
    stdout.channel.recv_exit_status()

    _, stdout, _ = ssh.exec_command("zip -r honey.zip honey")
    stdout.channel.recv_exit_status()

    _, stdout, _ = ssh.exec_command("zip -r health_logs.zip hunnypot_logs")
    stdout.channel.recv_exit_status()

def download_zips(ssh):
    with SCPClient(ssh.get_transport()) as scp:
        scp.get("mitm_logs.zip", "backup/mitm_logs.zip")
        scp.get("all_scripts.zip", "backup/all_scripts.zip")
        scp.get("honey.zip", "backup/honey.zip")
        scp.get("health_logs.zip", "backup/health_logs.zip")

def remove_remote_zips(ssh):
    ssh.exec_command("rm -f mitm_logs.zip")
    ssh.exec_command("rm -f all_scripts.zip")
    ssh.exec_command("rm -f honey.zip")
    ssh.exec_command("rm -f health_logs.zip")
