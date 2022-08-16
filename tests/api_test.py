import os

from kis_api.base import KISApi


def run_test():
    appkey = os.environ['APP_KEY']
    appsecret = os.environ['APP_SECRET']
    account_no = os.environ['ACCOUNT_NO']

    api = KISApi(appkey, appsecret)
    api.login()
    api.get_domestic_inquire_balance(account_no)
    api.logout()


if __name__ == '__main__':
    run_test()
