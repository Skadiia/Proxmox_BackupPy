#!/usr/bin/env python2.7
# -.- coding: utf-8 -.-

import argparse
import sys

def parsing():
    """ Fonction that parse command line arguments """

    parser = argparse.ArgumentParser(prog='Proxmox_BackupPy',
                                    description='Simple Python program for backup ProxmoxVE/CephRBD VMs',
                                    epilog='Made with <3')

    parser.add_argument('action',
                        help='Action to select (backup, restore, create, remove, list)')
    parser.add_argument('--vmid',
                        help='Vmids you want to backup separated by \",\" (example: --vmid 100,101)',
                        type=int)
    parser.add_argument('--dayfull',
                        help='Specify the day of the week for full backup between 1 and 7, where 1 is Monday',
                        type=int)
    parser.add_argument('--keep',
                        help='Number of backups to keep',
                        type=int)
    parser.add_argument('--pool',
                        help='Number of backups to keep',
                        type=str)
    parser.add_argument('--backupdir',
                        help='Destination directory for VMs backup',
                        type=str)
    parser.add_argument('--mail',
                        help='define an email address to send the backup or restore report',
                        type=str)
    parser.add_argument('--compress',
                        help='Specify if the backup should be compress. Need to be on/off',
                        type=bool)
    parser.add_argument('-v', '--version',
                        help='Display the program version',
                        action='version',
                        version='Made by @Init1, %(prog)s version is 0.1. Contact at (skadia@protonmail.com)')

    args = parser.parse_args()


    return args.action, args.vmid, args.dayfull, args.keep, args.backupdir, args.mail, args.compress
