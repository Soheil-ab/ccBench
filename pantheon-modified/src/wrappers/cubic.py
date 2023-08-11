#!/usr/bin/env python

from subprocess import check_call

import arg_parser


def main():
    args = arg_parser.receiver_first()

    if args.option == 'deps':
        print 'iperf'
        return

    if args.option == 'receiver':
        cmd = ['iperf3', '-s', '-p', args.port]
        check_call(cmd)
        return

    if args.option == 'sender':
        cmd = ['iperf3', '-C', 'cubic', '-c', args.ip, '-p', args.port,
               '-t', '7500']
        check_call(cmd)
        return


if __name__ == '__main__':
    main()
