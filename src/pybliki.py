#!/usr/bin/env python

from sys import argv
import os
import locale
from os.path import join, splitext

from time import strptime, strftime

from BlikiConfig import BlikiConfig
from entry import getEntryInformation
from xsite import generatePage
from rss import generateRSS

def main():
    if len(argv) < 2:
        print 'PyBliki weblog_directory'
        return

    cfg = BlikiConfig()

    for root, dirs, files in os.walk(os.path.abspath(argv[1])):
        cfg.testRoot(root, files)

        entries = []

        for filename in files:
            if splitext(filename)[1][1:] == \
                cfg.get('blog', 'extension')[1]:

                entry = getEntryInformation(join(root, filename))

                locale.setlocale(locale.LC_ALL, 
                                 cfg.get('blog', 'locale')[1])

                time_str = strftime(cfg.get('blog', 'timestamp')[1],
                               entry["date"])

                f = file(join(root, filename))
                text = f.read()
                f.close()

                entry['title'] = text.split('\n', 1)[0]
                entries.append(entry)

                page = generatePage(cfg, text)
                entry['name'] = splitext(filename)[0]

        # generate index file
        # TODO: generate directories
        esort = lambda d1, d2: d1['date'] < d2['date']
        entries.sort(esort)

        text = 'Index\n=====\n\n'
        for idx, e in enumerate(entries):
            text += '%d. %s\n\n' % (idx, e['title'].encode('utf-8'))
            for l in e['msg'].split('\n'):
                text += '\t%s\n' % l.encode('utf-8')
            text += '\n'
        page = generatePage(cfg, text)

        generateRSS(entries,
                    root,
                    cfg.get('blog', 'name')[1],
                    cfg.get('blog', 'webroot')[1])


        if '.svn' in dirs:
            dirs.remove('.svn')  # don't visit subversion directories


if __name__ == '__main__':
    main()
