#!/usr/bin/env python
# -.- coding: utf-8 -.-

import sys
import os
import re
import subprocess
from datetime import datetime, timedelta
from shutil import copyfile

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

class Backup_RBD(object):

    PVE_DIR="/etc/pve"
    PVE_NODES="$PVE_DIR/nodes"
    QEMU='qemu-server'
    QEMU_CONF="$PVE_NODES/*/$QEMU"
    TODAY=datetime.utcnow()
    YESTERDAY=datetime.utcnow - timedelta(1)

    def __init__(self, action=False, vmid=False, dayfull=False, keep=False, pool=False, backupdir=False, mail=False, compress='off'):
        self.action = action
        self.vmid = vmid
        self.dayfull = dayfull
        self.keep = keep
        self.pool = pool
        self.backupdir = backupdir
        self.mail = mail
        self.compress = compress

        # Connect Ceph rbd
        cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
        cluster.connect()
        self._ceph_ioctx = cluster.open_ioctx(pool)
        self._ceph.rbd = rbd.RBD()

    def _import_ceph_module(self):
        """ Function for importing rbd and rados module to interact with Ceph RBD cluster """
        try:
            import rbd
            import rados
        except ImportError:
            print(RED + '[-] Failed to import rbd/rados modules' + END)
            try:
                choice = raw_input(YELLOW + '[*] Would you like to autoinstall those modules ? [yY/nN] ' + END)
            except KeyboardInterrupt:
                print(RED + '[-] User keyboard interrupt the program' + END)
                raise SystemExit
            if choice.strip().lower()[0] == 'y':
                print(YELLOW + '[*] Trying to install rbd/rados modules...' + END),
                sys.stdout.flush()
                try:
                    import pip
                    pip.main(['install', '--upgrade', 'rbd'])
                    pip.main(['install', '--upgrade', 'rados'])
                    import rbd, rados
                    print(GREEN + '[+] Successfully import rbd/rados modules' + END)
                except Exception:
                    print(RED + '[-] Failed to import rbd/rados modules' + END)
                    raise SystemExit
            elif choice.strip().lower()[0] == 'n':
                print(RED + '[-] rbd/rados modules will not be autoinstall' + END)
                raise SystemExit
            else:
                print(RED + '[-] Invalid user input' + END)
                raise SystemExit

    def _get_snaps(self, disk):
        """ Function to get all snapshot from a disk image """
        self._import_ceph_module()
        try:
            disk_image = rbd.Image(self._ceph_ioctx, disk)
            snapshots = []
            for snapshot in disk_image.list_snaps():
                snapshots.append(snapshot)
        except Exception:
            print(RED + '[-] Failed to retrieve snapshots' + END)
            raise SystemExit

        return snapshots

    def _get_latest_snap(self, disk):
        """ Function to get the latest snapshot from a disk image """
        self._import_ceph_module()
        snapshots = self._get_snaps(disk)
        if len(snapshots) is 0:
            return None
        else:
            #return the maw snap id

    def _create_snap(self, disk, snapname):
        """ Function to create a daily snapshot from a disk image """
        self._import_ceph_module()
        try:
            disk_image = rbd.Image(self._ceph_ioctx, disk)
            disk_image.create_snap(snapname)

            return True
        except ImageExists:
            print(RED + '[-] This snapshot already exist' + END)
            raise SystemExit

    def _export_full(self):
        """ Function to make a full export backup """
        self._import_ceph_module()

    def _import_full(self):
        """ Function to make a full import restore """
        self._import_ceph_module()

    def _export_diff(self):
        """ Function to make a differential export backup """
        self._import_ceph_module()

    def _import_diff(self):
        """ Function to make a differential import restore """
        self._import_ceph_module()

    def _compress_backup(self):
        """ Function for compressing VM backup file if needed """
        pass

    def backup(self):
        """ Function for backup ProxmoxVE/CephRBD VMs """
        # Importing needed modules
        self._import_ceph_module()

        for vm in self.vmid.split(','):

            # Create backup dir if needed
            if not os.path.isdir(self.backupdir + vm):
                try:
                    os.makedirs(self.backupdir + vm)
                    print(GREEN + '[+] Backup directory for vm ' + vm + ' has been created.' + END)
                except OSError:
                    print(RED + '[-] The backup directory hasen\'t been created' + END)
                    raise SystemExit

            # Backup the configuration file of the vm
            try:
                copyfile(QEMU_CONF + vm + '.conf', self.backupdir + vm + '/' + vm + '.conf')
                print(GREEN + '[+] The configuration file of the vm ' + vm + ' has been backup' + END)
            except IOError:
                print(RED + '[-] The configuration backup of the vm ' + vm + 'has failed' + END)
                raise SystemExit

            # GET disk(s) name of the VMs
            try:
                list_vm_disk = []
                with open(QEMU_CONF + vm + '.conf', 'r') as vmconf:
                    for lines in vmconf:
                        m = re.search(r"(?P<disk>vm-[0-9].*-disk-[0-9])", lines)
                        if m is not None:
                            list_vm_disk.append(m.group('disk'))
            except IOError:
                print(RED + '[-] Impossible to read VM configuration file' + END)
                raise SystemExit

            for disk in list_vm_disk:

            # Create the daily vm snapshot
                snapshots = self._get_snaps(disk)
                for snap in snapshots:
                    if snap == TODAY.strftime('%Y-%m-%d'):
                        print(YELLOW + '[*] The daily snapshot for ' + disk + ' already exist' + END)
                    else:
                        try:
                            self._create_snap(disk, TODAY.strftime('%Y-%m-%d') + '-Full')
                            print(GREEN + '[+] The daily snapshot for the ' + disk + ' disk has been created' + END)
                        except Exception:
                            print(RED + '[-] Failed to create the daily snapshot for the ' + disk + ' disk' + END)

            # Check for Full or Diff export
            


    def restore(self):
        """ Function for restore ProxmoxVE/CephRBD VMs """
        pass

    def create_cron(self):
        """ Function for create a new cron backup task """
        if not os.path.isfile('/etc/cron.d/Proxmox_Backup'):
            try:
                task = '@daily root /usr/bin/Proxmox_BackupPy/Proxmox_Backup.py %s --vmid %s --dayfull %s --keep %s --backupdir %s --mail %s --compress %s'%(self.action,self.vmid,self.dayfull,self.keep,self.backupdir,self.mail,self.compress)

                with open('/etc/cron.d/Proxmox_Backup', 'a') as cronf:
                    cronf.write('''# Tâche de sauvegarde automatisée pour Cluster ProxmoxVE / Ceph RBD
# Fichier généré automatiquement - ne pas éditer
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

{}'''.format(task))
            except IOError:
                print(RED + '[-] Impossible to create the cron file for backup' + END)
                raise SystemExit
        else:
            print(YELLOW + '[+] The planifed backup task already exist' +END)
            raise SystemExit

    def remove_cron(self):
        """ Function for remove a cron backup task """
        if os.path.isfile('/etc/cron.d/Proxmox_Backup'):
            try:
                os.remove('/etc/cron.d/Proxmox_Backup')
                print(GREEN + '[+] The cron file has been deleted' + END)
            except OSError:
                print(RED + '[-] Permission denied to remove cron backup file' + END)
                raise SystemExit
        else:
            print(RED + '[-] The is no cron file to remove' + END)
            raise SystemExit

    def listing(self):
        """ Function for listing all the backups for a specified VM """
        if not os.path.isdir(str(self.backupdir)):
            print(RED + '[-] The specified backup directory doesn\'t exist.' + END)
            raise SystemExit
        else:
            for vm in self.vmid.split(','):
                if not os.path.isdir(str(self.backupdir) + '/' + str(vm)):
                    print(RED + '[-] No backup directory for the specified vm: {}'.format(vm) + END)
                    raise SystemExit
                else:
                    print(os.listdir(str(self.backupdir) + '/' + str(vm)))

    def send_mail(self):
        """ Function for sending a mail with the result of the backup proces """
        for mail in self.mail.split(','):
