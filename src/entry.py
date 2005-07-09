import os
from xml.dom.minidom import parseString
from time import strptime

def getEntryInformation(filename):
    svn_log = 'svn log --xml %s' % filename
    pipe = os.popen(svn_log)
    xml = pipe.read()
    pipe.close()

    log = []

    dom = parseString(xml)
    for logentry in dom.getElementsByTagName('logentry'):
        log.append({})

        author = logentry.getElementsByTagName('author')[0]
        log[-1]['author'] = author.firstChild.nodeValue.encode('utf-8')

        msg = logentry.getElementsByTagName('msg')[0]
        log[-1]['msg'] = msg.firstChild.nodeValue.encode('utf-8')

        date = logentry.getElementsByTagName('date')[0]
        log[-1]['date'] = strptime(date.firstChild.nodeValue[:19],
                                    '%Y-%m-%dT%H:%M:%S')

    data = {}
    data['log'] = log

    f = file(filename)
    text = f.read()
    f.close()

    data['text'] = text
    data['title'] = text.split('\n', 1)[0]
    data['name'] = os.path.splitext(os.path.basename(filename))[0]

    return data


