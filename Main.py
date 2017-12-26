#coding:utf-8

import Gentleman

url = "http://manhua.zsh8.com/pg/pxttfm/28101.html"
url1 = "http://manhua.zsh8.com/pg/zmdhfm/28155.html"
url2 = "http://manhua.zsh8.com/pg/qcsqfm/14049.html"
url3 = "http://manhua.zsh8.com/pg/pxttfm/28101.html/page/2"
save_path = "C:\Users\maois\Desktop\Desktop Temps\Python Temp"
gentleman = Gentleman.Gentleman(url1, save_path)
gentleman.Read()
