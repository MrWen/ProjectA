#!/usr/bin/python3

import logging
import sys
import cmysql
import re
import logging
import urllib.request
import os
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

mainUrl = 'http://tieba.baidu.com'

class MainUrl():
    """docstring for MainUrl"""
    def __init__(self, search_url):
        self.search_url = search_url
        self.b_next = True
        self.url_next = ''

class  UrlParser():
    def __init__(self, url):
        self.url = url
        self.cur_index = 0
        self.table_name = ''
        self.tieba_name = ''
        self.tieba_subject = ''
        self.table_insert = False

    def Start(self):
        print('start')
        db.Connect()
        datas = db.Fetch('select * from tieba_coef where name_type = 2')
        for row in datas:
            self.cur_index = row[2]
            db.Execute('update tieba_coef set cur_index = ' + str(self.cur_index +1) + ' where name_type = 2')

            self.table_name = 'tieba_template_' + str(self.cur_index)
            db.CreateTiebaTable(self.table_name)
        return True

    def DoWork(self, req_url):
        print('do work', req_url)

        html_content = urllib.request.urlopen(req_url).read()

        print('html_content', len(html_content))

        r_page = re.compile(r'<a href="(.*?)">下一页</a>')
        page_list = r_page.findall(html_content.decode('utf-8'))
        if len(page_list) > 0:
            self.url = mainUrl + page_list[0]
        else:
            self.url = None

        #r = re.compile('<title>(.*?)</title>')
        r = re.search(r'.*<div id="tofrs_up" class="tofrs_up"><a href="(.*?)" title="(.*?)"><.*', html_content.decode('utf-8'), re.M|re.I)
        if r:
            self.tieba_name = r.group(2)
        else:
            print('no match tieba_name')

        r = re.search(r'.*<h3 class="core_title_txt pull-left text-overflow  " title="(.*?)" .*', html_content.decode('utf-8'), re.M|re.I)
        if r:
            self.tieba_subject = r.group(1)
        else:
            print('no match tieba_subject')

        if self.table_insert == False:
            tmp_sql = "insert into tieba_name(table_name, tieba_name, sub_name, url, create_time) value('{0}','{1}','{2}','{3}',now())".format(self.table_name, self.tieba_name, self.tieba_subject, req_url)
            db.Execute(tmp_sql)
            self.table_insert = True

        #url+name
        r_user_1 = re.compile(r'<a style=".*" target="_blank" class=".*" href="(.*?)"><img username="(.*?)"')
        user_list_1 = r_user_1.findall(html_content.decode('utf-8'))
        #level
        r_user_2 = re.compile(r'<div class="d_badge_lv">(.*?)</div>')
        user_list_2 = r_user_2.findall(html_content.decode('utf-8'))
        #contect
        r_user_3 = re.compile(r'class="d_post_content j_d_post_content ">(.*?)</div>')
        user_list_3 = r_user_3.findall(html_content.decode('utf-8'))
        #time
        #<span class="tail-info">11楼</span><span class="tail-info">2016-08-08 20:50</span>
        r_user_4 = re.compile(r'<span class="tail-info">.*<span class="tail-info">(.*?)</span></div>')
        user_list_4 = r_user_4.findall(html_content.decode('utf-8'))

        if len(user_list_1) == len(user_list_3):
            for i in range(len(user_list_1)):
                user_id = 0
                user_name = (user_list_1[i][1]).strip()
                user_url = mainUrl + (user_list_1[i][0]).strip()
                user_context = (user_list_3[i]).strip().replace("'","\\'")
                user_level = (user_list_2[i]).strip()
                user_time = (user_list_4[i]).strip()

                if user_name in user_list:
                    user_id = user_list[user_name][0]
                else:
                    user_id = db.UpdateUserInfo(user_name, user_url, '', user_level)
                    user_list[user_name] = (user_id, user_url)

                context_sql = "insert into {0}(user_id, context, cur_time) Value({1},'{2}','{3}')".format(self.table_name, user_id, user_context, user_time)
                db.Execute(context_sql)
        else:
            print("len not match")

        self.GetUserInfo()

        return True

    def GetUserInfo(self):
        for (k,v) in user_list.items():
            datas = db.Fetch('select * from user_dynamics where user_id = ' + str(v[0]))
            if datas and len(datas) > 0:
                continue
            else:
                html_content = urllib.request.urlopen(v[1]).read()
                r = re.compile('class="u-f-item unsign"><span>(.*?)</span>')
                tieba_list = r.findall(html_content.decode('GBK'))
                for i in range(len(tieba_list)):
                    insert_sql = "insert into tieba_attention(user_id, attention, peoples, update_time) Value({0},'{1}',0 ,now())".format(v[0], tieba_list[i])
                    db.Execute(insert_sql)

                r_context = re.compile('<ul class="new_list clearfix">(.*?)</ul>')
                context_list = r_context.findall(html_content.decode('GBK'))

        print('GetUserInfo End')

    def SetUrl(self, url):
        self.url = url

tiebaMain = MainUrl('http://tieba.baidu.com/f?kw=%E5%86%92%E9%99%A9%E4%B8%8E%E6%8C%96%E7%9F%BF&ie=utf-8&pn=0')
#tiebaMain = MainUrl('http://tieba.baidu.com/f?ie=utf-8&kw=%E8%AE%A4%E7%9C%9F')

user_list = {}

db = cmysql.CMysql('127.0.0.1', 3306, 'root', '', 'tieba')

def main():
    #url.SetUrl('http://tieba.baidu.com/p/4722442838')
    while tiebaMain.b_next:
        try:
            html_content = urllib.request.urlopen(tiebaMain.search_url).read()
            r = re.compile('<a href="(.*?)" class="next pagination-item " >下一页&gt;</a>')

            url_main_list = r.findall(html_content.decode('utf-8'))
            if len(url_main_list) == 0:
                tiebaMain.b_next = False
                tiebaMain.search_url = ''

            for x in range(len(url_main_list)):
                tiebaMain.search_url = url_main_list[x]
            
            r_url = re.compile(' <a href="(.*?)" title=".*" target="_blank" class="j_th_tit ">')

            url_list = r_url.findall(html_content.decode('utf-8'))
            for i in range(len(url_list)):
                url = UrlParser('http://tieba.baidu.com' + url_list[i])
                if(url.Start()):
                    while url.url:
                        url.DoWork(url.url)
                    print('success', url.url)
                else:
                    print('fail')

        except Exception as e:
            print(e)
        
    print('end')

if __name__ == '__main__':
    main()
