import re

a_list = ['\r\n                                    ',
 '\r\n                                ',
 '陈龙飞',
 '\r\n                                        ',
 '\r\n                                    ',
 '\r\n                                        ',
 '\r\n                                        ',
 '\r\n\r\n                                        ',
 '\r\n\r\n                                    ']
str = ''
for i in a_list:
    str += i
print(str)
ret = re.findall('\w+', str)
print(ret)