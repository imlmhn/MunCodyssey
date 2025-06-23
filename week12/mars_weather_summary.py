import csv
import mysql.connector
from datetime import datetime

class MySQLHelper:
    """MySQL 데이터베이스 연결 및 쿼리를 관리하는 헬퍼 클래스."""
    
    def __init__(self, host, user, password, database):
        """데이터베이스 연결 초기화."""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        """쿼리 실행."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f'쿼리 실행 오류: {e}')
            raise

    def fetch_query(self, query, params=None):
        """쿼리 결과 조회."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f'쿼리 조회 오류: {e}')
            return []

    def close_connection(self):
        """연결 종료."""
        self.cursor.close()
        self.connection.close()

def read_csv_file(file_path):
    """CSV 파일을 읽고 데이터를 반환."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # mars_date를 datetime 객체로 변환 (YYYY-MM-DD)
                row['mars_date'] = datetime.strptime(row['mars_date'], '%Y-%m-%d')
                # temp를 부동소수점으로 변환
                row['temp'] = float(row['temp'])
                # storm을 정수로 변환 (CSV 헤더는 'stom')
                row['storm'] = int(row['stom'])
                data.append(row)
        return data
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {file_path}')
        return []
    except Exception as e:
        print(f'CSV 파일 읽기 오류: {e}')
        return []

def insert_weather_data(db_helper, data):
    """CSV 데이터를 mars_weather 테이블에 삽입."""
    insert_query = """
        INSERT INTO mars_weather (mars_date, temp, storm)
        VALUES (%s, %s, %s)
    """
    for row in data:
        params = (row['mars_date'], row['temp'], row['storm'])
        try:
            db_helper.execute_query(insert_query, params)
            print(f'데이터 삽입 완료: {row["mars_date"]}')
        except mysql.connector.Error as e:
            print(f'데이터 삽입 오류: {e}')

def main():
    """프로그램의 메인 함수."""
    # MySQL 연결 설정 (사용자 환경에 맞게 수정)
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '12345678',
        'database': 'mars_mission'
    }
    
    # CSV 파일 경로
    csv_file_path = 'week12/mars_weathers_data.csv'
    
    try:
        # MySQLHelper 인스턴스 생성
        db_helper = MySQLHelper(**db_config)
        
        # CSV 파일 읽기
        weather_data = read_csv_file(csv_file_path)
        if not weather_data:
            print('처리할 데이터가 없습니다.')
            return
        
        # 데이터 출력 (확인용)
        print('\nCSV 파일 내용:')
        for row in weather_data:
            print(f"날짜: {row['mars_date']}, 온도: {row['temp']}, 폭풍: {row['storm']}")
        
        # 데이터 삽입
        insert_weather_data(db_helper, weather_data)
        
        # 삽입된 데이터 확인
        print('\nmars_weather 테이블 내용:')
        select_query = 'SELECT * FROM mars_weather'
        results = db_helper.fetch_query(select_query)
        for row in results:
            print(f'ID: {row[0]}, 날짜: {row[1]}, 온도: {row[2]}, 폭풍: {row[3]}')
        
    except mysql.connector.Error as e:
        print(f'MySQL 연결 오류: {e}')
    except Exception as e:
        print(f'프로그램 실행 오류: {e}')
    finally:
        if 'db_helper' in locals():
            db_helper.close_connection()
            print('데이터베이스 연결 종료.')

if __name__ == '__main__':
    main()