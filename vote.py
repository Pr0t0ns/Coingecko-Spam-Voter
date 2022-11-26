import requests, json 
from random_user_agent.user_agent import UserAgent
class Coingecko:
    def __init__(self, token_id: int, vote_type: str="positive", proxy=None) -> None:
        self.session = requests.Session()
        self.proxy = proxy
        self.vote_type = vote_type
        self.token_id = token_id
        self.vote_url = 'https://www.coingecko.com/en/sentiment_votes?' # putting the self to use xd
        self.useragent = UserAgent()
        self.ua = self.useragent.get_random_user_agent() # there we go
        self.csrf_url = 'https://www.coingecko.com/accounts/csrf_meta.json'
        if self.proxy != None: self.session.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}
    def __cf_bm(self):
        try:
            data = self.session.get('https://static.coingecko.com/webfonts/fa-regular-400.woff2')
        except Exception:
            return print(f"[-]: Error Voting {self.vote_type}!")
        return self.session.cookies.get_dict().get('__cf_bm')
    def fetch_csrf(self, cf_bm):
        headers = { # Making votes seem as legitamate as possible
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cookie": f"__cf_bm={cf_bm}",
            "referer": "https://www.coingecko.com/en/coins/paradox-metaverse",
            "user-agent": self.ua 
        } 
        try:
            csrf = self.session.get(self.csrf_url, headers=headers)
        except Exception:
            return print(f"[-]: Error Voting {self.vote_type}!")
        csrf_token =csrf.json()['token']
        session_id = self.session.cookies.get_dict().get('_session_id')
        return csrf_token, session_id
    def spam_votes(self, csrf, cf_bm_cookie, session_cookie):
        headers = {
            "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br", # found the cookie
            "accept-language": "en-US,en;q=0.9", # ok edge still has them we will see if we need them 
            "cookie":f"__cf_bm={cf_bm_cookie}; datadome=4YIc~SCOARA4tqV4_8MkLVOTkv_mZ1RQmBvjssKDCO~JNYqOdwZ2Y-zkkNk-wDigSBDS7Z8K3C1Bk0NYOjJxIaaceinGmJbuo6dpVMRrCNFnpSSltpF3OKc6XsnE0Xqt; _session_id={session_cookie};",
            "origin": "https://www.coingecko.com",
            "referer": "https://www.coingecko.com/en/coins",
            "user-agent": self.ua,
            "x-csrf-token": csrf,
            "x-requested-with": "XMLHttpRequest"
        }
        url = f'{self.vote_url}coin_id={self.token_id}&sentiment={self.vote_type}'
        try:
            data = self.session.post(url, headers=headers)
        except Exception:
            return print(f"[-]: Error Voting {self.vote_type}!")
        if data.ok:
            return print(f"[+]: Successfully voted {self.vote_type} for {self.token_id}")

        else:
            return print(f"[-]: Error Voting {self.vote_type}!")
    def vote(self):
        cf_bm_cookie = self.__cf_bm()
        csrf, session = self.fetch_csrf(cf_bm_cookie)
        self.spam_votes(csrf, cf_bm_cookie, session)
        return self.vote()
