import requests
from lxml import etree

# baseUrl = "https://zz.58.com/zufang/"
baseUrl = "https://short.58.com/zd_p/7a4b266c-46f6-4b28-af79-90046c81b42d/?target=hh-16-xgk_hvimob_80633147683502q-feykn&end=end"

headers = {
        "Cookie": "f=n; suid=2788842785; commontopbar_new_city_info=342%7C%E9%83%91%E5%B7%9E%7Czz; commontopbar_ipcity=zz%7C%E9%83%91%E5%B7%9E%7C0; id58=c5/nq1yTlrSAau+7A9yMAg==; 58tj_uuid=2d932d4c-1a37-412e-949f-9d7007a10eb3; als=0; gr_user_id=0c271ff4-a4da-4250-b93c-f27b74d5781f; city=bj; myfeet_tooltip=end; xxzl_smartid=174f78bd0c5ec6a064c634ae313f0b25; xxzl_deviceid=TMr9ksuhMeoLxRiWRD3d%2FAaU2Jm3QuJ3dEQ%2F%2F1FtKcILukl9OWFXlbEtB4d31Jcx; wmda_uuid=dc8bed86453410a79a2903033e04946b; wmda_visited_projects=%3B2385390625025; Hm_lvt_3f405f7f26b8855bc0fd96b1ae92db7e=1555854699; f=n; defraudName=defraud; Hm_lvt_dcee4f66df28844222ef0479976aabf1=1555855282; Hm_lpvt_dcee4f66df28844222ef0479976aabf1=1555855282; wmda_session_id_2385390625025=1555940491220-a5243c66-6333-8682; new_uv=3; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.58.com%252Fzufang%252F; ppStore_fingerprint=A11848BCDFD41469F79FB07F30963EF3C588C7EDB241AA79%EF%BC%BF1555940495420; new_session=0; Hm_lpvt_3f405f7f26b8855bc0fd96b1ae92db7e=1555941532; ipcity=zz%7C%u90D1%u5DDE; xzfzqtoken=gJmNtxjy4Z3jwWhius%2FCVJKhA6JlYhJZSmKzaYOxTGI0QRLTnXIrVOc1B57Hvk7din35brBb%2F%2FeSODvMgkQULA%3D%3D",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
    }
data = requests.get(url=baseUrl, headers=headers)
print(data.text)
# select = etree.HTML(data.text)

# all_url = select.xpath('//div[@class="des"]/h2/a[@class="strongbox"]/@href')

# print(all_url)

# f76dab0b-71aa-4172-a1df-ddc729bf7313

"https://jxjump.58.com/service?target=FCADV8oV3os7xtAj_6pMK7rUlr-5xUYu-P1OaSjHiTjM-aoDZpk1zEffDjpdRkNz3Q5xoKYl4Bi0ja0SHDAPlmTPfr4j0Jqa8lpuNyBP1ZKMCGY3WEmD8HmQwmaC4LBH1MoVDeEvZYetOdm5K6VJ2u1_JWjMWIdRJ4jzwZtAUEnEhkw4g-XYtVsBipal4H5QrUvdBp0MrWFI447Q-B-u3kfXEh3K6Q-YyQO7rZ4Va80-ZO1n0jhLeh81wXaoj08mTC5as&amp;pubid=70222437&amp;apptype=0&amp;psid=148873162203940485798820423&amp;entinfo=37831354680201_0&amp;cookie=||https%3A%2F%2Fwww.58.com%2Fzufang%2F|c5/nq1yTlrSAau 7A9yMAg==&amp;fzbref=0&amp;key=&amp;params=rankjxzfbestpc2099^desc&amp;from=1-list-1"
