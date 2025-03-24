def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        headers = file.readline().strip().split(',')
        for line in file:
            values = line.strip().split(',')
            item = {headers[i]: values[i] for i in range(len(headers))}
            data.append(item)
    return data

def sort_by_flammability(data):
    return sorted(data, key=lambda x: float(x['Flammability']), reverse=True)

def filter_high_flammability(data, threshold=0.7):
    return [item for item in data if float(item['Flammability']) >= threshold]

def write_csv(file_path, data):
    with open(file_path, mode='w', encoding='utf-8') as file:
        headers = data[0].keys()
        file.write(','.join(headers) + '\n')
        for item in data:
            file.write(','.join(str(item[h]) for h in headers) + '\n')

def write_binary(file_path, data):
    with open(file_path, mode='wb') as file:
        for item in data:
            line = ''
            for h in item.keys():
                value = item[h]
                if isinstance(value, float):  # 실수형 데이터인 경우
                    line += float(value) + ','  # 실수형 데이터 그대로 추가
                else:
                    line += str(value) + ','  # 문자 데이터도 문자열로 변환하여 추가
            line = line.rstrip(',') + '\n'  # 마지막 ',' 제거하고 줄바꿈 추가
            file.write(line.encode('utf-8'))

def read_binary(file_path):
    data = []
    with open(file_path, mode='rb') as file:
        lines = file.readlines()
        headers = lines[0].decode('utf-8').strip().split(',')
        for line in lines[1:]:
            values = line.decode('utf-8').strip().split(',')
            item = {headers[i]: values[i] for i in range(len(headers))}
            data.append(item)
    return data

def main():
    input_file = 'week2/Mars_Base_Inventory_List.csv'
    output_file = 'week2/Mars_Base_Inventory_danger.csv'
    binary_file = 'week2/Mars_Base_Inventory_List.bin'
    
    # CSV 파일 읽기
    inventory_data = read_csv(input_file)
    
    # 인화성 기준으로 정렬
    sorted_inventory = sort_by_flammability(inventory_data)
    print("정렬된 적재 화물 목록:")
    for item in sorted_inventory:
        print(item)
    
    # 인화성 지수가 0.7 이상인 목록 필터링
    dangerous_items = filter_high_flammability(sorted_inventory, 0.7)
    print("\n인화성 지수가 0.7 이상인 목록:")
    for item in dangerous_items:
        print(item)
    
    # CSV 파일로 저장
    write_csv(output_file, dangerous_items)
    
    # 이진 파일로 저장
    write_binary(binary_file, sorted_inventory)
    
    # 이진 파일 다시 읽기 및 출력
    loaded_data = read_binary(binary_file)
    print("\n이진 파일에서 읽어온 정렬된 목록:")
    for item in loaded_data:
        print(item)

if __name__ == "__main__":
    main()
    
# 텍스트 파일 vs 이진 파일 차이점 및 장단점
# 텍스트 파일 장점: 사람이 읽기 쉬우며 편집이 용이함
# 텍스트 파일 단점: 데이터 크기가 크고, 저장 시 포맷 변환이 필요할 수 있음
# 이진 파일 장점: 빠른 읽기/쓰기 속도, 저장 공간 절약
# 이진 파일 단점: 사람이 직접 읽을 수 없으며, 특정 프로그램이 필요함
