import requests
import json
import os

CONFIG_PATH = "/root/.publishflow-ai-brain/project/_company/_shared/wp_config.json"
JSON_PATH = "/root/.publishflow-ai-brain/project/_company/_shared/post_audit_report.json"

def main():
    # 설정 로드
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    
    WP_URL = config['wp_url']
    WP_USER = config['wp_username']
    WP_PASS = config['wp_password']
    AUTH = (WP_USER, WP_PASS)

    # 삭제 리스트 로드
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    delete_list = report.get('delete_list', [])
    if not delete_list:
        print("삭제할 포스트가 없습니다.")
        return

    print(f"포스트 {len(delete_list)}건의 삭제를 시작합니다...")
    
    success_count = 0
    fail_count = 0
    
    for post_id in delete_list:
        try:
            # force=true 옵션으로 휴지통을 거치지 않고 영구 삭제
            response = requests.delete(
                f"{WP_URL}/wp-json/wp/v2/posts/{post_id}", 
                auth=AUTH, 
                params={'force': True}, 
                timeout=30
            )
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"포스트 삭제 실패 {post_id}: {response.status_code}")
                fail_count += 1
        except Exception as e:
            print(f"포스트 삭제 중 오류 발생 {post_id}: {str(e)}")
            fail_count += 1

    print(f"결과: 성공 {success_count}, 실패 {fail_count}")

if __name__ == "__main__":
    main()
