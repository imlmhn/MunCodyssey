# crawling_KBS.py

import requests
from bs4 import BeautifulSoup

def get_kbs_headlines():
    """
    KBS 뉴스의 실제 콘텐츠 URL에 직접 접속하여 헤드라인 뉴스를 크롤링합니다.

    Returns:
        list: 헤드라인 뉴스 제목들이 담긴 리스트.
              오류 발생 시 빈 리스트를 반환합니다.
    """
    # JavaScript 리다이렉션을 우회하기 위해 실제 콘텐츠가 있는 URL을 직접 지정
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    headline_list = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # 실제 콘텐츠 페이지의 구조에 맞춰 헤드라인 요소를 찾습니다.
        # 'div.main-news-wrapper'와 'div.small-sub-news-wrapper' 내의 제목들을 모두 선택합니다.
        selector = '.main-news-wrapper p.title, .small-sub-news-wrapper p.title'
        headline_elements = soup.select(selector)

        if not headline_elements:
            print("오류: 헤드라인 요소를 찾지 못했습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
            return []

        for element in headline_elements:
            title = element.get_text().strip()
            if title and title not in headline_list:
                headline_list.append(title)

    except requests.exceptions.RequestException as e:
        print(f'HTTP 요청 중 오류가 발생했습니다: {e}')
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')

    return headline_list

if __name__ == '__main__':
    kbs_news_headlines = get_kbs_headlines()

    if kbs_news_headlines:
        print('--- KBS 헤드라인 뉴스 (최종 완성본) ---')
        for index, headline in enumerate(kbs_news_headlines, 1):
            print(f'{index}. {headline}')
    else:
        print('최종적으로 헤드라인 뉴스를 가져오지 못했습니다.')