#!/usr/bin/env python

from sys import argv
import os
from tempfile import mkdtemp
import shutil

from BlikiConfig import BlikiConfig
from entry import getEntryInformation
from pages import generatePage, generateIndex
from rss import generateRSS

def main():
    if len(argv) < 2:
        print 'PyBliki weblog_directory'
        return

    blogroot = os.path.abspath(argv[1])
    tempdir = mkdtemp('', 'blog')

    cfg = BlikiConfig()

    for root, dirs, files in os.walk(blogroot):
        cfg.testRoot(root, files)

        # create directories inside temp
        dirname = root[len(blogroot)+1:]
        if len(dirname) > 0:
            name = os.path.join(tempdir, dirname)
            os.mkdir(name)

        entries = []

        # copy files
        icon_path, icon = cfg.get('misc', 'x-icon')
        if icon_path == root:
            shutil.copy(os.path.join(icon_path, icon),
                        os.path.join(tempdir, dirname))

        css_path, css = cfg.get('misc', 'css')
        if css_path == root:
            shutil.copy(os.path.join(css_path, css),
                        os.path.join(tempdir, dirname))

        banners_path, banners_dir = cfg.get('banners', 'dir')
        if banners_path == root:
            os.mkdir(os.path.join(tempdir, dirname, banners_dir))
            for name in os.listdir(os.path.join(banners_path, banners_dir)):
                fullname = os.path.join(banners_path, banners_dir, name)
                if os.path.isfile(fullname):
                    shutil.copy(fullname, os.path.join(tempdir, dirname,
                                                       banners_dir, name))

        # get entries and print pages
        index_exists = False
        for filename in files:
            if os.path.splitext(filename)[1][1:] == \
                cfg.get('blog', 'extension')[1]:

                entry = getEntryInformation(os.path.join(root, filename))
                entries.append(entry)

                if entry['name'] == 'index':
                    index_exists = True

                page = generatePage(root, cfg, entry)
                f = file(os.path.join(tempdir, dirname, entry['name']+'.html'),
                         'w')
                f.write(page)
                f.close()

                # copy images and other files
                for f in entry['files']:
                    filepath = os.path.join(tempdir, dirname, f)
                    filepath = os.path.normpath(filepath)
                    addpath, addfile = os.path.split(filepath)

                    tocreate = []
                    while not os.path.isdir(addpath):
                        addpath, notexists = os.path.split(addpath)
                        tocreate.append(notexists)

                    while len(tocreate) > 0:
                        addpath = os.path.join(addpath, tocreate.pop())
                        os.mkdir(addpath)

                    shutil.copy(os.path.join(root, f), filepath)

        # Remove ignored folders
        if '.svn' in dirs:
            dirs.remove('.svn')  # don't visit subversion directories

        if banners_path == root and banners_dir in dirs:
            dirs.remove(banners_dir)   # don't visit banners directories

        logfile = 'index.html'
        if index_exists:
            logfile = 'log.html'

        page = generateIndex(root, dirs, cfg, entries)
        f = file(os.path.join(tempdir, dirname, logfile), 'w')
        f.write(page)
        f.close()

        rss = generateRSS(root[len(blogroot):], cfg, entries)
        f = file(os.path.join(tempdir, dirname, 'index.rss'), 'w')
        f.write(rss)
        f.close()

    # upload
    os.system('scp -r %s/* %s' % (tempdir, cfg.get('blog', 'ssh')[1]))

    # remove
    shutil.rmtree(tempdir)


if __name__ == '__main__':
    main()
