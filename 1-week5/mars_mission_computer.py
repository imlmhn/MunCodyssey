import json
import platform
import psutil

class MissionComputer:

    def load_settings(self):
        try:
            with open("week5/setting.txt", "r", encoding="utf-8") as f:
                settings = [line.strip() for line in f if line.strip()]
            return settings
        except FileNotFoundError:
            print("⚠️ 설정 파일(setting.txt)을 찾을 수 없습니다. 모든 항목을 출력합니다.")
            return None  # 파일 없으면 전체 출력 허용
        
    def get_mission_computer_info(self):
            settings = self.load_settings()

            full_info = {
                "운영체계": platform.system(),
                "운영체계_버전": platform.version(),
                "CPU_타입": platform.processor(),
                "CPU_코어_수": psutil.cpu_count(logical=True),
                "메모리_크기(GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            info = {key: value for key, value in full_info.items() if settings is None or key in settings}
        
            print("=== 미션 컴퓨터 시스템 정보 ===")
            if info == {}:
                print("해당 부분은 setting.txt에서 비어있습니다.")
                return  # 아무것도 출력하지 않음
            
            print(json.dumps(info, indent=4, ensure_ascii=False))
            return info

    def get_mission_computer_load(self):
        settings = self.load_settings()
        full_load = {
            "CPU_실시간_사용량(%)": psutil.cpu_percent(interval=1),
            "메모리_실시간_사용량(%)": psutil.virtual_memory().percent
        }

        load = {key: value for key, value in full_load.items() if settings is None or key in settings}
        
        print("=== 미션 컴퓨터 부하 정보 ===")
        if load == {}:
            print("해당 부분은 setting.txt에서 비어있습니다.")
            return  # 아무것도 출력하지 않음
        print(json.dumps(load, indent=4, ensure_ascii=False))
        return load

RunComputer = MissionComputer()

RunComputer.get_mission_computer_info()
RunComputer.get_mission_computer_load()