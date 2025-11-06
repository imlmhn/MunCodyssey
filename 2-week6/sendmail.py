# sendmail.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


# SMTP 기본 정보 설정
# Gmail의 SMTP 서버와 STARTTLS를 위한 포트 587 사용
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_email():
    """
    Gmail SMTP 서버를 통해 이메일을 전송하고 예외를 처리하는 함수.
    """
    # ----------------------------------------------------
    # 1. 사용자 설정 (반드시 변경해야 합니다!)
    # ----------------------------------------------------
    sender_email = 'YOUR_GMAIL_ADDRESS@gmail.com'
    sender_password = 'YOUR_APP_PASSWORD'  # Gmail 앱 비밀번호 사용 권장
    receiver_email = 'RECEIVER_EMAIL_ADDRESS@example.com'  # 받는 사람 이메일
    
    subject = '파이썬으로 보내는 테스트 메일'
    body = '''
    이것은 파이썬 smtplib과 email 패키지를 사용하여 전송된 테스트 메시지입니다.
    지속적인 연결 테스트를 위한 자동 발송 메일입니다.
    '''
    
    # 보너스 과제: 첨부 파일 경로 설정 (경로를 변경하거나 주석 처리하세요)
    # 첨부 파일이 없으면 '' 빈 문자열로 설정하여 첨부 없이 보냅니다.
    attachment_file_path = ''  # 예시: 'document.pdf'
    # ----------------------------------------------------

    # MIMEMultipart 객체 생성 (첨부 파일을 위해)
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    
    # 2. 메일 본문 추가
    message.attach(MIMEText(body, 'plain'))

    # 3. 보너스 과제: 첨부 파일 처리
    if attachment_file_path and os.path.exists(attachment_file_path):
        try:
            attach_file_name = os.path.basename(attachment_file_path)
            
            with open(attachment_file_path, 'rb') as attachment:
                # MIMEBase 클래스는 첨부 파일의 기본 유형을 설정
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Base64로 인코딩하여 메일에 포함
            encoders.encode_base64(part)
            
            # Content-Disposition 헤더 설정 (파일 이름 지정)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{attach_file_name}"',
            )
            
            # 메시지에 첨부 파일 추가
            message.attach(part)
            print(f"INFO: '{attach_file_name}' 파일을 첨부했습니다.")
            
        except Exception as e:
            print(f"ERROR: 파일 첨부 중 오류가 발생했습니다: {e}")
            return # 첨부 오류 시 전송 중단
    
    # 4. SMTP 서버 연결 및 예외 처리
    try:
        # SMTP 서버 연결 및 STARTTLS 암호화 시작
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()  # 서버에 연결을 알림
        server.starttls()  # 암호화 시작
        server.ehlo()  # STARTTLS 시작 후 다시 알림
        
        # 로그인
        server.login(sender_email, sender_password)
        
        # 메일 전송
        server.sendmail(sender_email, receiver_email, message.as_string())
        
        print('\n-------------------------------------------------')
        print(f"SUCCESS: 메일 전송 완료!")
        print(f"보낸 사람: {sender_email}")
        print(f"받는 사람: {receiver_email}")
        print('-------------------------------------------------')
        
    # 예외 처리: 로그인 실패, 서버 연결 오류 등
    except smtplib.SMTPAuthenticationError:
        print('\n-------------------------------------------------')
        print("ERROR: SMTP 인증에 실패했습니다.")
        print("   -> 1. Gmail 주소와 비밀번호(앱 비밀번호)를 확인하세요.")
        print("   -> 2. 2단계 인증 사용자라면 반드시 '앱 비밀번호'를 사용해야 합니다.")
        print('-------------------------------------------------')
    except smtplib.SMTPConnectError as e:
        print('\n-------------------------------------------------')
        print(f"ERROR: SMTP 서버 연결에 실패했습니다: {e}")
        print("   -> 네트워크 연결 상태, 방화벽 설정을 확인하거나 포트 587을 확인하세요.")
        print('-------------------------------------------------')
    except Exception as e:
        print(f'\nERROR: 예상치 못한 오류가 발생했습니다: {e}')
    
    finally:
        # 연결이 성공적으로 이루어졌을 경우에만 닫기 시도
        if 'server' in locals() and server:
            server.quit()
            print("INFO: SMTP 연결 종료.")


if __name__ == '__main__':
    send_email()