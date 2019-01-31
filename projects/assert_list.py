#!/usr/local/bin/python

import os, sys

SUFFIXES=('', '-admin', '-bounces', '-confirm', '-join', '-leave',
          '-owner', '-request', '-subscribe', '-unsubscribe')
DEFAULT_PASS='FANTASTICALLY SECURE PASSWORD THAT QMAILADMIN LIKES GOES HERE'
MAILMAN_HOME=os.path.join( os.environ["HOME"], 'mailman' )

def write_file_format( filename, format, dict):
  fd = open(filename, 'w')
  fd.write( format % dict )
  fd.close()

def write_list_getmails( list_name, password=DEFAULT_PASS ):
  for suffix in SUFFIXES:
    account = list_name + suffix
    filename = os.path.join( os.environ["HOME"],
                             '.getmail', 'getmailrc.'+account )
    write_file_format( filename,
"""
[retriever]
use_apop = True
type = MultidropPOP3Retriever
server = mail.zettai.net
username = %(account)s@uufws.net
password = %(password)s
envelope_recipient = delivered-to:1

[destination]
type = MDA_qmaillocal

[options]
verbose = 2
received = false
message_log = ~/.getmail/log
""",
{ 'list_name': list_name,
  'password' : password,
  'account'  : account,
})

def suffix_to_command( suffix ):
  if suffix == '':
    return 'post'
  else:
    return suffix[1:]

def write_list_qmails( list_name ):
  mailman_cmd = os.path.join( MAILMAN_HOME, 'mail', 'mailman' )
  for suffix in SUFFIXES:
    account=list_name + suffix
    filename=os.path.join( os.environ["HOME"], '.qmail-'+account)

    write_file_format( filename,
"|%(mailman_cmd)s %(command)s %(list_name)s",
{ 'mailman_cmd' : mailman_cmd,
  'list_name'  : list_name,
  'command'    : suffix_to_command( suffix )
})
    os.chmod( filename, 0600 )


if __name__ == '__main__':
  for list_name in sys.argv[1:]:
    write_list_getmails( list_name )
    write_list_qmails( list_name )
