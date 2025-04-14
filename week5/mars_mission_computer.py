from week3.mars_mission_computer import DummySensor
import time
import json
import platform
import psutil

# 평균 계산 간격 변수(*5초)
# 5분 60(300초) 설정
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
            # 인스턴스에 값 할당
            ds.set_env()
            
            # 할당한 값을 그대로 받아옴
            self.env_values = ds.env_values
            
            # 받아온 값 출력
            self.print_env_values()
            
            # 받아온 값을 저장 변수에 저장
            for key in self.env_values:
                self.data_history[key].append(self.env_values[key])
                if len(self.data_history[key]) > AVERAGE_INTERVAL: 
                    self.data_history[key].pop(0)

            # AVERAGE_INTERVAL 간격마다 평균값 출력
            count += 1
            if count % AVERAGE_INTERVAL == 0:
                self.compute_5min_average()
                
            # 5초 휴식
            time.sleep(5)
            
    # 종료 함수
    def stop(self):
        self.running = False
        
    def get_mission_computer_info(self):
        info = {
            "운영체계": platform.system(),
            "운영체계_버전": platform.version(),
            "CPU_타입": platform.processor(),
            "CPU_코어_수": psutil.cpu_count(logical=True),
            "메모리_크기(GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
        }

        print("=== 미션 컴퓨터 시스템 정보 ===")
        print(json.dumps(info, indent=4, ensure_ascii=False))
        return info

    def get_mission_computer_load(self):
        load = {
            "CPU_실시간_사용량(%)": psutil.cpu_percent(interval=1),
            "메모리_실시간_사용량(%)": psutil.virtual_memory().percent
        }

        print("=== 미션 컴퓨터 부하 정보 ===")
        print(json.dumps(load, indent=4, ensure_ascii=False))
        return load    

RunComputer = MissionComputer()

RunComputer.get_mission_computer_info()
RunComputer.get_mission_computer_load()