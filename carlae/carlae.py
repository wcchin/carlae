# -*- coding: utf-8 -*-

# ====================================================================================
#
#    carlae - A simple stupid single webpage generator for project.
#    
# ====================================================================================

import sys
import os
from os.path import join as opj
from os.path import exists as opx
import shutil
import time
import re
import copy
from optparse import OptionParser

import jinja2
import markdown
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .docdata.yamldata import get_data as ygetdata
from .example_readme import EXAMPLE_FILES
    

def check_mkdir(outpath):
    #directory = os.path.dirname(outpath)
    #print(directory)
    if not opx(outpath):
        print('creating dir:', outpath)
        os.makedirs(outpath)
        

def text_export(outputText, outputPath):
    check_mkdir(os.path.dirname(outputPath))
    #print('writing file to:', outputPath)
    with open(outputPath, 'w') as f:
        f.write(outputText)#.encode("utf-8"))


# =============================================================================
# init site
# =============================================================================

def init(project='carlae_page', theme=None, output='docs', default_readme=False):
    """Initialize a site project."""
    HERE = os.path.dirname(os.path.realpath(__file__))
    THEME_DIR = opj(HERE, 'themes')
    
    cwd = os.getcwd()

    check_mkdir(opj(cwd, project))

    dir_out = opj(cwd, output)
    check_mkdir(dir_out)

    theme_dir = opj(project, "theme")
    if not(opx(theme_dir)):
        if theme is None: 
            theme = 'skeleton'
        elif not(theme in os.listdir(THEME_DIR)):
            print("the selected theme not in theme dir, will use skeleton")
            theme = 'skeleton'
        shutil.copytree(opj(THEME_DIR, theme), theme_dir)
    THEME_DIR = theme_dir
    
    static_dir = os.listdir(theme_dir)
    static_dir = [ d for d in static_dir if not(d[0]=='_') ]
    for d in static_dir:
        if not(opx(opj(dir_out, d))):
            shutil.copytree(opj(theme_dir, d), opj(dir_out, d))

    if default_readme:
        for fname, content in EXAMPLE_FILES.items():
            if not(opx(opj(cwd, fname))):
                print('info: create example %r' % fname)
                with open(opj(cwd, fname), 'w') as fp:
                    fp.write(content)
            else:
                print('README.md file exists, skip making default readme.md file')

    print("success: initialized project")


# =============================================================================
# build site
# =============================================================================


def build(target=None, output='docs'):
    
    cwd = os.getcwd()
    
    default_readme = False
    
    if target is None:
        tar = 'README.md'
        if tar in os.listdir(cwd):
            target = tar
        else:
            fs = os.listdir(cwd)
            fs2 = [ f.split('.')[0] for f in fs ]
            fs3 = [ f.lower() for f in fs2 ]
            if 'readme' in fs3:
                i = fs3.index('readme')
                target = fs[i]
            else:
                print('no readme file is found, make a default readme')
                #sys.exit(1)
                default_readme = True
    
    doc, doc_dic = get_doc(target)
    
    if 'theme' not in doc_dic: doc_dic['theme'] = None
    if 'carlae_dir' not in doc_dic: doc_dic['carlae_dir'] = 'carlae_page'
    init(project=doc_dic['carlae_dir'], theme=doc_dic['theme'], output=output, default_readme=default_readme)
                
    outpath = opj(cwd, output, 'index.html')
    theme_dir = opj(cwd, doc_dic['carlae_dir'], 'theme')
    process_one_page(doc, doc_dic, outpath, theme_dir)
    
    print('success: building project page')


def get_doc(target_file):
    cwd = os.getcwd()
    with open(opj(cwd, target_file), 'r') as f:
        doc = f.read()
    doc, doc_dic = ygetdata(doc)
    return doc, doc_dic
    
    
