#coding:utf-8

import urllib, urllib2
import re
import os
import zlib
import sys
import chardet
import random

class Gentleman:
    
    def __init__(self, url, path):
        default_encoding = 'utf-8'
        if sys.getdefaultencoding() != default_encoding:
            reload(sys)
            sys.setdefaultencoding(default_encoding)   
        self._create_dir(path)
        self._path = path
        self._url = url
    
    def _create_dir(self, path):
        try:
            path = path.rstrip("\\")
            isExists = os.path.exists(path.encode('gb2312'))
            if not isExists:
                os.makedirs(path.encode('gb2312'))
        except Exception, e:
            print "错误信息：" + "创建" + path + "失败;" + str(e)    
    
    def _get_content(self, url):
        error = 0
        while error < 5:
            try:
                request = urllib2.Request(url)
                user_agent = [
                    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
                    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
                    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'        
                ]            
                request.add_header("user-agent", random.choice(user_agent))
                response = urllib2.urlopen(request, timeout=20)
                coding = response.info().get('Content-Encoding')
                if coding == 'gzip':
                    decompressed_data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
                    main_content = decompressed_data.decode('gb2312', 'ignore')
                else:
                    main_content = response.read()
                return main_content
            except Exception, e:
                print "详细信息：" + url + "加载失败; " + str(e)
                print "详细信息：正在尝试重新加载:" + error
                error = error + 1
        print "详细信息：" + url + "尝试重新加载失败; "
        return None
        
    def _get_title(self, main_content):
        pattern = re.compile('<meta.?property="og:title".*?content="(.*?)".?/>')
        result = re.search(pattern, main_content)
        if result is None:
            return None
        else:
            title = result.group(1)
            return title
        
    def _get_catalogtitle(self, content):
        pattern = re.compile('<h2 class="fusion-post-title">(.*?)</h2>')
        result = re.search(pattern, content)
        if result is None:
            return None
        else:
            title = result.group(1)
            return title    
        
    def _get_catalogs(self, main_content):
        catalogs = []        
        while True:
            pattern = re.compile('<h2 class="blog-shortcode-post-title"><a href="(.*?)">.*?</a></h2>', re.S)
            items = re.findall(pattern, main_content)
            for item in items:
                catalogs.append(item)            
            pattern = re.compile('<a class="pagination-next" href="(.*?)">')
            result = re.search(pattern, main_content) 
            if result is None: 
                break
            nextnav = result.group(1)
            main_content = self._get_content(nextnav)
        if len(catalogs) > 0:
            return catalogs
        else:
            return None
    
    def _get_pages(self ,catalog_content):
        pages = []

        pattern = re.compile('<a href=\'(.*?)\' data-rel="lightbox-gallery-1">')
        items = re.findall(pattern, catalog_content)
        for item in items:
            pages.append(item) 
        if len(pages) > 0:
            return pages
        else:
            return None
    
    def _dl_catalogs(self, catalogs, title):
        catalog_path = self._path + "\\" + title##创建路径
        print catalog_path
        self._create_dir(catalog_path)##创建目录        
        for catalog_url in catalogs:
            catalog_content = self._get_content(catalog_url)
            catalogtitle = self._get_catalogtitle(catalog_content)
            get_pages = self._get_pages(catalog_content)
            self._dl_pages(get_pages, catalogtitle ,catalog_path)
    
    def _dl_pages(self, pages, catalogtitle, catalog_path):
        path = catalog_path + '\\' + catalogtitle
        print path
        self._create_dir(path)        
        for i in range(0, len(pages)): 
            try:
                downpath = path + "\\" + str(i + 1) + ".jpg"
                urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
                urllib.urlretrieve(pages[i], downpath.encode('gb2312'))
                print downpath + "下载完成"
            except Exception, e:
                print "详细信息："+pages[i] + "下载失败;" + str(e)
                return None
        print catalogtitle + "下载完成"

        
    def Read(self):
        try:
            content = self._get_content(self._url)
            ###芝士豪八动漫
            title = self._get_title(content)##获取标题
            print title
            catalogs = self._get_catalogs(content)##获取子目录列表
            dl_catalogs_result = self._dl_catalogs(catalogs, title)##开始下载##########
            self._title = title
            return title + "下载完成"
        except Exception, e:
            print "错误信息：读取失败; " + str(e)
            return None        