import argparse


def parse_wrapper_args(run_first):
    if run_first != 'receiver' and run_first != 'sender':
        sys.exit('Specify "receiver" or "sender" to run first')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='option')

    subparsers.add_parser(
        'deps', help='print a space-separated list of build dependencies')
    subparsers.add_parser(
        'run_first', help='print which side (sender or receiver) runs first')
    subparsers.add_parser(
        'setup', help='set up the scheme (required to be run at the first '
        'time; must make persistent changes across reboots)')
    subparsers.add_parser(
        'setup_after_reboot', help='set up the scheme (required to be run '
        'every time after reboot)')

    receiver_parser = subparsers.add_parser('receiver', help='run receiver')
    sender_parser = subparsers.add_parser('sender', help='run sender')

    if run_first == 'receiver':
        receiver_parser.add_argument('port', help='port to listen on')
        sender_parser.add_argument(
            'ip', metavar='IP', help='IP address of receiver')
        sender_parser.add_argument('port', help='port of receiver')
        sender_parser.add_argument('srate', help='requested sending rate',default=24)
    else:
        sender_parser.add_argument('port', help='port to listen on')
        sender_parser.add_argument('actor_id', help='Orca Actor Id (if existed!)')
        sender_parser.add_argument('orcakey', help='Orca 1st key')
        sender_parser.add_argument('orcakey_rl', help='Orca 2nd key')
        sender_parser.add_argument('orcalearn', help='Orca Learning')
        sender_parser.add_argument('comment', help='Generating env comment!')
        sender_parser.add_argument('tcpgen_cc', help='TCP scheme for generating dataset!')
        sender_parser.add_argument('num_flows', help='Give me the number of competing flows!')
        sender_parser.add_argument('bw', help='Give me the BW of the link!')
        sender_parser.add_argument('basetime_fld', help='basetimestamp\'s foder')
        sender_parser.add_argument('bw2', help='Second BW on the step-function traces')
        sender_parser.add_argument('trace_period', help='Period of change of the BW on trace files')
        #sender_parser.add_argument('duration', help='Sage & Tcp DatasetGen: overall time for sending traffic')

        receiver_parser.add_argument(
            'ip', metavar='IP', help='IP address of sender')
        receiver_parser.add_argument('port', help='port of sender')

    args = parser.parse_args()

    if args.option == 'run_first':
        print run_first

    return args


def receiver_first():
    return parse_wrapper_args('receiver')


def sender_first():
    return parse_wrapper_args('sender')
