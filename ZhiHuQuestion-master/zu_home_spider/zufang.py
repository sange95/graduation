from pprint import pprint

import requests
from lxml import etree
from copy import deepcopy
from pymongo import MongoClient

from config import HOST, POST


class fangtianxia:
    def __init__(self):
        self.start_url = "https://zz.zu.fang.com/"
        self.url_header = "https://zz.zu.fang.com"
        self.headers = {
            "Cookie": "integratecover=1; global_cookie=ne8iwofvlvqjz1olucfej3bhn1yjtwi3l41; city=zz; g_sourcepage=undefined; ASP.NET_SessionId=yvxg3pozpoz2qzx0rnvu4s3h; Rent_StatLog=502eca23-ff7f-4cdb-b52a-6544c89d6e33; keyWord_recenthousezz=%5b%7b%22name%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a0362%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e6%b1%bd%e9%85%8d%e5%a4%a7%e4%b8%96%e7%95%8c%22%2c%22detailName%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a0362-b02929%2f%22%2c%22sort%22%3a2%7d%5d; unique_cookie=U_2a4pv3cxivdhxuvjufoep0own3pju3gwd32*12; Captcha=562F426D6348733555734F4859434D536149737359747541345A66593468447038755730374B4B4741716465335677767264784C4937487A41657A3746533677546861494C6D535A3339773D",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        }
        self.headers1 = {
            "Cookie": "integratecover=1; global_cookie=ne8iwofvlvqjz1olucfej3bhn1yjtwi3l41; city=zz; g_sourcepage=undefined; ASP.NET_SessionId=yvxg3pozpoz2qzx0rnvu4s3h; Rent_StatLog=502eca23-ff7f-4cdb-b52a-6544c89d6e33; keyWord_recenthousezz=%5b%7b%22name%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a0362%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e6%b1%bd%e9%85%8d%e5%a4%a7%e4%b8%96%e7%95%8c%22%2c%22detailName%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a0362-b02929%2f%22%2c%22sort%22%3a2%7d%5d; Captcha=4367676249316B646671665A69767657637A72336375754E627467782F75313169585A52477967377A72324A306E65705952786C775964573631353136796A7045496261335969474273553D; unique_cookie=U_2a4pv3cxivdhxuvjufoep0own3pju3gwd32*13",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        }

    def get_detail_info(self, resp, local):
        pass

    def get_detail(self, local_list):
        # print(local_list)
        for local in local_list:
            # 保存每个大区,房子详情url
            # print(local)
            info_list = list()
            url = local["local_url"]
            resp = self.start(url).content.decode("gbk")
            html = etree.HTML(resp)
            detail_list = html.xpath("//div[@class='houseList']/dl[@class='list hiddenMap rel']//dd[@class='info rel']/p[1]/a/@href")
            # print(etree.tostring(dl_list).decode())
            for detail_url in detail_list:
                items = deepcopy(local)
                items["detail_url"] = self.url_header + detail_url
                resp = self.start1(items["detail_url"]).content.decode("gbk")
                html = etree.HTML(resp)
                items['title'] = html.xpath('//div[@class="tab-cont clearfix"]/h1/text()')
                # print(len(html.xpath("//a[@id='agantzfxq_C02_05']/div[@class='bigImg']/img[1]/@src")[0]))
                items['image_url'] = "https:" + html.xpath("//a[@id='agantzfxq_C02_05']/div[@class='bigImg']/img[1]/@src")[0]
                # print(items)
                items['money'] = html.xpath("//div[@class='trl-item sty1']/i/text()")[0]
     #            print(html.xpath("//div[@class='tab-cont-right']/div[5]/div[1]/div[2]/a/text()")
     # )
                items['xiaoqu_name'] = html.xpath("//div[@class='tab-cont-right']/div[5]/div[1]/div[2]/a/text()")
                items['dizhi'] = html.xpath("//div[@class='tab-cont-right']/div[5]/div[2]/div[@class='rcont']/a/text()")[0]
                # items['ruzhu_time'] = html.xpath("//div[@class='tab-cont-right']/div[5]/div[3]/div[@class='rcont']//text()")[0]
                items['house_person'] = html.xpath("//div[@class='trlcont rel']/div[1]/div/a[1]/text()")[0]
                items['phone'] = html.xpath("//div[@class='tjcont-list-cline2 tjcont_gs clearfix']/p/text()")[0]
                # pprint(items)
                # print(len(html.xpath("//div[@class='tjcont-list-cline2 tjcont_gs clearfix']/p/text()")[0]))
                # 保存到mongodb

                client = MongoClient(HOST, POST)
                collection = client["72bian"]["zufang"]
                collection.insert(items)


    def start1(self, url):
        resp = requests.get(url=url, headers=self.headers1)
        return resp


    def start(self, url):
        resp = requests.get(url=url, headers=self.headers)
        return resp

    def get_info(self, resp):
        # 存放所有的地区和url
        alist = list()
        html = etree.HTML(resp)
        a_list = html.xpath("//div[@class='con']/div[@class='search-listbox']/dl[1]/dd/a")[1:]
        # print(a_list[1])
        # print(len(a_list))
        for a in a_list:
            items = dict()
            items["local_url"] = self.url_header + a.xpath("@href")[0]
            items["local"] = a.xpath("text()")[0]
            alist.append(items)
        return alist


    # 启动项
    def run(self):
        # 请求郑州区域的url
        resp = self.start(self.start_url)
        # print(resp.text)
        # 获得所有地区和url
        local_list = self.get_info(resp.content.decode("gbk"))
        # 获取区域内租房信息
        self.get_detail(local_list)





if __name__ == '__main__':
    ft = fangtianxia()
    ft.run()