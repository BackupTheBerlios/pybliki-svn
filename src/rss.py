def generateRSS(entries):
    print '<?xml version="1.0" encoding="utf-8"?>'
    print '<rss version="2.0">'
    print '<channel>'
    print '<title>dado1945</title>'
    print '<link>http://uosis.mif.vu.lt/~dado1945/cgi-bin/index.cgi</link>'
    print '<description> dado1945 at uosis.mif.vu.lt</description>'

    for idx, entry in enumerate(entries[:10]):
        print '<item>'
        print '<title> %s </title>' % entry["title"]
        print '<link> http://uosis.mif.vu.lt/~dado1945/cgi-bin/entry.cgi?id=%d '\
              '</link>' % entry["id"]
        print '<description> %s </description>' % entry["msg"]
        print '<pubDate> %s </pubDate>' % \
                strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(entry["date"]))
        print '</item>'

    print '</channel>'
    print '</rss>'
