log_file = "week1/mission_computer_main.log"
result_file = "week1/log_analysis.md"

try:
    result_lines = []  # 오류 로그를 저장하는 리스트
    log_lines = [] # 기존 로그를 저장하는 리스트
    
    result_lines.append("# 로그 분석 보고서\n\n")
    result_lines.append("## 사고 개요\n")
    result_lines.append("- **발생 일시:** 2023-08-27 11:35:00 ~ 11:40:00\n")
    result_lines.append("- **이벤트:** 산소 탱크 불안정 → 산소 탱크 폭발\n")
    result_lines.append("- **결과:** 로켓 회수 후 폭발 발생, 센터 및 미션 컨트롤 시스템 종료됨\n\n")
    result_lines.append("## 로그 분석\n\n")

    readFile = open(log_file, "r", encoding="utf-8")
    
    for line in readFile:
        log_lines.append(line.strip())
        if "oxygen" in line.lower(): 
            # timestamp, event, message로 분리
            parts = line.strip().split(",")
            timestamp = parts[0]
            event = parts[1]
            message = parts[2]

            # 마크다운 형식으로 변환하여 리스트에 추가
            result_lines.append(f"### {timestamp}\n**Event:** {event}\n**Message:** {message}\n")
    
    readFile.close()
    
    if result_lines:
        with open(result_file, "w", encoding="utf-8") as writeFile:
            writeFile.writelines(result_lines)  # 한 번에 저장

    # log_lines를 그대로 출력 (오름차순으로)
    for row in log_lines:
        print(row) 
        
    # log_lines를 거꾸로 출력 (내림차순으로)
    reversed_lines = list(reversed(log_lines))
    for row in reversed_lines:
        print(row)
    
    print(f"로그 분석이 완료되었습니다. 결과 파일: {result_file}")
    
    
    
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {log_file}")
except Exception as e:
    print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
