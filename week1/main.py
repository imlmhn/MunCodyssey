import csv

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def sort_by_flammability(data):
    return sorted(data, key=lambda x: float(x['Flammability']), reverse=True)

def filter_high_flammability(data, threshold=0.7):
    return [item for item in data if float(item['Flammability']) >= threshold]

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    input_file = 'week2/Mars_Base_Inventory_List.csv'
    output_file = 'week2/Mars_Base_Inventory_danger.csv'
    
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
    print(f"\n인화성 지수가 0.7 이상인 목록이 {output_file} 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()
