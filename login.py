import re
import requests
from lxml import etree


class Login(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Host': 'github.com',
            'Referer': 'https://github.com/'
        }

        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    # 获取token的值
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers, verify=False)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div[@id="login"]/form/input[@name="authenticity_token"]/@value')[0]
        return token

    # 登录
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        cookies = self.session.cookies
        if response.status_code == 200 \
                and 'logged_in' in cookies.keys() \
                and cookies.get('logged_in') == 'yes':
            print('登录认证成功')
            print('加载项目列表...')
            self.loadRepos(response.text)
            response = self.session.get(self.logined_url, headers=self.headers)
            if response.status_code == 200:
                print('加载人员信息...')
                self.loadProfile(response.text)
        else:
            print('登录认证失败')

    def loadRepos(self, html):
        selector = etree.HTML(html)
        result = selector.xpath(
            '//div[@class="mb-3 Details js-repos-container mt-5"]//li[contains(@class,"no-description")]/div/a/@href')
        for item in result:
            print(item[1:])

    def loadProfile(self, html):
        selector = etree.HTML(html)
        username = selector.xpath('//input[@id="user_profile_name" and @value!=""]/@value')
        if username:
            print('username:', username)
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        if email:
            print('email:', email)


if __name__ == '__main__':
    client = Login()
    # 键入用户名和密码
    result = client.login(email='######', password='######')
