try:
    # 파일을 읽기 모드로 열기
    with open("week1/mission_computer_main.log", 'r', encoding='utf-8') as r:
        # 데이터프레임 생성
        data = r.read()

    # Markdown 형식으로 변환하는 함수
    def format_markdown(data):
        try:
            lines = data.strip().split("\n")
            headers = lines[0].split(",")
            data_rows = [line.split(",") for line in lines[1:]]

            # 각 열의 최대 길이를 계산
            col_widths = [max(len(headers[i]), max(len(row[i]) for row in data_rows)) for i in range(len(headers))]

            # 헤더를 가운데 정렬
            headers = [headers[i].ljust(col_widths[i]) for i in range(len(headers))]
            # 데이터 행의 각 항목을 왼쪽 정렬
            for row in data_rows:
                for i in range(len(row)):
                    row[i] = row[i].ljust(col_widths[i])

            # Markdown 출력 생성
            md_output = "\n| " + " | ".join(headers) + " |\n"
            md_output += "|" + "|".join("-" * (w + 2) for w in col_widths) + "|\n"
            md_output += "".join(f"| {' | '.join(row)} |\n" for row in data_rows)

            return md_output
        except Exception as e:
            raise ValueError(f"Markdown 포맷 생성 중 오류가 발생했습니다: {e}")

    # 데이터를 Markdown 형식으로 변환
    formatted_data = format_markdown(data)

    # 결과를 "mission_log.md" 파일로 저장
    with open("week1/mission_log.md", 'w', encoding='utf-8') as md_file:
        md_file.write(formatted_data)

    print("Markdown 파일이 성공적으로 저장되었습니다.\n")
    print(formatted_data)

except FileNotFoundError:
    print("로그 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
except Exception as e:
    print(f"예외가 발생했습니다: {e}")
