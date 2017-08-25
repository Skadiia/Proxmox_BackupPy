#!/usr/bin/env python
# -.- coding: utf-8 -.-

import sys
from Proxmox_BackupPy import Parser, CephCmd, Logger

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'


def main():
    """ Proxmox_BackupPy main function """
    # Create Backup_object instance
    try:
        action, vmid, dayfull, keep, backupdir, mail, compress = Parser.parsing()
        Backup_object = CephCmd.Backup_RBD(action=action, vmid=vmid, dayfull=dayfull, keep=keep, backupdir=backupdir, mail=mail, compress=compress)
    except Exception:
        print(RED + '[-] An unknow error occurs' + END)
        raise SystemExit
    except KeyboardInterrupt:
        print(RED + '[-] User keyboard interrupt the program' + END)
        raise SystemExit

    # Perform create cron file action
    if action.strip().lower() == 'create':
        try:
            Backup_object.create_cron()
            print(GREEN + '[+] The planified backup task has been created' + END)
        except Exception:
            print(RED + '[-] An unknow error occurs')
            raise SystemExit
        except KeyboardInterrupt:
            print(RED + '[-] User keyboard interrupt the program' + END)
            raise SystemExit

    # Perform remove cron file action
    elif action.strip().lower() == 'remove':
        try:
            Backup_object.remove_cron()
            print(GREEN + '[+] The planified backup task has been removed' + END)
        except Exception:
            print(RED + '[-] An unknow error occurs' + END)
            raise SystemExit
        except KeyboardInterrupt:
            print(RED + '[-] User keyboard interrupt the program' + END)
            raise SystemExit

    # Perform the listing of all the backup files for a vm
    elif action.strip().lower() == 'list':
        try:
            Backup_object.listing()
        except Exception:
            print(RED + '[-] An unknow error occurs' + END)
            raise SystemExit
        except KeyboardInterrupt:
            print(RED + '[-] User keyboard interrupt the program' + END)
            raise SystemExit

    # DEBUG

    elif action.strip().lower() == 'backup':
        Backup_object.backup()

    elif action.strip().lower() == 'restore':
        Backup_object.restore()

    else:
        print(RED + '[-] Invalid user input for the action to perform' + END)
        raise SystemExit

if __name__ == '__main__':
    main()
