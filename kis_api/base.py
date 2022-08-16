import json

import requests

from kis_api.utils import IllegalArgumentError, APIServerError


class ApiToken:
    def __init__(self, access_token, token_type, expires_in):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        pass


class KISApi:
    """
    무한루프 코딩 모임에서 사이드 프로젝트로 진행 중

    Parameters
    ----------
    appkey: 한국투자증권에서 발급한 API Key
    appsecret: 한국투자증권에서 발급한 API Secret Key
    base_url: 한국투자증권 API 주소
              실전투자 : 기본 값 (https://openapi.koreainvestment.com:9443)
              모의투자 : https://openapivts.koreainvestment.com:29443

    Examples
    --------
    >>> from kis_api.base import KISApi
    >>> api = KISApi(appkey="발급받은 App Key", appsecret="발급받은 App Secret Key")
    >>> api.login()
    >>> api.get_domestic_inquire_balance('XXXXXXXX-XX')
    >>> api.logout()
    """

    API = "https://openapi.koreainvestment.com:9443"
    API_VRT = "https://openapivrt.koreainvestment.com:29443"

    def __init__(self, appkey, appsecret, base_url=API):
        self.__APP_KEY = appkey
        self.__APP_SECRET = appsecret
        self.__BASE_URL = self.__check_url__(base_url)
        self.__API_TOKEN = None
        pass

    def login(self):
        self.__check_vrt__()

        URL = "/oauth2/tokenP"
        TARGET = f"{self.__BASE_URL}{URL}"

        response = requests.post(url=TARGET, headers={
            "content-type": "application/json"
        }, data=json.dumps({
            "grant_type": "client_credentials",
            "appkey": str(self.__APP_KEY),
            "appsecret": str(self.__APP_SECRET)
        }))

        if response.status_code == 200:
            response = json.loads(response.text)
            self.__API_TOKEN = ApiToken(response['access_token'], response['token_type'], response['expires_in'])
            print('로그인에 성공 했습니다.')
        else:
            raise APIServerError(response)

    def logout(self):
        self.__check_vrt__()
        self.__check_token__()

        URL = "/oauth2/revokeP"
        TARGET = f"{self.__BASE_URL}{URL}"

        response = requests.post(url=TARGET, headers={
            "content-type": "application/json"
        }, data=json.dumps({
            "appkey": str(self.__APP_KEY),
            "appsecret": str(self.__APP_SECRET),
            "token": self.__API_TOKEN.access_token
        }))

        if response.status_code == 200:
            self.__API_TOKEN = None
            print('성공적으로 로그아웃 했습니다.')
        else:
            raise APIServerError(response)

    def get_domestic_inquire_balance(self, account_no):
        self.__check_token__()

        URL = "/uapi/domestic-stock/v1/trading/inquire-balance"
        TARGET = f"{self.__BASE_URL}{URL}"

        headers = {
            'content-type': 'application/json; charset=utf-8',
            'authorization': f"{self.__API_TOKEN.token_type} {self.__API_TOKEN.access_token}",
            'appkey': self.__APP_KEY,
            'appsecret': self.__APP_SECRET,
            'tr_id': 'VTTC8434R' if self.__is_vrt__() else 'TTTC8434R',
            'tr_cont': '',
        }

        query = {
            'CANO': str(account_no.split('-')[0]),
            'ACNT_PRDT_CD': str(account_no.split('-')[1]),
            'AFHR_FLPR_YN': 'N',
            'OFL_YN': '',
            'INQR_DVSN': '02',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '00',
            'CTX_AREA_FK100': '',
            'CTX_AREA_NK100': ''
        }

        response = requests.get(url=TARGET, headers=headers, params=query)

        if response.status_code == 200:
            response = json.loads(response.text)
            print(f"예수금총금액: {format(int(response['output2'][0]['dnca_tot_amt']), ',d')}")
            print(f"익일정산금액: {format(int(response['output2'][0]['nxdy_excc_amt']), ',d')}")
            print(f"전일매수금액: {format(int(response['output2'][0]['bfdy_buy_amt']), ',d')}")
            print(f"전일매도금액: {format(int(response['output2'][0]['bfdy_sll_amt']), ',d')}")
            print(f"금일매수금액: {format(int(response['output2'][0]['thdt_buy_amt']), ',d')}")
            print(f"금일매도금액: {format(int(response['output2'][0]['thdt_sll_amt']), ',d')}")
            print(f"총평가금액: {format(int(response['output2'][0]['tot_evlu_amt']), ',d')}")
            print(f"순자산금액: {format(int(response['output2'][0]['nass_amt']), ',d')}")
        else:
            raise APIServerError(response)

    def __get_hash_key__(self, data):
        self.__check_vrt__()

        URL = "/uapi/hashkey"
        TARGET = f"{self.__BASE_URL}{URL}"

        response = requests.post(url=TARGET, headers={
            'content-type': 'application/json;charset=utf-8',
            'appkey': self.__APP_KEY,
            'appsecret': self.__APP_SECRET
        }, data=json.dumps(data))

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise APIServerError(response)

    def __check_url__(self, url):
        if url == self.API:
            return url
        elif url == self.API_VRT:
            return url
        else:
            raise IllegalArgumentError('Not Supported URL')

    def __is_vrt__(self):
        return self.__BASE_URL == self.API_VRT

    def __check_vrt__(self):
        if self.__BASE_URL == self.API_VRT:
            raise IllegalArgumentError('Not Supported Mode on VRT')

    def __check_token__(self):
        if self.__API_TOKEN is None:
            raise IllegalArgumentError("You must be login to KIS Server")
