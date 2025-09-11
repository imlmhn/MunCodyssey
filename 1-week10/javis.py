# pip install sounddevice scipy

import os
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import glob

def create_records_directory():
    """records 폴더를 생성하는 함수."""
    if not os.path.exists('week10/records'):
        os.makedirs('week10/records')

def get_current_timestamp():
    """현재 시간을 '년월일-시간분초' 형식의 문자열로 반환."""
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')

def record_audio(duration=5, sample_rate=44100):
    """지정된 시간 동안 오디오를 녹음하고 WAV 파일로 저장."""
    create_records_directory()
    timestamp = get_current_timestamp()
    file_path = f'week10/records/{timestamp}.wav'
    
    print(f'녹음 시작: {duration}초')
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # 녹음이 완료될 때까지 대기
    write(file_path, sample_rate, recording)
    print(f'녹음 완료: {file_path}에 저장됨')

def list_recordings(start_date, end_date):
    """지정된 날짜 범위 내의 녹음 파일 목록을 출력."""
    try:
        start = datetime.datetime.strptime(start_date, '%Y%m%d')
        end = datetime.datetime.strptime(end_date, '%Y%m%d')
        if start > end:
            print('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
            return
    except ValueError:
        print("날짜 형식이 잘못되었습니다. 'YYYYMMDD' 형식을 사용하세요.")
        return

    create_records_directory()
    files = glob.glob('week10/records/*.wav')
    print(f'{start_date}부터 {end_date}까지의 녹음 파일:')
    
    for file in files:
        file_name = os.path.basename(file).split('.')[0]
        try:
            file_date = datetime.datetime.strptime(file_name.split('-')[0], '%Y%m%d')
            if start <= file_date <= end:
                print(file)
        except ValueError:
            continue

def main():
    """프로그램의 메인 함수."""
    while True:
        print('\n1. 녹음 시작')
        print('2. 특정 날짜 범위의 녹음 파일 보기')
        print('3. 종료')
        choice = input('선택 (1-3): ')

        if choice == '1':
            try:
                duration = int(input('녹음 시간(초)을 입력하세요: '))
                if duration <= 0:
                    print('녹음 시간은 양수여야 합니다.')
                    continue
                record_audio(duration)
            except ValueError:
                print('유효한 숫자를 입력하세요.')
        elif choice == '2':
            start_date = input("시작 날짜(YYYYMMDD)를 입력하세요: ")
            end_date = input("종료 날짜(YYYYMMDD)를 입력하세요: ")
            list_recordings(start_date, end_date)
        elif choice == '3':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 선택입니다. 1-3 중에서 선택하세요.')

if __name__ == '__main__':
    main()