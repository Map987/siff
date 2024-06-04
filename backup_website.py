import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def backup_website(url, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # 获取当前日期作为文件名的一部分
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(backup_dir, f'{date_str}.html')

    # 发送 HTTP 请求获取网页内容
    response = requests.get(url)
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析网页
        soup = BeautifulSoup(response.text, 'html.parser')

        # 下载并替换图片链接
        for img_tag in soup.find_all('img'):
            img_url = img_tag['src']
            img_data = requests.get(img_url).content
            img_name = os.path.basename(img_url)
            img_path = os.path.join(backup_dir, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            img_tag['src'] = f'{date_str}/{img_name}'

        # 下载并替换 CSS 文件链接
        for link_tag in soup.find_all('link', rel='stylesheet'):
            css_url = link_tag['href']
            css_data = requests.get(css_url).content
            css_name = os.path.basename(css_url)
            css_path = os.path.join(backup_dir, css_name)
            with open(css_path, 'wb') as css_file:
                css_file.write(css_data)
            link_tag['href'] = f'{date_str}/{css_name}'

        # 保存修改后的 HTML 内容
        with open(file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(str(soup))
        print(f'Website backed up successfully: {file_path}')
    else:
        print(f'Failed to fetch the website: {url}')

if __name__ == '__main__':
    website_url = 'https://www.siff.com/'
    backup_dir = 'news'
    backup_website(website_url, backup_dir)
