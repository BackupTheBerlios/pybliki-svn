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
    data['css'] =  os.path.join(path, css)
    path, icon = cfg.get('misc', 'x-icon')
    data['icon'] = os.path.join(path, icon)
    parts = publish_parts(entry['text'], writer_name='html')
    data['body'] = parts['html_body'].encode('utf-8')
    data['blogname'] = cfg.get('blog', 'name')[1]
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
    esort = lambda d1, d2: d1['log'][0]['date'] < d2['log'][0]['date']
    entries.sort(esort)
    entries.reverse()

    entry = {}
    entry['title'] = 'Index'
    entry['log'] = [{'date': entries[0]['log'][0]['date'],
                     'author': entries[0]['log'][0]['author']}]

    text = 'Index\n=====\n\n'

    for dir in dirs:
        text += '* ' + dir + '\n'
    text += '\n'

    locale.setlocale(locale.LC_ALL, cfg.get('blog', 'locale')[1])

    for idx, e in enumerate(entries):
        text += '%d. `%s <%s>`__\n' % (idx+1, e['title'], e['name']+'.html')

        e['log'].reverse()

        for change in e['log']:
            text += ' '*4 + time.strftime(cfg.get('blog', 'timestamp')[1],
                                         change['date']) + '\n'
            for line in change['msg'].split('\n'):
                text += ' '*8 + line + '\n'
            text += '\n'

    entry['text'] = text

    return generatePage(root, cfg, entry)



