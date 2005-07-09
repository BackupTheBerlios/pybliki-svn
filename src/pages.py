from docutils.core import publish_parts
from os.path import join

def generatePage(cfg, text):
    # TODO: get author using `finger` or something similar
    # '<meta name="Author" content="?">'

    data = {}
    data['title'] = text.split('\n', 1)[0]
    path, css = cfg.get('misc', 'css')
    data['css'] =  join(path, css)
    path, icon = cfg.get('misc', 'x-icon')
    data['icon'] = join(path, icon)
    parts = publish_parts(text, writer_name='html')
    data['body'] = parts['html_body'].encode('utf-8')

    path, tmplname = cfg.get('blog', 'template')

    f = file(join(path, tmplname))
    template = f.read()
    f.close()

    print template % data


        #from xml.dom.minidom import parse, Element
        #dom = parse('rc/list.xml')
        #for el in dom.documentElement.childNodes:
        #    if el.nodeType == Element.ELEMENT_NODE and el.tagName == 'item':
        #        image = el.getElementsByTagName('image')[0].firstChild.nodeValue
        #        links = el.getElementsByTagName('link')
        #        if len(links) > 0:
        #            link = links[0].firstChild.nodeValue

        #        if image.find('http://') != -1:
        #            '<a href="%s"><img border="0" src="%s"></a>' % (link,image)
        #        else:
        #            '<a href="%s"><img border="0" src="rc/%s"></a>' % (link,image)
