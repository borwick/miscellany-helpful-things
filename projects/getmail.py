#!/usr/local/bin/python
import os, fnmatch

GETMAIL_HOME = os.path.join( os.environ['HOME'], '.getmail' ) 

def run_getmail( rcfile ) :
  os.system('/usr/local/bin/getmail -lqn --rcfile ' + rcfile )

def rcfiles( ):
  rcs = []  
  for file in os.listdir( GETMAIL_HOME ):
    if fnmatch.fnmatch(file, 'getmailrc.*'):
      rcs.append( file )
  return rcs

if __name__ == '__main__':
  for file in rcfiles():
    run_getmail( file )  
