def caesar_cipher_decode(target_text):
    """
    Caesar cipher 복호화 함수.
    알파벳 시프트를 1~25까지 변화시키며 결과를 출력한다.
    """
    print('--- Caesar Cipher Decode Start ---')
    decoded_list = []

    for shift in range(1, 26):
        decoded = ''
        for char in target_text:
            if 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            elif 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decoded += char

        print(f'Shift {shift:2}: {decoded}')
        decoded_list.append(decoded)

        # 보너스: 키워드 자동 탐지로 조기 중단
        keywords = ['password', 'open', 'key', 'unlock', 'emergency', 'door']
        for keyword in keywords:
            if keyword.lower() in decoded.lower():
                print(f'\n🔍 Found keyword "{keyword}" at shift {shift}. Stopping early.')
                save_result(decoded)
                return

    # 사용자가 직접 shift를 입력하여 저장할 수 있도록
    try:
        user_shift = int(input('\n🔢 저장하고 싶은 Shift 값을 입력하세요 (1-25): '))
        if 1 <= user_shift <= 25:
            save_result(decoded_list[user_shift - 1])
        else:
            print('❌ 유효하지 않은 shift 값입니다. 저장하지 않습니다.')
    except ValueError:
        print('❌ 숫자가 아닌 값이 입력되었습니다. 저장하지 않습니다.')


def save_result(decoded_text):
    """
    결과를 result.txt에 저장하는 함수
    """
    try:
        with open('week9/result.txt', 'w', encoding='utf-8') as result_file:
            result_file.write(decoded_text)
        print('✅ result.txt에 저장 완료')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')


def read_password_file(file_path):
    """
    password.txt 파일을 읽는 함수 (예외처리 포함)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print('❌ password.txt 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'파일 읽기 오류: {e}')
    return ''


def main():
    target_text = read_password_file('week9/password.txt')
    if target_text:
        caesar_cipher_decode(target_text)


if __name__ == '__main__':
    main()
