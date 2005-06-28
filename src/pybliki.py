#!/usr/bin/env python

from sys import argv
import os
import locale
from os.path import join, splitext

from xml.dom.minidom import parseString
from time import strptime, strftime

from BlikiConfig import BlikiConfig
from xsite import generatePage
from rss import generateRSS

def getEntryInformation(xml):
    dom = parseString(xml)
    logentry = dom.getElementsByTagName('logentry')[0]
    date = logentry.getElementsByTagName('date')[0].firstChild.nodeValue;
    data = {'author':
                logentry.getElementsByTagName('author')[0].firstChild.nodeValue,
            'msg': 
                logentry.getElementsByTagName('msg')[0].firstChild.nodeValue,
            'date': strptime(date[:19], '%Y-%m-%dT%H:%M:%S')}
    return data

def main():
    if len(argv) < 2:
        print 'PyBliki weblog_directory'
        return

    os.chdir(argv[1])

    cfg = BlikiConfig()

    for root, dirs, files in os.walk('.'):
        cfg.testRoot(root, files)

        entries = []

        for filename in files:
            if splitext(filename)[1][1:] == \
                cfg.get('blog', 'extension')[1]:

                locale.setlocale(locale.LC_ALL, 
                                 cfg.get('blog', 'locale')[1])

                svn_log = 'svn log --xml --limit 1 %s' % (join(root, filename),)
                pipe = os.popen(svn_log)
                entry = getEntryInformation(pipe.read())
                pipe.close()

                time_str = strftime(cfg.get('blog', 'timestamp')[1],
                               entry["date"])

                f = file(join(root, filename))
                text = f.read()
                f.close()

                entry['title'] = text.split('\n', 1)[0]
                entries.append(entry)

                page = generatePage(cfg, text)

        # generate index file
        esort = lambda d1, d2: d1['date'] < d2['date']
        entries.sort(esort)

        text = 'Index\n=====\n\n'
        for idx, e in enumerate(entries):
            text += '%d. %s\n\n' % (idx, e['title'].encode('utf-8'))
            for l in e['msg'].split('\n'):
                text += '\t%s\n' % l.encode('utf-8')
            text += '\n'
        page = generatePage(cfg, text)

        # TODO: generate RSS file, entry filename
        generateRSS(entries)


        if '.svn' in dirs:
            dirs.remove('.svn')  # don't visit subversion directories


if __name__ == '__main__':
    main()
