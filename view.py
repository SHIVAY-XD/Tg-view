import os
try:
 import requests
 from time import sleep
 from configparser import ConfigParser
 from os import system, name
 from threading import Thread, active_count
 from re import search, compile
except:
 os.system('pip install requests')
 os.system('pip install configparser')
THREADS = 500
PROXIES_TYPES = ('http', 'socks4', 'socks5')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
REGEX = compile(r"(?:^|\D)?(("+ r"(?:[1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"):" + (r"(?:\d|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}"
                + r"|65[0-4]\d{2}|655[0-2]\d|6553[0-5])")
                + r")(?:\D|$)")

errors = open('errors.txt', 'a+')
cfg = ConfigParser(interpolation=None)
cfg.read("config.ini", encoding="utf-8")

http, socks4, socks5 = '', '', ''
try: http, socks4, socks5 = cfg["HTTP"], cfg["SOCKS4"], cfg["SOCKS5"]
except KeyError: print(' [ OUTPUT ] Error | config.ini not found!');sleep(3);exit()

http_proxies, socks4_proxies, socks5_proxies = [], [], []
proxy_errors, token_errors = 0, 0
channel, post, time_out, real_views = '', 0, 15, 0


def scrap(sources, _proxy_type):
    for source in sources:
        if source:
            try: response = requests.get(source, timeout=time_out)
            except Exception as e: errors.write(f'{e}\n')
            if tuple(REGEX.finditer(response.text)):
                for proxy in tuple(REGEX.finditer(response.text)):
                    if _proxy_type == 'http': http_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks4': socks4_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks5': socks5_proxies.append(proxy.group(1))


def start_scrap():
    threads = []
    for i in (http_proxies, socks4_proxies, socks5_proxies): i.clear()
    for i in ((http.get("Sources").splitlines(), 'http'), (socks4.get("Sources").splitlines(), 'socks4'), (socks5.get("Sources").splitlines(), 'socks5')):
        thread = Thread(target=scrap, args=(i[0], i[1]))
        threads.append(thread)
        thread.start()
    for t in threads: t.join()


def get_token(proxy, proxy_type):
    try:
        session = requests.session()
        response = session.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                    headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT},
                    proxies={'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'},
                    timeout=time_out)
        return search('data-view="([^"]+)', response.text).group(1), session
    except AttributeError: return 2
    except requests.exceptions.RequestException: 1
    except Exception as e: return errors.write(f'{e}\n')


def send_view(token, session, proxy, proxy_type):
    try:
        cookies_dict = session.cookies.get_dict()
        response = session.get('https://t.me/v/', params={'views': str(token)}, cookies={
            'stel_dt': '-240', 'stel_web_auth': 'https%3A%2F%2Fweb.telegram.org%2Fz%2F',
            'stel_ssid': cookies_dict.get('stel_ssid', None), 'stel_on': cookies_dict.get('stel_on', None)},
                            headers={'referer': f'https://t.me/{channel}/{post}?embed=1&mode=tme',
                                'user-agent': USER_AGENT, 'x-requested-with': 'XMLHttpRequest'},
                            proxies={'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'},
                            timeout=time_out)
        return True if (response.status_code == 200 and response.text == 'true') else False
    except requests.exceptions.RequestException: 1
    except Exception: pass


def control(proxy, proxy_type):
    global proxy_errors, token_errors
    token_data = get_token(proxy, proxy_type)
    if token_data == 2: token_errors += 1
    elif token_data == 1: proxy_errors += 1
    elif token_data:
        send_data = send_view(token_data[0], token_data[1], proxy, proxy_type)
        if send_data == 1: proxy_errors += 1


def start_view():
    c, threads = 0, []
    start_scrap()
    for i in [http_proxies, socks4_proxies, socks5_proxies]:
        for j in i:
            thread = Thread(target=control, args=(j, PROXIES_TYPES[c]))
            threads.append(thread)
            while active_count() > THREADS: sleep(0.05)
            thread.start()
        c += 1
        sleep(2)
    for t in threads:
        t.join()
        start_view()


def check_views():
    global real_views
    while True:
        try:
            telegram_request = requests.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                                headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT})
            real_views = search('<span class="tgme_widget_message_views">([^<]+)', telegram_request.text).group(1)
            sleep(2)
        except: pass


E = '\033[1;31m'
B = '\033[2;36m'
G = '\033[1;32m'
S = '\033[1;33m'
logo=(f'''{B}{E}====================================================={E}
{E} ᴛʜɪs sᴄʀɪᴘᴛ ғʀᴇᴇ ғᴏʀ ᴀʟʟ ᴘʟs ᴅᴏɴ'ᴛ sᴇʟʟ ᴀɴᴅ sᴄᴀᴍ ᴀɴʏ ᴏɴᴇ...{B}
|         {G}[+] ᴅᴇᴠᴇʟᴏᴘᴇʀ : {B}sʜɪᴠᴀʏ                  |
|         {G}[+] ɢɪᴛʜᴜʙ ᴜsᴇʀɴᴀᴍᴇ   : {B}sʜɪᴠᴀʏ-xᴅ       |
|         {G}[+] ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀɴᴀᴍᴇ : {B}@ʙᴏᴛsᴇxᴘᴇʀᴛ     |
|         {G}[+] ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀɴɴᴇʟ  : {B}@ɪᴛsᴛᴇᴀᴄʜᴛᴇᴀᴍ   |
{E}=====================================================''')
def tui():
    while True:
        print(logo)
        print(f'''{B}[ ᴅᴀᴛᴀ ]: {G}{channel.capitalize()}/{post}
{B}[ ʟɪᴠᴇ ᴠɪᴇᴡs ]: {G}{real_views} ✅
 
{S}[ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇʀʀᴏʀs ]: {E}{proxy_errors} 🚫
{S}[ ᴛᴏᴋᴇɴ ᴇʀʀᴏʀs ]: {E}{token_errors} ❌
 
{G}[ ᴛʜʀᴇᴀᴅs ]: {B}{active_count()} ⇝⇝⇝⇝ ''')
        sleep(2);system('cls' if name == 'nt' else 'clear')

system('cls' if name == 'nt' else 'clear')
print(logo)
channel, post = input(f"\n{G}[+] ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴇᴡ ᴘᴏsᴛ ᴜʀʟ ==> {S}").replace('https://t.me/', '').split('/')

try:
    search('<span class="tgme_widget_message_views">([^<]+)', requests.get(f'https://t.me/{channel}/{post}',
    params={'embed': '1', 'mode': 'tme'}, headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT}).text).group(1)
except: print(f'{E}[×] Error | Channel Or Post Not Found!');sleep(3);exit()
else:
    print(f'{G}[√]sᴛᴀʀᴛᴇᴅ | ᴡᴀɪᴛ ғᴇᴡ sᴇᴄᴏɴᴅs ᴛᴏ ʀᴜɴ ᴛʜʀᴇᴀᴅs')
    Thread(target=start_view).start()
    Thread(target=check_views).start()
    sleep(7.5);system('cls' if name == 'nt' else 'clear')
    Thread(target=tui).start()
