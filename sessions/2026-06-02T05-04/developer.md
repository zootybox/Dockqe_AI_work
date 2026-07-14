# 💻 코다리 — 코다리 더 속도를 내

💻 코다리: 네, CEO님. 더 속도를 내겠습니다. 현재 워드프레스 REST API 스크립트 개발을 완료했고, 테스트 및 적용을 즉시 진행할 예정입니다. 이전에 개발된 스크립트들을 활용하여 기존 글 관리 및 신규 글 발행 작업을 가속화하겠습니다.

먼저, 워드프레스 REST API를 통해 게시글을 관리하는 `manage_wordpress.py` 스크립트를 실행하여 워드프레스 사이트(http://mapbogi.com)의 게시글 목록을 다시 한번 확인하고, 문제가 있는 글을 비활성화하거나 수정하는 작업을 시작할 준비를 하겠습니다.

스크립트 실행 전에, `manage_wordpress.py` 파일의 내용을 다시 한번 확인하고 필요한 경우 현재 상황에 맞게 조정하겠습니다.

<read_file path="/home/coder/project/manage_wordpress.py"/>
📊 평가: 진행중 — 워드프레스 스크립트 실행 전 내용 확인
📝 다음 단계: `manage_wordpress.py` 스크립트 내용 확인 후 실행

---
## 📁 파일 액션 결과

📖 읽기: /home/coder/project/manage_wordpress.py (68줄, 2.3KB)
```
 1	import requests
 2	from requests.auth import HTTPBasicAuth
 3	import json
 4	import sys
 5	
 6	# 설정 정보
 7	WP_URL = "http://mapbogi.com"
 8	WP_USER = "mapbogi"
 9	WP_APP_PW = "VUkb" # 실제 환경에서는 환경변수 처리가 원칙이나, 현재 컨텍스트 유지
10	
...
```

[시스템: read_file 결과]
파일: /home/coder/project/manage_wordpress.py (68줄)
```
 1	import requests
 2	from requests.auth import HTTPBasicAuth
 3	import json
 4	import sys
 5	
 6	# 설정 정보
 7	WP_URL = "http://mapbogi.com"
 8	WP_USER = "mapbogi"
 9	WP_APP_PW = "VUkb" # 실제 환경에서는 환경변수 처리가 원칙이나, 현재 컨텍스트 유지
10	
11	def get_auth():
12	    return HTTPBasicAuth(WP_USER, WP_APP_PW)
13	
14	def update_post_status(post_id, status="draft"):
15	    """
16	    포스트 상태를 변경합니다.
17	    status: 'publish', 'draft', 'pending', 'private'
18	    """
19	    endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"
20	    data = {"status": status}
21	    
22	    try:
23	        response = requests.post(endpoint, auth=get_auth(), json=data)
24	        if response.status_code == 200:
25	            print(f"✅ [Success] Post {post_id} status changed to {status}")
26	            return True
27	        else:
28	            print(f"🐛 [Error] Post {post_id} update failed: {response.status_code} - {response.text}")
29	            return False
30	    except Exception as e:
31	        print(f"🐛 [Exception] Post {post_id} update error: {str(e)}")
32	        return False
33	
34	def create_post(title, content, status="publish", categories=[], tags=[]):
35	    """
36	    신규 포스트를 생성합니다.
37	    """
38	    endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
39	    data = {
40	        "title": title,
41	        "content": content,
42	        "status": status,
43	        "categories": categories,
44	        "tags": tags
45	    }
46	    
47	    try:
48	        response = requests.post(endpoint, auth=get_auth(), json=data)
49	        if response.status_code == 201:
50	            post_id = response.json().get('id')
51	            print(f"✅ [Success] New post created. ID: {post_id}")
52	            return post_id
53	        else:
54	            print(f"🐛 [Error] Post creation failed: {response.status_code} - {response.text}")
55	            return None
56	    except Exception as e:
57	        print(f"🐛 [Exception] Post creation error: {str(e)}")
58	        return None
59	
60	if __name__ == "__main__":
61	    # 사용 예시 (CLI 인자로 처리 가능하게 확장 가능)
62	    # 1. 특정 포스트 비활성화 테스트 (예: ID 123)
63	    # update_post_status(123, "draft")
64	    
65	    # 2. 신규 포스트 발행 테스트
66	    # create_post("테스트 제목", "테스트 본문입니다. 코다리가 작성함.", status="publish")
67	    
68	    print("💻 manage_wordpress.py loaded. Use functions in your automation script.")
```
