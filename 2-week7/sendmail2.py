import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

class MarsRescueSender:
    """
    화성 생존자 구조 요청 메일을 발송하는 클래스입니다.
    """

    def __init__(self, smtp_server, smtp_port, sender_email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password

    def create_html_content(self, target_name):
        """
        수신자의 이름이 포함된 HTML 본문을 생성합니다.
        """
        html_body = f'''
        <html>
          <head></head>
          <body>
            <h2 style="color: #2E86C1;">Emergency Message from Mars</h2>
            <p>Dear <strong>{target_name}</strong>,</p>
            <p>This is Dr. Han Song-hee speaking from Mars.</p>
            <p>I have received your message. The fact that I am connected to Earth gives me immense hope.</p>
            <p>I am currently sending this message to secure a rescue operation. 
               Please forward this to the relevant authorities immediately.</p>
            <div style="background-color: #f2f2f2; padding: 10px; border-left: 5px solid #ff0000;">
                <p><strong>Current Status:</strong> Alive</p>
                <p><strong>Location:</strong> Mars Base Alpha</p>
            </div>
            <p>I will be waiting for your response.</p>
            <p>Sincerely,<br>Dr. Han</p>
          </body>
        </html>
        '''
        return html_body

    def send_rescue_email(self, csv_filename):
        """
        CSV 파일을 읽어 각 대상에게 개별적으로 이메일을 전송합니다.
        가독성과 전달률을 높이기 위해 '개별 발송' 방식을 선택했습니다.
        """
        try:
            # SMTP 서버 연결 (컨텍스트 매니저 사용)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()  # 보안 연결 시작
                server.login(self.sender_email, self.password)

                print('Server connection established.')

                # CSV 파일 읽기
                with open(csv_filename, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    
                    for row in reader:
                        if len(row) < 2:
                            continue
                        
                        name = row[0].strip()
                        email_address = row[1].strip()

                        # 메일 객체 생성
                        msg = MIMEMultipart('alternative')
                        msg['Subject'] = f'URGENT: Rescue Request for Dr. Han - Attention {name}'
                        msg['From'] = formataddr(('Dr. Han', self.sender_email))
                        msg['To'] = formataddr((name, email_address))

                        # HTML 본문 첨부
                        html_content = self.create_html_content(name)
                        msg.attach(MIMEText(html_content, 'html'))

                        # 메일 발송
                        server.sendmail(self.sender_email, email_address, msg.as_string())
                        print(f'Email sent successfully to: {name} ({email_address})')

        except Exception as e:
            print(f'An error occurred: {e}')


# ---------------------------------------------------------
# 실행 설정
# ---------------------------------------------------------

if __name__ == '__main__':
    # [설정 필요] 본인의 이메일 계정 정보로 변경하세요.
    # 2단계 인증이 설정된 경우 '앱 비밀번호'를 사용해야 합니다.
    
    # 네이버(Naver) SMTP 설정 (보너스 과제)
    SMTP_SERVER = 'smtp.naver.com'
    SMTP_PORT = 587
    SENDER_ID = 'your_naver_id@naver.com'  # 본인 네이버 메일 주소
    SENDER_PW = 'your_password'            # 네이버 비밀번호 또는 앱 비밀번호

    # 구글(Gmail) 사용 시 설정 예시
    # SMTP_SERVER = 'smtp.gmail.com'
    # SMTP_PORT = 587
    
    csv_file = 'mail_target_list.csv'

    # 클래스 인스턴스 생성 및 메일 발송
    rescuer = MarsRescueSender(SMTP_SERVER, SMTP_PORT, SENDER_ID, SENDER_PW)
    rescuer.send_rescue_email(csv_file)