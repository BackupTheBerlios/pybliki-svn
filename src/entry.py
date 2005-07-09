import os
from xml.dom.minidom import parseString

def getEntryInformation(filename):
    svn_log = 'svn log --xml %s' % filename
    pipe = os.popen(svn_log)
    xml = pipe.read()
    pipe.close()

    dom = parseString(xml)
    data = []

    for logentry in dom.getElementsByTagName('logentry'):
        data.append({})

        author = logentry.getElementsByTagName('author')[0]
        data[-1]['author'] = author.firstChild.nodeValue

        msg = logentry.getElementsByTagName('msg')[0]
        data[-1]['msg'] = msg.firstChild.nodeValue

        date = logentry.getElementsByTagName('date')[0]
        data[-1]['date'] = strptime(date.firstChild.nodeValue[:19],
                                    '%Y-%m-%dT%H:%M:%S')}
    return data


