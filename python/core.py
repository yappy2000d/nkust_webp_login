import time
from io import BytesIO
from random import random

from PIL import Image
import requests as req
from bs4 import BeautifulSoup

from captcha import recognize


class Student:
    def __init__(self, username: str, password: str):
        self.school_url = 'https://webap.nkust.edu.tw/nkust/'
        self.username = username
        self.password = password
        self.client = req.session()

    def login(self):
        # Get login page
        response = self.client.get(self.school_url + 'index_main.html', verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get captcha answer
        captcha_image = self.client.get(self.school_url + f'validateCode.jsp?it={random()}', verify=False)
        captcha_answer = recognize(BytesIO(captcha_image.content))

        # Login
        data = {
            'uid': self.username,
            'pwd': self.password,
            'etxt_code': captcha_answer
        }
        response = self.client.post(self.school_url + 'perchk.jsp', data=data, verify=False)
        # print(response.content.decode('utf-8'))

    def get_home(self):
        # Get home page
        response = self.client.get(self.school_url + 'f_index.html', verify=False)
        print(response.content.decode('utf-8'))

    def welcome(self):
        response = self.client.get(self.school_url + 'f_head.jsp', verify=False)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        info = soup.find('div', {'class': 'personal'}).find_all('span')
        print(f'Welcome, {info[1].text} {info[2].text}!')

    def get_schedule(self, acade: int, semester: int) -> str:
        '''
        :param acade: 學年度
        :param semester: 學期
        :return: 課表
        '''
        # Get schedule page
        response = self.client.post(self.school_url + 'system/sys001_00.jsp?', data={
            'yms': f'{acade},{semester}',
            'spath': 'ag_pro/ag222.jsp?',
            'arg01': acade,
            'arg02': semester,
        }, verify=False)

        # response = self.client.get(self.school_url + 'f_index.html', verify=False)
        response = self.client.get(self.school_url + 'f_right.jsp', verify=False)
        print(response.content.decode('utf-8'))

    def logout(self):
        # Logout
        response = self.client.get(self.school_url + 'reclear.jsp', verify=False)
        # print(response.content.decode('utf-8'))

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        self.client.close()