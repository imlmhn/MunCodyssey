# crawling_finance_info.py

import requests
from bs4 import BeautifulSoup

def get_usd_exchange_rate():
    """
    네이버 금융에서 현재 원/달러 환율 정보를 가져옵니다.

    Returns:
        str: 현재 환율 정보. 오류 발생 시 None을 반환합니다.
    """
    url = 'https://finance.naver.com/marketindex/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        rate_element = soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')

        if rate_element:
            return rate_element.get_text()
        else:
            return '환율 정보를 찾을 수 없습니다.'

    except requests.exceptions.RequestException as e:
        print(f'환율 정보 요청 중 오류가 발생했습니다: {e}')
        return None
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')
        return None

def get_naver_stock_price():
    """
    네이버 금융에서 NAVER 주식의 현재가를 가져옵니다.

    Returns:
        str: 현재 주가 정보. 오류 발생 시 None을 반환합니다.
    """
    # NAVER(종목코드: 035420)의 네이버 금융 페이지 URL
    url = 'https://finance.naver.com/item/main.naver?code=035420'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 현재가를 담고 있는 div.today 안의 span.blind 요소를 선택
        price_element = soup.select_one('div.today span.blind')
        
        if price_element:
            return price_element.get_text()
        else:
            return '주가 정보를 찾을 수 없습니다.'

    except requests.exceptions.RequestException as e:
        print(f'NAVER 주가 요청 중 오류가 발생했습니다: {e}')
        return None
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')
        return None

if __name__ == '__main__':
    print('-' * 40)
    # 1. 환율 정보 가져오기 및 출력
    usd_rate = get_usd_exchange_rate()
    if usd_rate:
        print(f'현재 원/달러 환율: {usd_rate} 원')
    else:
        print('환율 정보를 가져오는 데 실패했습니다.')

    # 2. NAVER 주식 가격 가져오기 및 출력
    naver_price = get_naver_stock_price()
    if naver_price:
        print(f'NAVER 현재가: {naver_price} 원')
    else:
        print('NAVER 주가 정보를 가져오는 데 실패했습니다.')
        
    print('-' * 40) 