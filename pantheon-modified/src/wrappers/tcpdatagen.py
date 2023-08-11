#!/usr/bin/env python

from os import path
from subprocess import check_call

import arg_parser
import context
from helpers import kernel_ctl
import sys

def setup_datagen():
    sys.stderr.write("*******************\n******************* Before using TCPDataGen, make sure you have installed the proper Kernel patches (>=4.19.112-0062) *******************\n*******************\n")

def main():
    args = arg_parser.sender_first()

    cc_repo = path.join(context.third_party_dir, 'tcpdatagen')
    bin_dir = path.join(cc_repo, 'bin')
    send_src = path.join(cc_repo, 'dataset.sh')
    recv_src = path.join(cc_repo, 'client.sh')

    if args.option == 'setup':
        sh_cmd = './build.sh'
        check_call(sh_cmd, shell=True, cwd=cc_repo)
        setup_datagen()
        return

    if args.option == 'setup_after_reboot':
        setup_datagen()
        return

    if args.option == 'sender':
        cmd = [send_src, args.port, ' 50',' 150',' 10',' 2', args.tcpgen_cc, bin_dir , args.comment,args.num_flows,args.bw,args.basetime_fld,args.bw2,args.trace_period]
        check_call(cmd)
        return

    if args.option == 'receiver':
        cmd = [recv_src, args.ip, ' 1 ' , args.port, bin_dir]
        check_call(cmd)
        return

if __name__ == '__main__':
    main()
