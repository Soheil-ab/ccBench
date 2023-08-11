#!/usr/bin/env python

from subprocess import check_call

import arg_parser
import context
from helpers import kernel_ctl


def setup_westwood():
    # load tcp_ kernel module (only available since Linux Kernel 4.9)
    kernel_ctl.load_kernel_module('tcp_westwood')

    # add westwood to kernel-allowed congestion control list
    kernel_ctl.enable_congestion_control('westwood')


def main():
    args = arg_parser.receiver_first()

    if args.option == 'deps':
        print 'iperf'
        return

    if args.option == 'setup_after_reboot':
        setup_westwood()
        return

    if args.option == 'receiver':
        cmd = ['iperf3', '-s', '-p', args.port]
        check_call(cmd)
        return

    if args.option == 'sender':
        cmd = ['iperf3', '-C', 'westwood', '-c', args.ip, '-p', args.port,
               '-t', '7500']
        check_call(cmd)
        return


if __name__ == '__main__':
    main()
