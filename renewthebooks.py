##############################
#
#时间：2015-01-15
#作者： truehyp
#说明：程序能自动续借用户所有书籍，续借后，借阅时间变为当前时间，应还时间为借阅时间加续借的天数（默认为30)
#
##############################
import urllib
import urllib.request
import http.cookiejar
import re
import getpass


#获取用户名和密码，并且组成postdata
name = input('username: ')
pwd = getpass.getpass('password: ')
data=b'T1='+name.encode('gb2312')+b'&xm=&tday1=26360&B1=%b5%c7%c2%bd&T3='+pwd.encode('gb2312')

#登陆信息
login_request=urllib.request.Request('http://lib.cjlu.edu.cn/ttweb/dz.php',data)
#设置cookie
cookie=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
#登陆
response=opener.open(login_request)
#登陆返回页面
ans=response.read().decode('gb2312')

if re.findall(r'没有该读者',ans):
    print('没有该读者，请重新运行程序')
    input("按任意键退出: ")
    exit()

if re.findall(r'重新输入',ans):
	print('输入读者号和密码')
	input("按任意键退出: ")
	exit()

#匹配书的编号
match_number=re.findall(r'<tr><td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?</tr>',ans,re.S)

#生成postdata
data1=b'T1='+name.encode('gb2312')+b'&Submit=%d0%f8%bd%e8%d1%a1%d6%d0%cd%bc%ca%e9'
for item in match_number:
    data1=b'netxj%5b%5d='+item.encode('gb2312')+b'%2f%2f30%2f%2f-1&'+data1
#续借信息
print ('正在续借所有书籍...')
xj_request=urllib.request.Request('http://lib.cjlu.edu.cn/ttweb/bkxj1.php',data1)
#进行续借操作
response=opener.open(xj_request)
#续借返回页面
ans=response.read().decode('gb2312')
###加一个返回信息，提示续借结果
if re.findall(r'成功',ans):
    print('成功续借')
else:
    print('续借失败')
input("按任意键退出: ")
exit()
