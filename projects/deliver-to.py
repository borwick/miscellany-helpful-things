#!/usr/local/bin/python
"""
This program looks at sys.argv, messes with it a bit, and then execs (the original)
sys.argv[1] with the munged options.  Here's basically what it was written to do:

  /path/to/deliver-to --delimiter=- --replace=1 --mailman-magic=1 \
    /path/to/mailman example.com-hello-join
   -becomes-
  /path/to/mailman join hello

while correctly doing
  /path/to/mailman post hello-there

for a list.  Basically, you can use a multidrop POP3 account with getmail and a
bunch of aliases, using the deliver-to: fields.
"""


import os
import sys
import copy
from optparse import OptionParser

MM_MAGIC_ENDINGS = [ 'admin', 'bounces', 'confirm', 'join',
                     'leave', 'owner', 'request', 'subscribe',
                     'unsubscribe' ]

def munge_args( args ):
  parser = OptionParser()

  parser.add_option("-d", "--delimiter",
                    dest="delimiter",
                    help="Delimiter character to use" )

  parser.add_option("-r", "--replace",
                    dest="replace",
                    type="int",
                    help="Argument to change" )

  parser.add_option("-m", "--mailman-magic",
                    dest="mm_field",
                    type="int",
                   help="Argument for which to perform mailman magic")

  (options, args) = parser.parse_args( args=args )

  # remove myself from the stack
  args = args[1:]
  delimiter = getattr( options, 'delimiter' )
  replace = getattr( options, 'replace' )
  mm_field = getattr( options, 'mm_field' )

  if delimiter and replace:
    orig_arg = args[ replace ]
    # Python throws an exception if delimiter not found:
    delimiter_pos = orig_arg.index( delimiter )
    mogrified_arg = orig_arg[ delimiter_pos +1: ]
    args[ replace ] = mogrified_arg

  if mm_field:
    mm_arg = args[ mm_field ]
    mm_action = 'post'
    mm_list = mm_arg
  
    if mm_arg.rfind('-') >= 0:
      mm_last_dash = mm_arg[ mm_arg.rindex( '-' ) +1 : ].lower()
      mm_pre_dash = mm_arg[ 0 : mm_arg.rindex( '-' ) ]
      print "mm_last_dash=%s" % mm_last_dash
      if mm_last_dash in MM_MAGIC_ENDINGS:
        mm_action = mm_last_dash
        mm_list = mm_pre_dash

    args[ mm_field ] = mm_list
    args.insert( mm_field , mm_action )

  return args

if __name__ == '__main__':
  args = munge_args( args=sys.argv )
  print "ARGS=%s" % args
  os.execvp( args[0], args ) 
  print "Could not exec mail-debug"
  sys.exit( 1 )


