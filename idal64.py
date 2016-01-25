#!/usr/bin/env python

import pexpect
import sys

def main(args):
    """
    Wrap the "idal" binary with pexpect, in order to fake a terminal for IDA so we could run IDA as a regular
    command-line command without GUI.
    :param args:
    :return:
    """
    pexpect.run('idal64 ' + args, timeout=600)

if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))