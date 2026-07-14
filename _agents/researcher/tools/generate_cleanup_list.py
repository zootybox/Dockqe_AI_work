import pandas as pd
import json
import os

# 경로 설정
COMPANY_DIR = "/root/.publishflow-ai-brain/project/_company"
CSV_INPUT = os.path.join(COMPANY_DIR, "_shared/posts_analysis.csv")
JSON_INPUT = os.path.join(COMPANY_DIR, "_shared/post_audit_report.json")
OUTPUT_FILE = os.path.join(COMPANY_DIR, "_shared/content_cleanup_list.csv")

def classify(row):
    try:
        length = int(row.get('length', 0))
        # 구조 확인 (H2, H3 태그 존재 여부)
        # CSV에서는 'has_structure' 컬럼이 True/False로 있을 것으로 가정, 
        # JSON에서는 'has_structure' 키가 있을 것으로 가정
        has_structure = str(row.get('has_structure', 'False')).lower() == 'true'
        
        if length < 500:
            return "삭제"
        elif length < 1000 or not has_structure:
            return "보완"
        else:
            return "유지"
    except:
        return "검토 필요"

def main():
    data = []
    
    # 1. CSV 파일 우선 시도
    if os.path.exists(CSV_INPUT):
        print(f"CSV에서 읽는 중: {CSV_INPUT}")
        df_input = pd.read_csv(CSV_INPUT)
        data = df_input.to_dict('records')
    # 2. JSON 파일 차선 시도
    elif os.path.exists(JSON_INPUT):
        print(f"JSON에서 읽는 중: {JSON_INPUT}")
        with open(JSON_INPUT, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            # post_audit_report.json 구조: modify_list 또는 전체 리스트 확인
            if 'modify_list' in json_data:
                data = json_data['modify_list']
            elif isinstance(json_data, list):
                data = json_data
            else:
                # 기타 구조 처리
                for key, value in json_data.items():
                    if isinstance(value, list):
                        data = value
                        break
    else:
        print("오류: 입력 데이터 파일을 찾을 수 없습니다.")
        return

    if not data:
        print("오류: 분석할 포스트 데이터가 없습니다.")
        return

    # 데이터프레임 변환 및 분류 적용
    df = pd.DataFrame(data)
    df['decision'] = df.apply(classify, axis=1)
    
    # 필요한 컬럼만 추출 (ID, 제목, 길이, 구조여부, 결정)
    # 컬럼명이 다를 수 있으므로 유연하게 매칭
    col_map = {
        'id': 'Post ID',
        'title': 'Title',
        'length': 'Length',
        'has_structure': 'Has Structure',
        'decision': 'Decision'
    }
    
    # 실제 존재하는 컬럼만 필터링
    final_cols = []
    for src, target in col_map.items():
        # JSON의 경우 title이 dict일 수 있음 {'rendered': '...'}
        if src == 'title' and 'title' in df.columns:
            df['title'] = df['title'].apply(lambda x: x.get('rendered', str(x)) if isinstance(x, dict) else str(x))
        
        if src in df.columns:
            df = df.rename(columns={src: target})
            final_cols.append(target)
    
    # 결정 컬럼은 반드시 포함
    if 'Decision' not in final_cols:
        final_cols.append('Decision')

    df[final_cols].to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"성공적으로 생성됨: {OUTPUT_FILE}")
    print(df['Decision'].value_counts().to_string())

if __name__ == "__main__":
    main()
