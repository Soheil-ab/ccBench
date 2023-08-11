#!/usr/bin/env python

from os import path
from subprocess import check_call

import arg_parser
import context


def main():
    args = arg_parser.sender_first()

    cc_repo = path.join(context.third_party_dir, 'c2tcp')
    send_src = path.join(cc_repo, 'server.sh')
    recv_src = path.join(cc_repo, 'client')

    if args.option == 'setup':
         sh_cmd = './build.sh'
         check_call(sh_cmd, shell=True, cwd=cc_repo)
         return

    if args.option == 'sender':
        #: port Target(ms) init_target_ratio(150) report_period(ms)
        cmd = [send_src, args.port, '50',' 500', cc_repo]
        check_call(cmd)
        return

    if args.option == 'receiver':
        cmd = [recv_src, args.ip, ' 1 ' ,args.port]
        check_call(cmd)
        return


if __name__ == '__main__':
    main()
