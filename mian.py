import re
import hashlib
import requests
import json

def make_enc(time, clazzId, duration, clipTime, objectId, jobid, userid):
    if jobid == None:
        jobid = ''
    raw = '[{0}][{1}][{2}][{3}][{4}][{5}][{6}][{7}]'.format(clazzId, userid, jobid, objectId, time*1000, "d_yHJ!$pdA~5", duration*1000, clipTime)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def make_sequence(clazzId, duration, clipTime, objectId, jobid, userid):
    playingTime = -60
    result = []
    while playingTime < duration:
        playingTime += 60
        if playingTime > duration:
            playingTime = duration
        enc = make_enc(playingTime, clazzId, duration, clipTime, objectId, jobid, userid)
        result.append((playingTime, enc))
    return result

def get_mArg(url, cookies):
    chapterId = re.search(r'chapterId=(.*?)&', url).group(1)
    clazzId = re.search(r'clazzid=(.*?)&', url).group(1)
    courseId = re.search(r'courseId=(.*?)&', url).group(1)
    url = "http://mooc1.mooc.whu.edu.cn/knowledge/cards?clazzid=" + clazzId + "&courseid=" + courseId + "&knowledgeid=" + chapterId + "&num=0&ut=s&cpi=64752888&v=20160407-1"
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    headers = {'User-Agent':ua}
    html = requests.get(url, cookies=cookies, headers=headers).text
    mArg_string  = re.search("mArg = ({.+?});", html, re.S).group(1)
    mArg = json.loads(mArg_string)
    return mArg

def play_video(url, cookies):
    mArg = get_mArg(url, cookies)
    clazzId = mArg['defaults']['clazzId']
    userid = mArg['defaults']['userid']
    for video in mArg['attachments']:
        duration = int(video['headOffset'])/1000
        clipTime = '0_' + str(duration)
        objectId = video['objectId']
        otherInfo = video['otherInfo']
        jobid = video['jobid']
        sequence = make_sequence(clazzId, duration, clipTime, objectId, jobid, userid)
        for info in sequence:
            playingTime = info[0]
            enc = info[1]
            pass


if __name__ == '__main__':
    url = "http://mooc1.mooc.whu.edu.cn/mycourse/studentstudy?chapterId=331570352&courseId=207018950&clazzid=14103123&enc=5085df6bb6f7a2546c8ad0a57d938da3"
    f = open(r'cookies.txt', 'r')  # 打开所保存的cookies内容文件
    cookies = {}  # 初始化cookies字典变量
    for line in f.read().split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    play_video(url, cookies)