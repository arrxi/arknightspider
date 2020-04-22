
import requests
from urllib.parse import urlparse
from lxml import etree
import os
#下载明日方舟头像图片
class HeadICon:
    path= "D:\\ArkNight\\headIcon\\"
    url = r'https://commons.moegirl.org/Special:%E6%96%B0%E5%BB%BA%E6%96%87%E4%BB%B6?like=%E6%98%8E%E6%97%A5%E6%96%B9%E8%88%9F+tx&user=Al+crayon&mediatype%5B%5D=BITMAP&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset='
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
        response = requests.get(url=self.url,headers=self.header)
        xp =  etree.HTML(response.text)
        lis = xp.xpath('//*[@id="mw-content-text"]/ul/li')
        for item in lis:
            pngName =  item.xpath('./div/div[@class="gallerytext"]/a/text()')[0].replace("明日方舟 tx ","").replace(".png","")
            pngPath =  item.xpath('./div/div[@class="thumb"]/div/a/img/@src')[0]
            # print(pngName)
            self.DownloadPng(pngPath,pngName)
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