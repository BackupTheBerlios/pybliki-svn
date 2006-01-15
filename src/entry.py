import os
from xml.dom.minidom import parseString
from time import strptime
from re import findall

def getEntryInformation(filename):
    """ This function gets the last log entry for given from SVN repository
    and parses it's contents. This functions scans if there are any additional
    files mentioned inside as well (images and etc). """

    svn_log = 'svn log --xml %s --limit 1' % filename
    pipe = os.popen(svn_log)
    xml = pipe.read()
    pipe.close()

    log = {}

    dom = parseString(xml)
    logentry = dom.getElementsByTagName('logentry')[0]

    author = logentry.getElementsByTagName('author')[0]
    log['author'] = author.firstChild.nodeValue.encode('utf-8')

    msg = logentry.getElementsByTagName('msg')[0]
    if msg.firstChild is not None:
        log['msg'] = msg.firstChild.nodeValue.encode('utf-8').strip()
    else:
        log['msg'] = ''

    date = logentry.getElementsByTagName('date')[0]
    log['date'] = strptime(date.firstChild.nodeValue[:19],
                           '%Y-%m-%dT%H:%M:%S')

    data = {}
    data['log'] = log

    f = file(filename)
    text = f.read()
    f.close()

    # scan for additional links in text file
    additional_files = []

    images = findall('image::\s.*', text)
    for image in images:
        spos = len('image:: ')
        imagefile = image[spos:].strip()
        additional_files.append(imagefile)

    files = findall('`.*\<.*\>`__', text)
    for f in files:
        if f.find('http://') == -1 and f.find('.html') == -1:
            spos = f.find('<')
            epos = f.find('>')
            additional_files.append(f[spos+1:epos])

    # set data
    text = text.replace('\r', '')
    data['text'] = text
    data['title'] = text.split('\n', 1)[0]
    data['name'] = os.path.splitext(os.path.basename(filename))[0]
    data['files'] = additional_files

    return data


