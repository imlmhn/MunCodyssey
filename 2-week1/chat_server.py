# chat_server.py

import socket
import threading

# --- 서버 설정 ---
HOST = '127.0.0.1'  # 서버 IP 주소 (로컬호스트)
PORT = 9999         # 서버 포트 번호

# --- 전역 변수 ---
# 여러 스레드에서 공유될 클라이언트 리스트와 닉네임 리스트
clients = []
nicknames = []
# 공유 자원(clients, nicknames) 접근을 제어하기 위한 락(Lock)
client_lock = threading.Lock()


def broadcast(message):
    """모든 클라이언트에게 메시지를 전송하는 함수"""
    with client_lock:
        for client_socket in clients:
            try:
                client_socket.send(message)
            except socket.error:
                # 메시지 전송 중 오류가 발생하면 해당 클라이언트를 제거
                remove_client(client_socket)


def remove_client(client_socket):
    """클라이언트 목록에서 특정 클라이언트를 안전하게 제거하는 함수"""
    # 이 함수는 client_lock이 이미 획득된 상태에서 호출되어야 합니다.
    if client_socket in clients:
        index = clients.index(client_socket)
        nickname = nicknames[index]

        # 목록에서 클라이언트와 닉네임 제거
        clients.pop(index)
        nicknames.pop(index)

        # 클라이언트 소켓 닫기
        client_socket.close()

        print(f'\'{nickname}\'님이 연결을 종료했습니다.')
        broadcast(f'\'{nickname}\'님이 퇴장하셨습니다.'.encode('utf-8'))


def handle_client(client_socket, addr):
    """
    개별 클라이언트와의 통신을 처리하는 스레드 함수
    """
    # 첫 메시지로 클라이언트의 닉네임을 수신
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
        with client_lock:
            nicknames.append(nickname)
            clients.append(client_socket)

        print(f'\'{nickname}\'님이 입장했습니다. (주소: {addr})')
        broadcast(f'\'{nickname}\'님이 입장하셨습니다.'.encode('utf-8'))

    except (ConnectionResetError, BrokenPipeError):
        print(f'닉네임 수신 중 클라이언트 연결이 끊겼습니다. 주소: {addr}')
        client_socket.close()
        return

    # 메시지 수신 및 처리 루프
    while True:
        try:
            message = client_socket.recv(1024)
            # 클라이언트가 연결을 종료하면 빈 메시지가 수신됨
            if not message:
                break

            decoded_message = message.decode('utf-8')

            # '/종료' 명령어 처리
            if decoded_message == '/종료':
                break

            # 보너스 과제: 귓속말 기능 ('/w 닉네임 메시지' 형식)
            if decoded_message.startswith('/w '):
                parts = decoded_message.split(' ', 2)
                if len(parts) < 3:
                    client_socket.send("'사용법: /w [상대방닉네임] [메시지]'".encode('utf-8'))
                    continue

                target_nickname = parts[1]
                whisper_message = parts[2]
                sender_nickname = nicknames[clients.index(client_socket)]

                with client_lock:
                    if target_nickname in nicknames:
                        target_index = nicknames.index(target_nickname)
                        target_socket = clients[target_index]

                        # 귓속말 전송
                        formatted_whisper = f'\'{sender_nickname}\'님의 귓속말> {whisper_message}'.encode('utf-8')
                        target_socket.send(formatted_whisper)

                        # 발신자에게 확인 메시지 전송
                        sender_confirm = f'\'{target_nickname}\'님에게 귓속말을 보냈습니다.'.encode('utf-8')
                        client_socket.send(sender_confirm)
                    else:
                        client_socket.send(f'\'{target_nickname}\'님을 찾을 수 없습니다.'.encode('utf-8'))

            else:
                # 일반 메시지를 모든 클라이언트에게 브로드캐스트
                sender_nickname = nicknames[clients.index(client_socket)]
                formatted_message = f'\'{sender_nickname}\'> {decoded_message}'.encode('utf-8')
                print(f"수신: '{sender_nickname}'> {decoded_message}")
                broadcast(formatted_message)

        except (ConnectionResetError, BrokenPipeError):
            # 클라이언트가 비정상적으로 연결을 종료한 경우
            break
        except Exception as e:
            print(f'오류 발생: {e}')
            break

    # 클라이언트 연결 종료 처리
    with client_lock:
        remove_client(client_socket)


def start_server():
    """서버를 시작하고 클라이언트 연결을 대기하는 메인 함수"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 서버 종료 후 즉시 재시작 시 주소 재사용 옵션 설정
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f'서버가 시작되었습니다. ({HOST}:{PORT})')

        while True:
            # 클라이언트의 연결 요청을 수락
            client_socket, addr = server_socket.accept()

            # 각 클라이언트를 처리할 새로운 스레드를 생성하고 시작
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr)
            )
            client_thread.daemon = True  # 메인 스레드 종료 시 자식 스레드도 함께 종료
            client_thread.start()

    except OSError as e:
        print(f'서버 소켓 오류: {e}')
    except KeyboardInterrupt:
        print('서버를 종료합니다.')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()