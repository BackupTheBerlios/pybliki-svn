from docutils.core import publish_parts
from xml.dom.minidom import parse, Element
import os
import locale
import time


def generateBanners(root, cfg):
    banners_path, banners_dir = cfg.get('banners', 'dir')
    relpath = '../'*root[len(banners_path):].count('/')

    bannersinfo_path, banners_info = cfg.get('banners', 'info')
    result = ''

    dom = parse(os.path.join(bannersinfo_path, banners_info))
    for el in dom.documentElement.childNodes:
        if el.nodeType == Element.ELEMENT_NODE and el.tagName == 'item':
            image = el.getElementsByTagName('image')[0].firstChild.nodeValue
            image = image.encode('utf-8')
            links = el.getElementsByTagName('link')
            if len(links) > 0:
                link = links[0].firstChild.nodeValue.encode('utf-8')

            if image.find('http://') != -1:
                result += '<a href="%s"><img border="0" src="%s"></a>' \
                        % (link, image)
            else:
                result += '<a href="%s"><img border="0" src="%s"></a>' % \
                        (link, os.path.join(relpath, banners_dir, image))
    return result


def generatePage(root, cfg, entry):
    data = {}
    data['title'] = entry['title']
    data['author'] = entry['log'][-1]['author']
    path, css = cfg.get('misc', 'css')
    relpath = '../'*root[len(path):].count('/')
    data['css'] =  os.path.join(relpath, css)
    path, icon = cfg.get('misc', 'x-icon')
    relpath = '../'*root[len(path):].count('/')
    data['icon'] = os.path.join(relpath, icon)
    parts = publish_parts(entry['text'], writer_name='html')
    data['body'] = parts['html_body'].encode('utf-8')

    webroot = cfg.get('blog', 'webroot')
    blogname = cfg.get('blog', 'name')
    blogpath = '<a href="http://%s">%s</a>' % (webroot[1], blogname[1])
    sitepath = root[len(webroot[0])+1:]

    sidx = -1
    eidx = sitepath.find('/')
    while eidx != -1:
        blogpath += '/<a href="http://%s">%s</a>' % \
                (os.path.join(webroot[1], sitepath[:eidx]),
                 sitepath[sidx+1:eidx])

        sidx = eidx
        eidx = sitepath.find('/', eidx+1)

    if len(sitepath[sidx+1:]) > 0:
        blogpath += '/<a href="http://%s">%s</a>' % \
                    (os.path.join(webroot[1], sitepath),
                     sitepath[sidx+1:])

    data['blogpath'] = blogpath
    data['banners'] = generateBanners(root, cfg)

    locale.setlocale(locale.LC_ALL, cfg.get('blog', 'locale')[1])
    data['date'] = time.strftime(cfg.get('blog', 'timestamp')[1],
                                 entry['log'][0]['date'])

    path, tmplname = cfg.get('blog', 'template')
    f = file(os.path.join(path, tmplname))
    template = f.read()
    f.close()

    return template % data


def generateIndex(root, dirs, cfg, entries):
    entry = {}
    entry['title'] = 'Index'
    if len(entries) > 0:
        entry['log'] = [{'date': entries[0]['log'][0]['date'],
                         'author': entries[0]['log'][0]['author']}]
    else:
        entry['log'] = [{'date': time.gmtime(time.time()),
                         'author': ''}]

    text = 'Index\n=====\n\n'

    text += '* `.. <..>`__\n'
    for dir in dirs:
        text += '* `%(dir)s <%(dir)s>`__\n' % {'dir': dir}
    text += '\n'

    locale.setlocale(locale.LC_ALL, cfg.get('blog', 'locale')[1])

    for idx, e in enumerate(entries):
        text += '%d. `%s <%s>`__\n' % (idx+1, e['title'], e['name']+'.html')

        e['log'].reverse()

        for change in e['log']:
            if len(change['msg']) > 0:
                text += ' '*4 + time.strftime(cfg.get('blog', 'timestamp')[1],
                                             change['date']) + '\n'
                for line in change['msg'].split('\n'):
                    text += ' '*8 + line + '\n'
                text += '\n'

    entry['text'] = text

    return generatePage(root, cfg, entry)



