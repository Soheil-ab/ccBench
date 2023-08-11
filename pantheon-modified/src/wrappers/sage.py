#!/usr/bin/env python

from os import path
from subprocess import check_call

import arg_parser
import context
from helpers import kernel_ctl
import sys
def setup_sage():
    sys.stderr.write("*******************\n******************* Before using Sage, make sure you have installed the proper Kernel patches (>4.19.112-0062) *******************\n*******************\n")

def main():
    args = arg_parser.sender_first()

    cc_repo1 = path.join(context.third_party_dir, 'sage')
    cc_repo = path.join(cc_repo1,'sage_rl')
    rl_fld = path.join(cc_repo, 'rl_module')
    send_src = path.join(cc_repo1, 'sage.sh')
    recv_src = path.join(cc_repo1, 'client.sh')

    if args.option == 'setup':
        sh_cmd = './build.sh'
        check_call(sh_cmd, shell=True, cwd=cc_repo1)
        setup_sage()
        return

    if args.option == 'setup_after_reboot':
        setup_sage()
        return

    if args.option == 'sender':
        cmd = [send_src, args.port, ' 50',' 150',' 10','0', "pure", rl_fld , args.comment,args.num_flows,args.bw,args.basetime_fld,args.bw2,args.trace_period]
        sys.stderr.write("...  ...  ... %s\n" % (cmd))

        check_call(cmd)
        return

    if args.option == 'receiver':
        cmd = [recv_src, args.ip, ' 1 ' ,args.port, rl_fld]
        check_call(cmd)
        return

if __name__ == '__main__':
    main()
