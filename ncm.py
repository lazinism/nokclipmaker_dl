from pytube import YouTube
import ipaddress
import json, requests, urllib3, os
from datetime import datetime
from functools import reduce

forbidden_chars = "%:/\\<>*?？|！\n\""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
yt_dl_url = "https://www.youtube.com/watch?v={0}"
down_dir = os.getcwd() + "/videos/"
def on_complete(st, path):
    print("{0} 다운 완료.".format(path))
    
if __name__=="__main__":
    if not os.path.isdir(down_dir):
        print("videos 폴더가 존재하지 않아 생성합니다.")
        os.mkdir(down_dir)
    start_date = input("YYMMDD 형식으로 시작 날짜를 입력하세요.: ")
    end_date = input("YYMMDD 형식으로 끝 날짜를 입력하세요.: ")
    start_dt = datetime.strptime(start_date, '%y%m%d')
    end_dt = datetime.strptime(end_date, '%y%m%d')
    print("{0}부터 {1}까지의 클립을 다운로드 합니다.".format(start_dt.strftime("%y년%m월%d일"), end_dt.strftime("%y년%m월%d일")))
    url = "https://minbird.kr/clipmaker/api?re=clipList&direction=False&cn=50&ln={0}"
    response = requests.get(url.format("1"), verify=False)
    if(response.status_code == 200):
        data = json.loads(response.text)
    else:
        raise Exception('클립메이커 페이지가 정상 작동 중이지 않습니다.')
    page_count = data['PAGEALL']
    dl_queue = []
    for i in range(1, page_count):
        res = requests.get(url.format(i), verify=False)
        data = json.loads(res.text)
        for k,v in data.items():
            if not k == 'PAGEALL':
                date = datetime.strptime(data[k]['data']['strm_date'], '%y-%m-%d')
                if date >= start_dt and date <= end_dt:
                    safe_name = reduce(lambda x,y: x.replace(y, "_"), list(forbidden_chars), data[k]['cn'])
                    yt_url = data[k]['data']['yt_url']
                    dl_queue.append(("[{0}] {1}".format(data[k]['data']['strm_date'], safe_name), yt_url))
    for item in dl_queue:
        yt = YouTube(yt_dl_url.format(item[1]))
        try:
            yt.streams.get_highest_resolution().download(output_path=down_dir, filename="{0}.mp4".format(item[0]))
        except:
            print('에러 발생 - {0}'.format(item[1]))
        else:
            print("{0} 다운로드 완료.".format(item[0]))
