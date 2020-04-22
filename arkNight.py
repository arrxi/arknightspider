
import requests
from urllib.parse import urlparse
from lxml import etree
import os
#下载明日方舟技能图标
class ArkNight:
    url = r"http://ak.mooncell.wiki/w/%E5%88%86%E7%B1%BB:%E6%8A%80%E8%83%BD%E5%9B%BE%E6%A0%87"
    path= "D:\\ArkNight\\"
    def __init__(self):
        super().__init__()
        self.header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
        }
        self.host = urlparse(url=self.url).netloc
        print(self.host)
        self.session = requests.session()
    def getItem(self):
        response = self.session.get(self.url,headers=self.header)
        xp = etree.HTML(response.text)
        arkhightList = xp.xpath('//*[@id="mw-category-media"]/ul/li')
        print(len(arkhightList))
        for item in arkhightList:
            pngName =  item.xpath('./div/div[@class="gallerytext"]/a/text()')[0].replace("技能 ","").replace(".png","")
            pngPath =  item.xpath('./div/div[@class="thumb"]/div/a/img/@data-src')[0]
            pnguri = "http://" +self.host+pngPath
            response = self.session.get(url=pnguri,headers = self.header)
            self.DownloadPng(pnguri,pngName)
    def DownloadPng(self,url,name):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        try:
            response = self.session.get(url,headers=self.header)
            print(name+"请求成功")
        except:
            print(name+"--------请求失败")
            return
        try:
            with open(self.path+name+".png",'wb+') as file:
                file.write(response.content)
            print(name+"--------读写完成")
        except:
            print(name+"--------读写失败")
            return