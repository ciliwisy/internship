import json

def generate_location_data():
    # 读取文件
    provinces = {}
    cities = {}
    districts = {}
    
    with open('C:/Users/thinkbook/Desktop/location.txt', 'r', encoding='utf-8') as f:
        for line in f:
            code, full_name = line.strip().split('\t')
            if not code or not full_name:
                continue
                
            adcode = int(code)
            names = full_name.split(',')
            
            # 处理省级
            if code.endswith('0000'):
                provinces[code] = {
                    'name': names[0],
                    'adcode': adcode,
                    'children': []
                }
            
            # 处理市级
            elif code.endswith('00'):
                if len(names) >= 2:
                    cities[code] = {
                        'name': names[-1],  # 取最后一个名称作为城市名
                        'adcode': adcode,
                        'children': []
                    }
                    # 找到对应的省份并添加城市
                    province_code = code[:2] + '0000'
                    if province_code in provinces:
                        provinces[province_code]['children'].append(cities[code])
            
            # 处理区级
            else:
                if len(names) >= 2:
                    districts[code] = {
                        'name': names[-1],  # 取最后一个名称作为区名
                        'adcode': adcode
                    }
                    # 找到对应的市并添加区
                    city_code = code[:4] + '00'
                    if city_code in cities:
                        cities[city_code]['children'].append(districts[code])

    # 转换为列表格式
    result = list(provinces.values())
    
    # 生成 TypeScript 文件内容
    ts_content = f"""
// 此文件由脚本自动生成，请勿手动修改
export interface Region {{
    name: string;
    adcode: number;
    children?: Region[];
}}

export const locationData: Region[] = {json.dumps(result, ensure_ascii=False, indent=2)};
"""

    # 写入文件
    output_path = './locationData.ts'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print('Location data generated successfully!')

if __name__ == '__main__':
    generate_location_data()