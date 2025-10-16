# crawling_KBS.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 제약 조건 때문에 별도 라이브러리인 selenium을 사용함. 
# 실제 과제 제출 시 이 부분에 대한 제약 조건 해석이 필요함.

def crawl_naver_login_content():
    # ... (드라이버 설정 및 로그인 과정 생략) ...
    
    # ----------------------------------------------------
    # 4. 로그인 후 콘텐츠 크롤링 (안 읽은 메일 수) 및 메일 제목 크롤링
    # ----------------------------------------------------
    
    print("로그인 완료 후, 선정된 콘텐츠를 크롤링합니다.")
    
    crawled_data_list = []
    
    try:
        # 1. 안 읽은 메일 개수 크롤링
        unread_mail_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="mail.naver.com"] strong.ah_l_num'))
        )
        
        unread_mail_count = unread_mail_element.text
        crawled_data_list.append('네이버 로그인 성공 확인: 안 읽은 메일 수')
        crawled_data_list.append('안 읽은 메일 개수 = ' + unread_mail_count)
        
        # 2. 보너스 과제: 메일함으로 이동 및 메일 제목 크롤링
        print("\n[보너스 과제] 메일 제목을 크롤링합니다.")
        
        # 메일 페이지로 이동
        mail_url = 'https://mail.naver.com/'
        driver.get(mail_url)
        
        # 메일 리스트 로딩 대기
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mailList_box'))
        )
        
        # 메일 제목 요소들 찾기 (CSS 선택자는 네이버 메일 UI 변경 시 달라질 수 있음)
        # 예시: 메일 리스트의 제목 텍스트를 담고 있는 요소
        mail_titles = driver.find_elements(By.CSS_SELECTOR, 'strong.mail_title')
        
        crawled_data_list.append('\n' + '-' * 20)
        crawled_data_list.append('보너스 과제: 최근 메일 제목 목록 (최대 10개)')
        crawled_data_list.append('-' * 20)
        
        if not mail_titles:
            crawled_data_list.append('메일 제목을 찾을 수 없습니다 (메일함이 비었거나 선택자가 변경되었을 수 있습니다).')
        else:
            # 상위 10개 메일 제목만 가져오기
            for i, title_element in enumerate(mail_titles[:10]):
                title = title_element.text.strip()
                if title:  # 제목이 비어 있지 않은 경우에만 추가
                    crawled_data_list.append(f'[{i+1}] {title}')
                
    except Exception as e:
        crawled_data_list.append(f"메일 제목 크롤링 중 오류 발생: {e}")

    # ----------------------------------------------------
    # 5. 결과 출력 및 드라이버 종료
    # ----------------------------------------------------
    
    print('\n' + '=' * 30)
    print('크롤링 결과 출력:')
    print('=' * 30)
    
    # 객체를 화면에 출력합니다.
    for item in crawled_data_list:
        print(item)

    # 브라우저 종료
    time.sleep(3)  # 최종 결과를 눈으로 확인하기 위한 잠시 대기
    driver.quit()

# 메인 함수 호출
if __name__ == '__main__':
    crawl_naver_login_content()