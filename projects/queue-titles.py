#!/usr/bin/python
import feedparser
MY_RSS_QUEUE = 'http://whatever'
JOUR_RSS_QUEUE = 'http://whatever'
# also edit __main__ below

def feed_titles( feed ):
    return map( lambda x: x.title, feed.entries )

def strip_title_numbers( titles):
    return map( lambda x: x.split('- ')[1], titles )

def normalize_titles( titles):
    normals = []
    for t in titles:
        if len(t)>4 and t.lower().startswith('the '):
            t = t[4:] + ', The'
        elif len(t)>2 and t.lower().startswith('a '):
            t = t[2:] + ', A'
        elif len(t)>3 and t.lower().startswith('an '):
            t = t[3:] + ', An'
        normals.append(t)
    return normals

def case_insensitive_sort( strings):
    """
    Python Cookbook, 2d Ed, p. 196
    note: this looks a lot like a schwartzian transform!
    """
    auxiliary_list = [(x.lower(), x) for x in strings]
    auxiliary_list.sort()
    return [x[1] for x in auxiliary_list]

def print_list( strings):
    for s in strings:
        print s

if __name__ == '__main__':
    titles = []
    for (url,i) in ( (MY_RSS_QUEUE, 'Mine'),
                     (JOUR_RSS_QUEUE, 'Yours'),
                     ):
        feed = feedparser.parse( url )
        url_titles = feed_titles( feed )
        url_titles = strip_title_numbers( url_titles )
        url_titles = normalize_titles( url_titles )
        url_titles = map( lambda x: x+' (%s)' % i, url_titles )
        titles.extend( url_titles )
    titles = case_insensitive_sort( titles)
    print_list( titles )
