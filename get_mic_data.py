#coding:utf-8
#date:20110916
#抓取行业网站数据，为投放广告取得广告组名、目标网址、关键字。

import urllib
from pyExcelerator import *
from pyquery import PyQuery as pq

def main():
    w=Workbook()#创建excel表格
    ws=w.add_sheet(u'系列1')
    ws.write(0,0,u'广告组名称')
    ws.write(0,1,u'广告目标网址')
    ws.write(0,2,u'关键词')

    row=1
    url_list=[]
    urls=raw_input(u"请输入url地址：")
    result=pq(url=urls)('.cates')#所要抓取的内容所在的类
    print result
    for item in result:#result是一个列表结构
        li_tag=pq(item)('li')#广告组名称及链接在li标签里面
        for item in li_tag:
            ad_group=pq(item).text()#提取广告组名称
            index=ad_group.find('(',0)
            new_ad_group=ad_group[:index-1]#广告组名称去括号
            destination_url=pq(item).find('a').attr('href')#提取目标网址
            url_Prefix=r'http://construction.made-in-china.com'#url前缀
            new_destination_url=url_Prefix+destination_url#完整的url地址
            ws.write(row,0,new_ad_group)#写入广告组名
            ws.write(row,1,new_destination_url)#写入目标网址
            url_list.append(new_destination_url)#url列表
            row+=1
            
    row=1
    for item in url_list:
        keyword_list=get_keyword(item)#调用get_keyword函数
        column=2
        for item in keyword_list:    
            ws.write(row,column,item)
            column+=1
        row+=1
        
    w.save(ur'c:\documents and settings\all users\桌面\关键词表格.xls')#保存excel表格
    print 'the job has done!'


def get_keyword(urls):
    keyword_list=[]#关键词列表
    result=pq(url=urls)('.item')#关键词所在类名
    for item in result:
        keyword=pq(item)('a').text()#提取关键词
        ellipsis_index=keyword.rfind('...')
        if ellipsis_index!=-1:
            keyword=keyword[:ellipsis_index-1]#去除省略号
        Brackets_index=keyword.find('(')
        if Brackets_index!=-1:
            keyword=keyword[:Brackets_index-1]#去除括号
        keyword_list.append(keyword)#添加入列表
    return keyword_list#返回关键词列表
            
if __name__=='__main__':
    main()    
