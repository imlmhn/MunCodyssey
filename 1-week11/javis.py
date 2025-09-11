# pip install sounddevice scipy speechrecognition
import os
import datetime
import glob
import csv
import numpy as np
import sounddevice as sd
import wave
import speech_recognition as sr

def create_records_directory():
    """week10/records 폴더를 생성하는 함수."""
    if not os.path.exists('week10/records'):
        os.makedirs('week10/records')

def get_current_timestamp():
    """현재 시간을 '년월일-시간분초' 형식의 문자열로 반환."""
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')

def record_audio(duration=5, sample_rate=44100):
    """지정된 시간 동안 오디오를 녹음하고 16-bit PCM WAV 파일로 저장."""
    create_records_directory()
    timestamp = get_current_timestamp()
    file_path = f'week10/records/{timestamp}.wav'
    
    print(f'녹음 시작: {duration}초')
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    
    # 16-bit PCM WAV 파일로 저장
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)  # 모노
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())
    
    print(f'녹음 완료: {file_path}에 저장됨')

def validate_wav_file(wav_file):
    """WAV 파일이 올바른 형식인지 확인."""
    try:
        with wave.open(wav_file, 'rb') as wf:
            if wf.getsampwidth() != 2 or wf.getnchannels() != 1:
                return False
            return True
    except wave.Error:
        return False

def process_speech_to_text(wav_file):
    """음성 파일에서 텍스트를 추출하고 CSV로 저장."""
    if not validate_wav_file(wav_file):
        print(f'{wav_file}: 잘못된 WAV 형식 또는 손상된 파일입니다.')
        return
    
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(wav_file)
    
    try:
        with audio_file as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ko-KR')
            duration = source.DURATION
            csv_file = wav_file.replace('.wav', '.csv')
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['time', 'text'])
                writer.writerow([f'{duration:.2f}', text])
            
            print(f'STT 완료: {csv_file}에 저장됨')
            print(f'인식된 텍스트: {text}')
    except sr.UnknownValueError:
        print(f'{wav_file}: 음성을 인식할 수 없습니다.')
    except sr.RequestError as e:
        print(f'{wav_file}: STT 요청 오류 - {e}')
    except Exception as e:
        print(f'{wav_file}: 처리 중 오류 - {e}')

def list_and_process_recordings():
    """모든 음성 파일을 불러와 STT 처리."""
    create_records_directory()
    files = glob.glob('week10/records/*.wav')
    if not files:
        print('녹음 파일이 없습니다.')
        return
    
    print('처리 중인 음성 파일:')
    for file in files:
        print(f'- {file}')
        process_speech_to_text(file)

def search_keyword_in_csv(keyword):
    """CSV 파일에서 키워드를 검색하여 결과 출력."""
    create_records_directory()
    files = glob.glob('week10/records/*.csv')
    if not files:
        print('CSV 파일이 없습니다.')
        return
    
    print(f'키워드 "{keyword}" 검색 결과:')
    found = False
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 건너뛰기
                for row in reader:
                    if len(row) >= 2 and keyword.lower() in row[1].lower():
                        print(f'{file}: 시간={row[0]}초, 텍스트={row[1]}')
                        found = True
        except Exception as e:
            print(f'{file}: 읽기 중 오류 - {e}')
    
    if not found:
        print('키워드와 일치하는 결과가 없습니다.')

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
        print('3. 음성 파일 STT 처리')
        print('4. CSV 파일에서 키워드 검색')
        print('5. 종료')
        choice = input('선택 (1-5): ')

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
            list_and_process_recordings()
        elif choice == '4':
            keyword = input('검색할 키워드를 입력하세요: ')
            search_keyword_in_csv(keyword)
        elif choice == '5':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 선택입니다. 1-5 중에서 선택하세요.')

if __name__ == '__main__':
    main()