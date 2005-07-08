from os.path import join
from time import strftime, gmtime
import locale

def generateRSS(entries, root, name, webroot):

    locale.setlocale(locale.LC_ALL, 'C')

    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<rss version="2.0">'
    print '<channel>'
    print '<title>%s</title>' % name
    print '<link>http://%s</link>' % webroot
    print '<description> %s at http://%s</description>' % (name, webroot)

    for idx, entry in enumerate(entries[:10]):
        print '<item>'
        print '<title> %s </title>' % entry["title"]
        print '<link> http://%s.html'\
              '</link>' % join(webroot, root, entry["name"])
        print '<description> %s </description>' % entry["msg"]
        print '<pubDate> %s </pubDate>' % \
                strftime("%a, %d %b %Y %H:%M:%S GMT", entry["date"])
        print '</item>'

    print '</channel>'
    print '</rss>'
