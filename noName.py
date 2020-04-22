
import requests
from lxml import etree
import queue
from urllib.parse import urlparse
import threading
import os
import re
from xml.dom.minidom import Document
# 下载图片
# 不知道起啥名字 哈哈
class NoName:
    url='https://www.diopoo.com/ark/characters?pn={0}'
    #现在图片的路径
    def __init__(self,path):
        super().__init__()
        self.header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
        }
        self.path = path
        self.host = urlparse(url=self.url).netloc
        print(self.host)
        self.session = requests.session()
    def get(self):
        self.doc = Document()
        self.root = self.doc.createElement("Root")
        self.root.setAttribute("text","noting")
        self.doc.appendChild(self.root)
        self.f = open('test.xml','w',encoding='utf-8')

        for i in range(1,10):
            self.getItems(str.format(self.url,i))
            break
        #f.write(doc.toprettyxml(indent = '\t', newl = '\n', encoding = 'utf-8'))
        self.doc.writexml(self.f,indent = '\t',newl = '\n', addindent = '\t',encoding='utf-8')
        self.f.close()
    def getItems(self,url):
        reg='(media/.*?.png)'
        response = self.session.get(url=url ,headers=self.header)
        xp = etree.HTML(response.text)
        itemList = xp.xpath('/html/body/div[2]/div[1]/ul[2]/li')
        for item in itemList:
            print('---------------------------------------')
            name  = item.xpath('./a[@class="name"]/text()')[0]

            pngPath = item.xpath('./div/a/@style')[0]
            remp = re.findall(reg,pngPath)[0]
            realpngPath = str.format("http://{0}/ark/{1}",self.host,remp)
            job = item.xpath('./div/img[@class="job shadow"]/@src')[0].split('/')[-1].replace(".png","")
            star=item.xpath('./div/img[@class="star"]/@src')[0].split('/')[-1].split('.')[0][-1]
            print(str.format("名字：{0}",name))
            print(str.format("图片地址：{0}",realpngPath))
            print(str.format("职业：\t{0}",job))
            print(str.format("稀有度：\t{0}",star))

            agent = self.doc.createElement("AgentItem")
            agent.setAttribute("Name",name)
            agent.setAttribute("job",job)
            agent.setAttribute("star",star)

            self.DownloadPng(realpngPath,name,self.path)
            self.root.appendChild(agent)
    def DownloadPng(self,url,name,path):
        print(path+name+".png")
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            response = self.session.get(url,headers=self.header)
            print(name+"----请求成功")
        except:
            print(name+"--------请求失败")
            return
        try:
            with open(path+name+".png",'wb+') as file:
                file.write(response.content)
            print(name+"----读写完成")
        except:
            print(name+"--------读写失败")
            return
            # agent.setIdAttribute()