# -*- coding: utf-8 -*-
"""
    sphinx.ext.extlinks
    ~~~~~~~~~~~~~~~~~~~

    Minor mod of sphinx.ext.extlinks to allow specifying leptonica files
    and functions and have the URLs automatically converted to point at
    the Doxygen generated Reference Documentation.

    Extension to save typing and prevent hard-coding of base URLs in the reST
    files.

    This adds a new config value called ``doxylinks`` that is created like this::

       doxylinks = {'doxyfile': ('/Leptonica/%s.html', userfunc), ...}

    Now you can use e.g. :doxyfile:`foo.c` in your documents.  This will
    create a link to ``/leptonica/foo_8c.html``.

"""

import os
from lxml import etree

from docutils import nodes, utils
from sphinx.util.nodes import split_explicit_title

def _genDoxyDicts(doxytagFilename):
    """Extract html filename and function anchor from Doxygen GENERATE_TAGFILE
       file."""

    doxyFileDict = {}
    doxyFuncDict = {}

    tree = etree.parse(doxytagFilename)
    root = tree.getroot()
    files=root.findall("compound[@kind='file']")
    for fileElement in files:
        filename = fileElement.findtext("name")
        if filename == "leptprotos.h":
            continue
        dummy, ext = os.path.splitext(filename)
        if ext not in [".h", ".c"]:
            continue

        doxyFileDict[filename] = fileElement.findtext("filename") + ".html"
        functions = fileElement.findall("member[@kind='function']")
        for funcElement in functions:
            if funcElement.attrib.has_key("static"):
                continue
            funcName = funcElement.findtext("name")
            anchorFile = funcElement.findtext("anchorfile")
            anchor = funcElement.findtext("anchor")
            fileDict = doxyFuncDict.setdefault(funcName, {})
            fileDict[anchorFile] = anchor
            doxyFuncDict[funcName] = fileDict

    return doxyFileDict, doxyFuncDict

_doxyFileDict, _doxyFuncDict = _genDoxyDicts("../leptonica.doxy.tags")

def convertToDoxyFile(env, text):
    head, tail = os.path.split(text)
    root, ext = os.path.splitext(tail)
    if not ext:
        tail = tail + ".c"
        
    if _doxyFileDict.has_key(tail):
        return "doxyfile", (_doxyFileDict[tail],)
    env.warn(env.docname, 'unable to find doxyfile %s' % text)
    return "doxyfile", ('',)

def convertToDoxyFunc(env, text):
    text = text.replace("()", "")
    if _doxyFuncDict.has_key(text):
        filelist = _doxyFuncDict[text]
        keys = filelist.keys()
        return "doxyfunc", (keys[0], filelist[keys[0]])
    else:
        env.warn(env.docname, 'unable to find doxyfunc %s' % text)
        return "doxyfunc", ('',)

def make_link_role(base_url, userfunc):
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        text = utils.unescape(text)
        has_explicit_title, title, part = split_explicit_title(text)
        env = inliner.document.settings.env

        typ, parts = userfunc(env, text)
        try:
            full_url = base_url % parts
        except (TypeError, ValueError):
            env.warn(env.docname, 'unable to expand %s extlink with base '
                     'URL %r, please make sure the base contains \'%%s\' '
                     'the correct number of times for %s' % (typ,
                                                             base_url, text))
            full_url = base_url + parts[0]
        pnode = nodes.reference(title, title, internal=False, refuri=full_url)
        pnode['classes'].append(typ)

        return [pnode], []
    return role

def setup_link_roles(app):
    for name, (base_url, userfunc) in app.config.doxylinks.iteritems():
        app.add_role(name, make_link_role(base_url, userfunc))

def setup(app):
    app.add_config_value('doxylinks', {}, 'env')
    app.connect('builder-inited', setup_link_roles)
