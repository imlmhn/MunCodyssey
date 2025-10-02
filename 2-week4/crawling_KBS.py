import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 사용자 설정 ---
NAVER_ID = 'YOUR_ID'
NAVER_PW = 'YOUR_PASSWORD'
# ------------------

def get_naver_info():
    """
    셀레니움을 사용하여 네이버에 로그인하고, 계정 정보와
    메일 제목 리스트를 가져옵니다.
    
    Returns:
        dict: {'account': [...], 'mail_subjects': [...]} 형태의 딕셔너리.
              실패 시 빈 딕셔너리를 반환합니다.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    
    final_result = {}

    try:
        # 1. 네이버 로그인
        print('네이버 로그인 페이지에 접속합니다.')
        driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com')
        input_id = wait.until(EC.presence_of_element_located((By.ID, 'id')))
        input_id.click()
        pyperclip.copy(NAVER_ID)
        input_id.send_keys('\ue009', 'v')
        time.sleep(1)
        input_pw = driver.find_element(By.ID, 'pw')
        input_pw.click()
        pyperclip.copy(NAVER_PW)
        input_pw.send_keys('\ue009', 'v')
        time.sleep(1)
        driver.find_element(By.ID, 'log.login').click()
        print('로그인을 시도합니다.')
        
        # 2. 계정 정보 가져오기 (이전과 동일)
        print('로그인 후 계정 정보를 가져옵니다...')
        account_area = wait.until(EC.presence_of_element_located((By.ID, 'account')))
        user_info_div = account_area.find_element(By.CSS_SELECTOR, 'div[class*="MyView-module__info_user"]')
        account_info_list = user_info_div.text.split('\n')
        final_result['account'] = account_info_list
        print('계정 정보 추출 완료.')

        # 3. 네이버 메일 페이지로 이동
        print('\n네이버 메일 페이지로 이동합니다...')
        driver.get('https://mail.naver.com/')

        # 4. 메일 목록이 나타날 때까지 대기
        mail_list_ul = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.mail_list.font_small')))
        print('메일 리스트 로딩 완료. 메일 제목을 가져옵니다.')

        # 5. 메일 목록(ul) 하위의 모든 li 요소를 찾음
        mail_items = mail_list_ul.find_elements(By.TAG_NAME, 'li')
        
        mail_subjects_list = []
        # 6. 각 li 요소를 순회하며 내부의 span.text (메일 제목)만 추출
        for item in mail_items:
            try:
                # 각 li 요소 내에서 'span' 태그이면서 class가 'text'인 요소를 찾습니다.
                subject_element = item.find_element(By.CSS_SELECTOR, 'span.text')
                mail_subjects_list.append(subject_element.text)
            except NoSuchElementException:
                # 간혹 광고 등 다른 구조의 li가 있을 수 있어 예외 처리
                # 제목(span.text)이 없는 항목은 건너뜁니다.
                pass

        final_result['mail_subjects'] = mail_subjects_list
        print('메일 제목 추출 완료.')

        return final_result

    except Exception as e:
        print(f'오류가 발생했습니다: {e}')
        return {}
    finally:
        print('\n크롤링이 완료되었습니다. 브라우저를 수동으로 닫아주세요.')
        # driver.quit()

if __name__ == '__main__':
    naver_info = get_naver_info()
    
    if naver_info:
        # 계정 정보 출력 (이전과 동일)
        if 'account' in naver_info:
            print('\n--- 최종 크롤링 결과 (계정 정보) ---')
            for text_line in naver_info['account']:
                print(text_line)
        
        # 메일 제목 리스트 출력 (요청하신 형식으로 변경)
        if 'mail_subjects' in naver_info and naver_info['mail_subjects']:
            print('\n--- 최종 크롤링 결과 (메일 제목) ---')
            for index, subject in enumerate(naver_info['mail_subjects'], 1):
                print(f"{index}번째 메일 제목 : {subject}")
    else:
        print('\n콘텐츠를 가져오는데 실패했습니다.')