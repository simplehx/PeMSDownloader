import requests
import datetime
import os
from tqdm import tqdm


session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Referer': 'https://pems.dot.ca.gov/?dnode=Clearinghouse&type=station_5min&district_id=3&submit=Submit',
    'Cookie': ''  # replace your cookie
}

# if you need to use proxy, please add the configuration
proxy = {
    # 'http': '127.0.0.1:7890',
    # 'https': '127.0.0.1:7890'
}

def download(year, district):
    download_url_list = []
    with open("download_urls.txt", encoding="utf-8") as f:
        download_url_list = f.read().splitlines()

    file_name_list = []
    dt = datetime.datetime.strptime("{}-01-01".format(year), "%Y-%m-%d")
    end_dt = datetime.datetime.strptime("{}-01-01".format(year + 1), "%Y-%m-%d")
    while dt < end_dt:
        file_name_list.append(str(dt.date()) + ".txt.gz")
        dt += datetime.timedelta(days=1)

    save_dir_path = district + "_" + str(year)
    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)
    download_completed_list = os.listdir(save_dir_path)

    for file_name, url in tqdm(zip(file_name_list, download_url_list)):
        try:
            if file_name in download_completed_list:
                continue
            if len(proxy) > 0:
                r = session.get(url=url, headers=headers, proxies=proxy)
            else:
                r = session.get(url=url, headers=headers)
            path = os.path.join(save_dir_path, file_name)
            with open(path, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print(file_name, e)

if __name__ == '__main__':
    download(year=2019, district="D4")