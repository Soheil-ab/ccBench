#!/usr/bin/env python

from os import path
from subprocess import check_call

import arg_parser
import context
from helpers import kernel_ctl

def setup_orca():
    # load tcp_ kernel module (only available since Linux Kernel 4.9)
    kernel_ctl.load_kernel_module('tcp_cubic')
    # add cubic to kernel-allowed congestion control list
    kernel_ctl.enable_congestion_control('cubic')


def main():
    args = arg_parser.sender_first()

    cc_repo = path.join(context.third_party_dir, 'orca')
    ddpg_src = path.join(cc_repo, 'rl-module')
    send_src = path.join(cc_repo, 'server.sh')
    recv_src = path.join(cc_repo, 'client.sh')

    if args.option == 'setup':
        setup_orca()
        sh_cmd = './build.sh'
        check_call(sh_cmd, shell=True, cwd=cc_repo)
        return

    if args.option == 'setup_after_reboot':
        setup_orca()
        return

    if args.option == 'sender':
        cmd = [send_src, args.port, ' 50',' 150',' 20',args.orcalearn, 'cubic ', ddpg_src,args.actor_id]
        check_call(cmd)
        return

    if args.option == 'receiver':
        cmd = [recv_src, args.ip, ' 1 ' ,args.port, ddpg_src]
        check_call(cmd)
        return

if __name__ == '__main__':
    main()