def process_one_page(doc, doc_dic, output_path, theme_dir):
    
    cwd = os.getcwd()
    #doc = doc.decode('utf-8')
    
    main_text = doc.split('\n')
    main_text2 = []
    menus = []
    for line in main_text:
        if line[:3]=='## ':
            text = line[3:]
            line = '<h2 id="{}">{}</h2>'.format(text.replace(' ','').lower(), text)
            if len(menus)>0:
                menus[-1][1].append((text.replace(' ','').lower(), text))
        elif line[:2]=='# ':
            text = line[2:]
            line = '<h1 id="{}">{}</h1>'.format(text.replace(' ','').lower(), text)
            menus.append([(text.replace(' ','').lower(), text), []])
        main_text2.append(check_icons(line))
    main_text = main_text2

    main_text_str = '\n'.join(main_text)    

    md = markdown.Markdown()
    html = md.convert(main_text_str)
    
    #print(html)
    #print(doc_dic)
    
    conf_default = {
        'template': 'page.html', 
        'top_title': 'A Read-Me Page', 
        'project_name': 'carlae', 
        'smart_title': None, 
        'author':'annonymous', 
        'short_description': 'short project description', 
        'three_concepts': None,
        'three_desc': None,
        'menu': {}, 
        'google_analytics': None,
        'concept_color': 'black'
    }
    
    for k,v in conf_default.items():
        if not k in doc_dic: doc_dic[k] = v
        
    if doc_dic['three_concepts'] is not None:
        doc_dic['concept_width'] = 'four'
        doc_dic['three_concepts'] = doc_dic['three_concepts'][:3]
        temp_concepts = []
        for con in doc_dic['three_concepts']:
            temp_concepts.append( check_icons(con) )
        doc_dic['three_concepts'] = temp_concepts
    
    doc_dic['content'] = html
    doc_dic['menus'] = menus
    #print(opj(THEME_DIR, 'templates'))
    template_loader = jinja2.FileSystemLoader( searchpath=opj(theme_dir, '_templates') )
    template_env = jinja2.Environment( loader=template_loader )
    template = template_env.get_template( doc_dic['template'] )
    output_text = template.render( doc_dic )
    
    text_export(output_text, output_path)
    


def check_icons(astring):
    sets = ['fab', 'fas', 'fal', 'far', 'fad']
    patterns = [ '\:{}-(.*?)\:'.format(setname) for setname in sets ]
    matches = [ re.findall(pat, astring) for pat in patterns ]
    bstring = copy.copy(astring)
    for mat, setname in zip(matches, sets):
        for m1 in mat:
            tag = '<i class="{} fa-{}"></i>'.format(setname, m1)
            target = ':{}-{}:'.format(setname, m1)
            bstring = bstring.replace(target, tag)

    pat_typcn = '\:typcn-(.*?)\:'
    mat = re.findall(pat_typcn, bstring)
    for m1 in mat:
        tag = '<span class="typcn typcn-{}"></span>'.format(m1)
        target = ':typcn-{}:'.format(m1)
        bstring = bstring.replace(target, tag)
    return bstring


class MyHandler(FileSystemEventHandler):
    def __init__(self, infile, outdir):
        self.infile = infile
        self.outdir = outdir

    def dispatch(self, event):
        build(self.infile, self.outdir)
        print("updated page")


def main():
    parser = OptionParser()
    parser.add_option("-i", "--input",
        dest="filename",
        help="the readme markdown file",
        default='README.md',
        metavar="readme.md")
    parser.add_option("-o", "--output",
        dest="output",
        help="tthe location to store the website",
        default='docs',
        metavar="docs")
    parser.add_option("-w", "--watch", action="store_true", dest="watch", default=False)

    options, args = parser.parse_args()
    build(target=options.filename, output=options.output)

    if options.watch:
        print("start watching changes")
        print("to stop watching, press ctrl+c")
        observer = Observer()
        event_handler = MyHandler(options.filename, options.output)
        path =  os.path.dirname(os.path.abspath(options.filename))
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        print("")
        print("watching stop")    