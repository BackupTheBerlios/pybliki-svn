from os.path import join
from docutils.core import publish_parts
import time
import locale

tr = lambda s: s.replace('&', '&amp;').replace('<','&lt;').replace('>','&gt;')

def generateRSS(root, cfg, entries):
    text = ''
    text += '<?xml version="1.0" encoding="utf-8"?>'
    text += '<rss version="2.0">'
    text += '<channel>'
    text += '<title>%s</title>' % cfg.get('blog', 'name')[1]
    text += '<link>http://%s</link>' % cfg.get('blog', 'webroot')[1]
    text += '<description> %s at http://%s</description>' % \
            (cfg.get('blog', 'name')[1], cfg.get('blog', 'webroot')[1])

    for entry in entries[:10]:
        if entry['name'] != 'index' and entry['log']['msg'] == 'publish':
            text += '<item>'
            text += '<title> %s </title>' % entry['title']
            if entry.has_key('dir'):
                text += '<link>http://%s.html'\
                        '</link>' % join(cfg.get('blog', 'webroot')[1],
                                         entry['dir'], entry['name'])
            else:
                text += '<link>http://%s.html'\
                        '</link>' % join(cfg.get('blog', 'webroot')[1],
                                         root, entry['name'])

            parts = publish_parts(entry['text'].split('\n\n')[1],
                                  writer_name='html')

            text += '<description>%s</description>' % \
                    tr(parts['html_body'].encode('utf-8'))

            locale.setlocale(locale.LC_ALL, 'C')
            text += '<pubDate>%s</pubDate>' % \
                    time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                  entry['log']['date'])
            text += '</item>'

    text += '</channel>'
    text += '</rss>'
    return text
