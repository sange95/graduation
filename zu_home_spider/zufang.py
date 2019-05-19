import random
import re
from pprint import pprint
import gevent
import time
from gevent import monkey

import requests
from lxml import etree
from copy import deepcopy
import uuid
from pymongo import MongoClient

from config import HOST, POST, DBNAME, SETNAME

monkey.patch_all()


class fangtianxia:
    A = 1

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

    def get_uuid(self):
        return str(uuid.uuid1())

    # def save_img(self, url_list):
    #     for url in url_list:
    #         resp = self.start(url).content.decode('utf8')
    #

    # def get_detail_info(self, resp, local):
    #     pass
    def get_infos(self, t):
        detail_url = t[0]
        local = t[1]
        items = deepcopy(local)
        items["_id"] = self.get_uuid()
        # print(items["_id"])
        items["detail_url"] = self.url_header + detail_url
        print(items["detail_url"])
        try:
            time.sleep(random.random())
            # print("正在爬取第{}条数据".format(self.A))
            resp = self.start1(items["detail_url"]).content.decode("gbk")
            html = etree.HTML(resp)
            items['title'] = html.xpath('//div[@class="tab-cont clearfix"]/h1/text()')
            # print(len(html.xpath("//a[@id='agantzfxq_C02_05']/div[@class='bigImg']/img[1]/@src")[0]))
            img_url = html.xpath("//a[@id='agantzfxq_C02_05']/div[@class='bigImg']/img/@src")
            img_url = ["https:" + url for url in img_url]
            # items['image_url'] = img_url
            # 将图片保存在本地
            url_list = list()
            for url in img_url:
                # print(url)
                # time.sleep(0.5)
                resp = self.start(url)
                # print(type(resp.content().decode("utf8")))
                # print(resp)
                # print(resp.content)
                # print(resp.text())
                with open("../information/info/static/imgs/rent/{}.jpg".format(self.get_uuid()), "wb") as f:
                    # resp = resp.content.decode("utf8")
                    f.write(resp.content)
                url_list.append("{}.jpg".format(self.get_uuid()))

            items["image_url"] = url_list

            # # print(items)
            items['money'] = html.xpath("//div[@class='trl-item sty1']/i/text()")[0]
            zhifu = html.xpath("//div[@class='trl-item sty1']/text()")[0]
            #            print(html.xpath("//div[@class='tab-cont-right']/div[5]/div[1]/div[2]/a/text()")
            # )
            zhifu = re.sub(r"(元/月\（)|(\）)", '', zhifu)
            # print(zhifu)
            # items["_id"] = items["local"]
            # div_list = html.xpath("//div[@class='tab-cont-right']/div[3]")
            items['chuzufangshi'] = \
                html.xpath(
                    '//div[@class="tab-cont-right"]/div[3]/div[@class="trl-item1 w146"]/div[@class="tt"]/text()')[0]
            items["huxing"] = html.xpath('//div[@class="tab-cont-right"]/div[3]/div[2]/div[@class="tt"]/text()')[0]
            items["jianzumianji"] = html.xpath("//div[@class='tab-cont-right']/div[3]/div[3]/div[@class='tt']/text()")[
                0]
            divs = html.xpath("//div[@class='tab-cont-right']/div[4]")[0]
            items["chaoxiang"] = divs.xpath("//div[@class='tab-cont-right']/div[4]/div[1]/div[@class='tt']/text()")[0]
            items["zongloucheng"] = \
            divs.xpath("//div[@class='tab-cont-right']/div[4]/div[2]/div[@class='font14']/text()")[
                0]
            items["loucheng"] = divs.xpath("//div[@class='tab-cont-right']/div[4]/div[2]/div[@class='tt']/text()")[0]
            items["zhuangxiu"] = divs.xpath("//div[@class='tab-cont-right']/div[4]/div[3]/div[@class='tt']/text()")[0]

            items['zhifufangshi'] = zhifu
            items['xiaoqu_name'] = html.xpath("//div[@class='tab-cont-right']/div[5]/div[1]/div[2]/a/text()")
            items['dizhi'] = html.xpath("//div[@class='tab-cont-right']/div[5]/div[2]/div[@class='rcont']/a/text()")[0]
            # items['ruzhu_time'] = html.xpath("//div[@class='tab-cont-right']/div[5]/div[3]/div[@class='rcont']//text()")[0]
            str_list = html.xpath("//div[@class='trlcont rel']/div[1]/div//a[1]/text()")
            # pprint(items['house_person'])
            str = ''
            for i in str_list:
                str += i
            # print(str)
            ret = re.findall('\w+', str)[0]

            items['house_person'] = ret
            # print(ret)
            items['phone'] = html.xpath("//div[@class='tjcont-list-cline2 tjcont_gs clearfix']/p/text()")[0]
            items['liulanrenshu'] = random.randint(500, 1500)
            items['fangyuanliangdian'] = html.xpath(
                "//li[@class='font14 fyld']/div[@class='fyms_con floatl gray3']//text()")
            items['xiaoqujieshao'] = html.xpath(
                "//li[@class='font14 xqjs']/div[@class='fyms_con floatl gray3']//text()")
            items['zhoubianpeitao'] = html.xpath(
                "//li[@class='font14 zbpt']/div[@class='fyms_con floatl gray3']//text()")
            items['jioatongchuxing'] = html.xpath(
                "//li[@class='font14 jtcx']/div[@class='fyms_con floatl gray3']//text()")
            # self.A += 1
        except:
            # print(self.A)
            # self.A += 1
            pass

        # pprint(items)
        # pprint(items)
        # 保存图片在本地



        # print(len(html.xpath("//div[@class='tjcont-list-cline2 tjcont_gs clearfix']/p/text()")[0]))
        # 保存到mongodb

        client = MongoClient(HOST, POST)
        collection = client[DBNAME][SETNAME]
        collection.insert(items)

    def get_detail(self, local_list):
        # print(local_list)
        for local in local_list:
            # print(local["local"])
            # 保存每个大区,房子详情url
            # print(local)
            # info_list = list()
            url = local["local_url"]
            try:
                resp = self.start(url).content.decode("gbk")
                html = etree.HTML(resp)
                detail_list = html.xpath(
                    "//div[@class='houseList']/dl[@class='list hiddenMap rel']//dd[@class='info rel']/p[1]/a/@href")
                # print(etree.tostring(dl_list).decode())
                url_list = list()
                for detail_url in detail_list:
                    url_list.append(detail_url)
                    if len(url_list) == 3:
                        # self.A += 1
                        # print(self.A)
                        gevent.joinall([
                            gevent.spawn(self.get_infos, (url_list[0], local)),
                            gevent.spawn(self.get_infos, (url_list[1], local)),
                            gevent.spawn(self.get_infos, (url_list[2], local))
                        ])
                        url_list = []
            except:
                pass

    def start1(self, url):
        try:
            resp = requests.get(url=url, headers=self.headers1, timeout=3)
            return resp
        except:
            pass

    def start(self, url):
        try:
            resp = requests.get(url=url, headers=self.headers, timeout=3)
            return resp
        except:
            pass

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
