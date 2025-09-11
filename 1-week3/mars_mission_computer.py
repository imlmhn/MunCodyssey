import datetime
import random

def is_float(value):
    # 실수인지 확인
    if isinstance(value, float):
        # 소수점이 있을 경우에만 자릿수 계산
        value_str = str(value)
        if '.' in value_str:
            return value_str.split(".")[1] != '0'
        
    return False  # 실수가 아니거나 소수점 이하 자릿수가 없는 경우

def get_random_with_step(start, end, step=1):
    
    # start가 end보다 크거나, step이 1이 아니면서 end를 초과하면 error 반환
    if((start > end) or (step!=1 and end<step)):
        return "Error"
    
    # start가 실수이고, step이 default(1)일 때
    if(is_float(start) and start < step):
        start_precision = len(str(start).split(".")[1])
        while(start_precision>0):
            start_precision -= 1
            step /= 10
    
    # 자릿수 저장 변수
    multiple = 1

    # start, end, step 중 실수가 안나올 때까지 자릿수와 함께 10을 곱함
    while(is_float(start) or is_float(end) or is_float(step)):
        start *= 10
        end *= 10
        step *= 10
        multiple *= 10
    
    # 정수 random 범위 반환
    result = random.randrange(int(start), int(end), int(step))
    
    # 반환된 값을 다시 자릿수로 나누어 리턴
    return result/multiple
    
class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }
            
    def set_env(self):
        # 3번째 step 인자를 주지 않으면, start의 자리수에 맞게 1단위로 step 설정
        self.env_values["mars_base_internal_temperature"] = get_random_with_step(18, 30)
        self.env_values["mars_base_external_temperature"] = get_random_with_step(0, 21)
        self.env_values["mars_base_internal_humidity"] = get_random_with_step(50, 60)
        self.env_values["mars_base_external_illuminance"] = get_random_with_step(500, 715)
        self.env_values["mars_base_internal_co2"] = get_random_with_step(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = get_random_with_step(4, 7)
            
    def get_env(self): 
        log_file = "week3/mission_computer_main"
        
        # 현재 날짜와 시간 가져오기
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 한글화된 환경 변수
        env_in_korean = {
            "mars_base_internal_temperature": "화성 기지 내부 온도",
            "mars_base_external_temperature": "화성 기지 외부 온도",
            "mars_base_internal_humidity": "화성 기지 내부 습도",
            "mars_base_external_illuminance": "화성 기지 외부 조도",
            "mars_base_internal_co2": "화성 기지 내부 CO2 농도",
            "mars_base_internal_oxygen": "화성 기지 내부 산소 농도"
        }
        
        # 마크다운 형식으로 기록할 내용 생성
        log_content = f"현재 날짜 : {current_time}\n\n"
        for key, value in self.env_values.items():
            korean_key = env_in_korean.get(key, key)  # 키를 한글로 변환
            log_content += f"{korean_key} : {value}\n"
        
        # 로그 파일에 기록
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_content + "\n\n")
                
        return self.env_values

    
# 인스턴스 생성
ds = DummySensor()

# 난수 생성 및 할당
ds.set_env()

# env_values 받아와 변수에 저장
result = ds.get_env()

# # 딕셔너리 형태로 출력
# for key, value in result.items():
#     print(f"{key} : {value}")