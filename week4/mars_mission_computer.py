from week3.mars_mission_computer import DummySensor
import time
import threading
import json

# 평균 계산 간격(*5초)
# 임의로 3(15초) 설정
AVERAGE_INTERVAL = 3

class MissionComputer:
    def __init__(self):
        
        # 초기값 설정(Dict)
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }
        # 실행 제어 변수
        self.running = True
        
        # env_values 값 평균을 위한 저장 변수
        self.data_history = {
            key: [] for key in self.env_values
        }
        
    # 기본 출력
    def print_env_values(self):
        print(json.dumps(self.env_values, indent=2))
        
    # 각 환경값에 대한 5분 평균 값 출력
    def compute_5min_average(self):
        avg_values = {}
        for key, values in self.data_history.items():
            if values:
                avg = sum(values) / len(values)
                avg_values[key] = round(avg, 2)
        print('[5min Average]--------------------------------')
        print(json.dumps(avg_values, indent=4))
        print('----------------------------------------------')

    # 5초마다 DummySensor의 환경값 설정 및 출력
    def get_sensor_data(self, ds : DummySensor):
        # 시간 저장 변수. 1 -> 5초
        count = 0
        while self.running:
            ds.set_env()
            self.env_values = ds.env_values
            self.print_env_values()
            for key in self.env_values:
                self.data_history[key].append(self.env_values[key])
                if len(self.data_history[key]) > AVERAGE_INTERVAL: 
                    self.data_history[key].pop(0)

            time.sleep(5)
            
            count += 1
            if count % AVERAGE_INTERVAL == 0:
                self.compute_5min_average()
            
    # 종료 함수
    def stop(self):
        self.running = False

#
def listen_for_stop(computer):
    while True:
        user_input = input()
        if user_input.lower() == 's':
            computer.stop()
            print('System stopped…')
            break
    
# 인스턴스 생성
ds = DummySensor()
RunComputer = MissionComputer()

# 환경값 출력 함수 및 종료 제어 함수 각각 스레드화
thread_sensor = threading.Thread(target=RunComputer.get_sensor_data, args=(ds,))
thread_listener = threading.Thread(target=listen_for_stop, args=(RunComputer,))

# 두 스레드 시작
thread_sensor.start()
thread_listener.start()

# 두 스레드가 종료할 때까지 메인 프로그램 기다리게 함함 
thread_sensor.join()
thread_listener.join()
