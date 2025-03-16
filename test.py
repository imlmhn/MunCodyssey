# main.py

try:
    with open('mission_computer_main.log', 'r') as log_file:
        log_data = log_file.readlines()

        # 전체 로그 출력
        print('All Log List>>>>>')
        for line in log_data:
            print(line.strip(), '\n')

        # 에러 로그 필터링
        error_logs = [line.strip() for line in log_data if '[ERROR]' in line]

        # 에러 로그가 있는 경우만 출력
        if error_logs:
            print('\n[ERROR] Log>>>>>')
            for error in error_logs:
                print(error)

        # 보고서 작성
        with open('log_analysis.md', 'w') as report_file:
            report_file.write('# [Log Analysis Report]\n\n')
            # 에러 로그가 있을 경우만 추가
            if error_logs:
                report_file.write('\n## [ERROR] Logs\n')
                for error in error_logs:
                    report_file.write(f'- {error}\n')
            else: 
                    report_file.write(f"Can't find ERROR\n")


        print('\nlog_analysis.md report has been created.')

except FileNotFoundError:
    print('File not found.')
except Exception as e:
    print(f"except: {e}")
