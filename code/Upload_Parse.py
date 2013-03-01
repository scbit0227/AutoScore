#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 wooparadog <wooparadog@1l0v3U4v3r>
#
# Distributed under terms of the MIT license.

from __future__ import division
import os
import re
from collections import defaultdict
import requests
import cPickle
import hashlib
from lxml import etree

upload_url = "http://knowminer.at:8080/team-pdf-extraction-webapp/extract/?action=upload"
result_extractor = re.compile("<h\d>(.*)<div", re.S|re.M)
block_splitter = re.compile("<h\d>")
block_end_splitter = re.compile("</h\d>")
list_item_finder = re.compile("<li>(.*?)</li>")
cache_dir = "cache"


def cache(content_getter):
    def __(f):
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        def key_builder(*arg, **kwds):
            raw_key = '_'.join(list(arg)+["%s_%s" % (k, v) for k, v in kwds.iteritems()])
            key = hashlib.md5()
            key.update(raw_key )
            return key.hexdigest()

        def _(*arg, **kwds):
            key = key_builder(*arg, **kwds)
            cache_path = os.path.join(cache_dir, key)
            if os.path.exists(cache_path):
                try:
                    result = cPickle.load(open(cache_path))
                except:
                    print "cache miss, reuploading"
                else:
                    print "cache hit"
                    return result

            result = f(*arg, **kwds)
            with open(cache_path, 'w') as fp:
                content = content_getter(result)
                fp.write(cPickle.dumps(content))
            return content
        return _
    return __

@cache(lambda x:x.text)
def upload(pdf_file):
    try:
        files = {
                "file": open(pdf_file, 'rb')
                }
    except IOError:
        print "file io error"
    else:
        return requests.post(upload_url, files=files)

def ul_to_list(html):
    """
    >>> ul_to_list("<ul><li>1.a</li><li>2.b</li></ul>")
    ['1.a', '2.b']
    >>> ul_to_list("asdfas asd fas df ")
    'asdfas asd fas df '
    """
    return list_item_finder.findall(html) or html

def sort_blocks(page_width, blocks):
    left_list = []
    right_list = []
    for block in blocks:
        if block.keys()[0][1] / page_width <= 0.4:
            left_list.append(block)
        else:
            right_list.append(block)
    return left_list + right_list

def parse_result(content):
    """
    metas:
    {
        "key": content # content is str if singular, else it's a list
        "author": ['rainywh269', 'wooparadog'],
        'abstract': "simple extractor",
    }

    blocks:
    {
        (name, chance): ["block1", "block2"...]
    }
    """
    html = content
    content = result_extractor.findall(html)
    metas = {}
    paper_info = {}
    block_list = []
    if content:
        content = content[0]
        for block in block_splitter.split(content):
            meta = block_end_splitter.split(block, 1)
            k, v = meta
            metas[k.strip()] = ul_to_list(v.strip())

    tree = etree.HTML(html.encode('utf8'))
    pages = tree.xpath('//div[@id="preview"]')
    
    page_index = 1
    for p in pages:
        paper_info[page_index] = []
        page_width = int(p.xpath(".//img//@width")[0])
        blocks = p.xpath('.//div[contains(@class, "block")]')
        for block in blocks:
            style = block.xpath(".//@style")[0]
            left = int(style.split(';')[1].split(':')[1][:-2])
            top = int(style.split(';')[2].split(':')[1][:-2])
            width = int(style.split(';')[3].split(':')[1][:-2])
            block_key = (top, left, width)
            block_value = block.xpath(".//span/text()")
            paper_info[page_index].append({block_key: block_value})
        paper_info[page_index] = sort_blocks(page_width, paper_info[page_index])
        block_list += paper_info[page_index]
            
        page_index += 1
   
    return metas, block_list

def analysis_pdf(pdf_file):
    content = upload(pdf_file)
    result = parse_result(content)
    return result

def main(test_pdf_file_path):
 
    metas, blocks = analysis_pdf(test_pdf_file_path)
    return metas, blocks