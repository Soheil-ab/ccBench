#!/usr/bin/env python

from subprocess import Popen, check_call, check_output

import arg_parser
import context
from helpers import kernel_ctl


def setup_vegas():
    # load tcp_vegas kernel module
    kernel_ctl.load_kernel_module('tcp_htcp')

    # add vegas to kernel-allowed congestion control list
    kernel_ctl.enable_congestion_control('htcp')


def main():
    args = arg_parser.receiver_first()

    if args.option == 'deps':
        print 'iperf'
        return

    if args.option == 'setup_after_reboot':
        setup_vegas()
        return

    if args.option == 'receiver':
        cmd = ['iperf3', '-s', '-p', args.port]
        check_call(cmd)
        return

    if args.option == 'sender':
        cmd = ['iperf3', '-C', 'htcp', '-c', args.ip, '-p', args.port,
               '-t', '7500']
        check_call(cmd)
        return


if __name__ == '__main__':
    main()
