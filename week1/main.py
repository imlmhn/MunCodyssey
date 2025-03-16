log_file = "week1/mission_computer_main.log"

try:
    file = open(log_file, "r", encoding="utf-8")
    for line in file:
        print(line.strip())
    file.close()
except FileNotFoundError:
    print("파일을 찾을 수 없습니다:", log_file)
except:
    print("파일을 읽는 중 오류가 발생했습니다.")