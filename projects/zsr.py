#!/usr/bin/python
from mechanize import Browser
import re, sys

# ZSR_START_PAGE = 'http://zsr.wfu.edu'
ZSR_START_PAGE = 'http://zsr.wfu.edu/cgi-bin/Pwebrecon.cgi?DB=local&PAGE=hbSearch'
class ZSRResult(object):
    def __init__(self, call=None, status=None):
        self.call=call
        self.status=status
    def get_call(self): return self.call
    def get_status(self): return self.status

class ZSRSearchException(Exception): pass

def html_to_result(html):
    call = None
    status = ''
    
    state = 'LOOKING'
    for line in html.split('\n'):
        if state == 'LOOKING':
            if re.search( 'Call Number:', line ):
                state = 'CALL'
            elif re.search( 'Status:', line ):
                state = 'STATUS'
        elif state == 'CALL':
            m = re.search('<a href=".*?">\s*(.*?)\s*</a>', line, re.I)
            if m:
                call = m.group(1)
                state='LOOKING'
        elif state == 'STATUS':
            if re.search('</td>', line, re.I):
                state='LOOKING'
            line = re.sub('<.*?>', '', line )
            status += line + ' '
    status = ' '.join( status.split() )
    if call and status:
        return ZSRResult(call=call, status=status)
    else:
        raise ZSRSearchException("Could not find call number and status")


def title_search( title ):
    b = Browser()
    b.set_handle_robots(False)
    b.set_handle_refresh(True)
#    b.set_debug_http(True)
    b.open( ZSR_START_PAGE )
    assert b.viewing_html()
    b.select_form(name='querybox')
    b['Search_Code']=['TALL']
    b['Search_Arg']=title
    response = b.submit()
    if b.title() == 'Titles':
        l=b.links( url_regex=re.compile('\?v1=1&') )
        response = b.follow_link( l[0] )
    html = response.read()
    result = html_to_result( html )
    response.close()
    return result

if __name__ == '__main__':
    for line in sys.stdin.xreadlines():
        line=line.rstrip()
        print line
        title=re.sub('\s*[,(:].*','',line)
        try:
            r = title_search( title )
            print "%s: %s" % ( title, r.get_call() )
            print "Status: %s" % ( r.get_status() )
        except ZSRSearchException, e:
            print "Could not find a record for %s" % title
        print
        sys.stdout.flush()
