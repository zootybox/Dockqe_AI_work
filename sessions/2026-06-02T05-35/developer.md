# 💻 코다리 — 워드프레스 REST API 스크립트(`manage_wordpress.py`) 개발을 즉시 완료하고, 기존 글의 상태 변경(비활성화/수정) 및 신규 글 발행을 위한 스크립트를 테스트 및 적용합니다. 완료 후 secretary에게 보고합니다.

<thought>*   Goal: Complete the development of `manage_wordpress.py`, test it, and apply it to change the status of existing posts (disable/modify) and publish new posts.
    *   Target Site: `http://mapbogi.com`
    *   Credentials: User `mapbogi`, App Password `VUkb` (as per decision logs).
    *   Current State: Files `get_wordpress_posts.py`, `wordpress_api_utils.py`, and `manage_wordpress.py` have been created.
    *   Required Action:
        1.  Verify the existing code in `manage_wordpress.py` and `wordpress_api_utils.py`.
        2.  Implement/Refine functionality to:
            *   Change post status (e.g., `publish` -> `draft`).
            *   Update post content.
            *   Create new posts.
        3.  Run tests (dry-run or actual small-scale test).
        4.  Apply to the site (as requested).
        5.  Report to secretary.

    *   `/home/coder/project/wordpress_api_utils.py`: Likely contains the API wrapper.
    *   `/home/coder/project/manage_wordpress.py`: Likely contains the logic for managing posts.
    *   `/home/coder/project/get_wordpress_posts.py`: Used for extraction.

    *   Step 1: Read the current implementation of `wordpress_api_utils.py` and `manage_wordpress.py` to see what's missing.
    *   Step 2: Enhance `manage_wordpress.py` to include specific functions for status changes and new post creation.
    *   Step 3: Create a test script or use `manage_wordpress.py` with specific arguments to verify functionality.
    *   Step 4: Execute the status change for "problematic posts" (though the list of problematic posts isn't explicitly provided in this turn, I should implement the *capability* and perhaps a way to load a list of IDs).
    *   Step 5: Final verification.

    *   WordPress REST API uses Basic Auth with Application Passwords.
    *   Endpoint for posts: `/wp-json/wp/v2/posts`
    *   Update post: `POST /wp-json/wp/v2/posts/<id>`
    *   Create post: `POST /wp-json/wp/v2/posts`

    *   Read files first.
    *   Apply edits.
    *   Run tests.
    *   Confirm success.</thought>💻 코다리: 작업 시작합니다.

CEO님, `manage_wordpress.py`를 통해 워드프레스 제어권을 완전히 확보하고, 실제 적용 가능한 수준으로 고도화하겠습니다. 단순히 "코드 짰다"에서 끝내지 않고, 실제로 글 상태가 바뀌는지, 새 글이 올라가는지 검증 루프까지 돌리겠습니다.

먼저 현재 작성된 파일들의 내용을 확인하여 누락된 기능이 있는지 파악하겠습니다.

<read_file path="/home/coder/project/wordpress_api_utils.py"/>
<read_file path="/home/coder/project/manage_wordpress.py"/>

위 파일들을 읽고, 부족한 부분(상태 변경 로직, 신규 발행 인터페이스 등)을 보완한 뒤 테스트 세션을 진행하겠습니다. 확인 후 바로 수정 들어갑니다. ⚙️

📊 평가: 진행중 — 기존 코드 분석 후 고도화 및 테스트 단계 진입 예정
📝 다음 단계: `wordpress_api_utils.py`와 `manage_wordpress.py` 분석 결과 바탕으로 기능 보완 및 테스트 실행

---
## 📁 파일 액션 결과

📖 읽기: /home/coder/project/wordpress_api_utils.py (183줄, 6.8KB)
```
 1	import requests
 2	import json
 3	import base64
 4	
 5	# 워드프레스 정보 (환경 변수 또는 설정 파일에서 로드하는 것이 보안상 더 좋습니다)
 6	WORDPRESS_URL = "http://mapbogi.com"
 7	USERNAME = "mapbogi"
 8	APPLICATION_PASSWORD = "VUkb" # 애플리케이션 비밀번호
 9	
10	# REST API 엔드포인트
...
```
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
파일: /home/coder/project/wordpress_api_utils.py (183줄)
```
  1	import requests
  2	import json
  3	import base64
  4	
  5	# 워드프레스 정보 (환경 변수 또는 설정 파일에서 로드하는 것이 보안상 더 좋습니다)
  6	WORDPRESS_URL = "http://mapbogi.com"
  7	USERNAME = "mapbogi"
  8	APPLICATION_PASSWORD = "VUkb" # 애플리케이션 비밀번호
  9	
 10	# REST API 엔드포인트
 11	POSTS_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
 12	CATEGORIES_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/categories"
 13	TAGS_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/tags"
 14	
 15	# 인증 헤더 생성
 16	credentials = f"{USERNAME}:{APPLICATION_PASSWORD}"
 17	token = base64.b64encode(credentials.encode())
 18	AUTH_HEADERS = {
 19	    "Authorization": f"Basic {token.decode('utf-8')}",
 20	    "Content-Type": "application/json"
 21	}
 22	
 23	def get_posts(post_id=None, status=None, per_page=100, page=1):
 24	    """
 25	    워드프레스 게시글을 조회합니다.
 26	    :param post_id: 조회할 게시글의 ID (선택 사항)
 27	    :param status: 조회할 게시글의 상태 (예: 'publish', 'draft', 'private', 'trash')
 28	    :param per_page: 페이지당 게시글 수
 29	    :param page: 조회할 페이지 번호
 30	    :return: 게시글 목록 또는 단일 게시글 딕셔너리
 31	    """
 32	    params = {"per_page": per_page, "page": page}
 33	    if status:
 34	        params["status"] = status
 35	
 36	    url = POSTS_API_ENDPOINT
 37	    if post_id:
 38	        url = f"{POSTS_API_ENDPOINT}/{post_id}"
 39	        params = {} # 단일 게시글 조회 시 per_page, page는 필요 없음
 40	
 41	    try:
 42	        response = requests.get(url, headers=AUTH_HEADERS, params=params, timeout=10)
 43	        response.raise_for_status()
 44	        return response.json()
 45	    except requests.exceptions.RequestException as e:
 46	        print(f"Error fetching posts: {e}")
 47	        return None
 48	
 49	def update_post(post_id, data):
 50	    """
 51	    특정 게시글의 내용을 수정합니다.
 52	    :param post_id: 수정할 게시글의 ID
 53	    :param data: 수정할 내용을 담은 딕셔너리 (예: {"status": "draft", "title": "새 제목"})
 54	    :return: 수정된 게시글 딕셔너리 또는 None
 55	    """
 56	    url = f"{POSTS_API_ENDPOINT}/{post_id}"
 57	    try:
 58	        response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data), timeout=10)
 59	        response.raise_for_status()
 60	        return response.json()
 61	    except requests.exceptions.RequestException as e:
 62	        print(f"Error updating post {post_id}: {e}")
 63	        return None
 64	
 65	def create_post(title, content, status="publish", categories=None, tags=None):
 66	    """
 67	    새로운 게시글을 생성하고 발행합니다.
 68	    :param title: 게시글 제목
 69	    :param content: 게시글 내용
 70	    :param status: 게시글 상태 (기본 'publish')
 71	    :param categories: 카테고리 ID 목록 (예: [1, 2])
 72	    :param tags: 태그 ID 목록 (예: [10, 11])
 73	    :return: 생성된 게시글 딕셔너리 또는 None
 74	    """
 75	    data = {
 76	        "title": title,
 77	        "content": content,
 78	        "status": status
 79	    }
 80	    if categories:
 81	        data["categories"] = categories
 82	    if tags:
 83	        data["tags"] = tags
 84	
 85	    try:
 86	        response = requests.post(POSTS_API_ENDPOINT, headers=AUTH_HEADERS, data=json.dumps(data), timeout=10)
 87	        response.raise_for_status()
 88	        return response.json()
 89	    except requests.exceptions.RequestException as e:
 90	        print(f"Error creating post: {e}")
 91	        return None
 92	
 93	def get_categories(name=None):
 94	    """
 95	    워드프레스 카테고리를 조회합니다.
 96	    :param name: 특정 카테고리 이름 (선택 사항)
 97	    :return: 카테고리 목록 딕셔너리
 98	    """
 99	    params = {}
100	    if name:
101	        params["search"] = name
102	    try:
103	        response = requests.get(CATEGORIES_API_ENDPOINT, headers=AUTH_HEADERS, params=params, timeout=10)
104	        response.raise_for_status()
105	        return response.json()
106	    except requests.exceptions.RequestException as e:
107	        print(f"Error fetching categories: {e}")
108	        return None
109	
110	def get_tags(name=None):
111	    """
112	    워드프레스 태그를 조회합니다.
113	    :param name: 특정 태그 이름 (선택 사항)
114	    :return: 태그 목록 딕셔너리
115	    """
116	    params = {}
117	    if name:
118	        params["search"] = name
119	    try:
120	        response = requests.get(TAGS_API_ENDPOINT, headers=AUTH_HEADERS, params=params, timeout=10)
121	        response.raise_for_status()
122	        return response.json()
123	    except requests.exceptions.RequestException as e:
124	        print(f"Error fetching tags: {e}")
125	        return None
126	
127	if __name__ == "__main__":
128	    print("--- Testing WordPress API Utilities ---")
129	
130	    # 모든 게시글 조회 (예시)
131	    print("\nGetting all published posts...")
132	    posts = get_posts(status="publish")
133	    if posts:
134	        for post in posts[:5]: # 상위 5개만 출력
135	            print(f"  ID: {post['id']}, Title: {post['title']['rendered']}, Status: {post['status']}")
136	    else:
137	        print("  No posts found or error occurred.")
138	
139	    # 특정 게시글 조회 (예시: 첫 번째 게시글)
140	    if posts and posts[0]:
141	        first_post_id = posts[0]['id']
142	        print(f"\nGetting post with ID: {first_post_id}...")
143	        single_post = get_posts(post_id=first_post_id)
144	        if single_post:
145	            print(f"  Title: {single_post['title']['rendered']}, Content: {single_post['content']['rendered'][:50]}...")
146	        else:
147	            print("  Post not found or error occurred.")
148	
149	    # 게시글 상태 수정 (예시: 첫 번째 게시글을 'draft'로 변경 시도 - 실제 적용은 주석 해제 후)
150	    # print(f"\nUpdating status of post {first_post_id} to draft...")
151	    # updated_post = update_post(first_post_id, {"status": "draft"})
152	    # if updated_post:
153	    #     print(f"  Updated Post ID: {updated_post['id']}, New Status: {updated_post['status']}")
154	    # else:
155	    #     print("  Failed to update post.")
156	
157	    # 새 게시글 생성 (예시 - 실제 적용은 주석 해제 후)
158	    # print("\nCreating a new post...")
159	    # new_post_title = "새로운 테스트 게시글 by 코다리"
160	    # new_post_content = "이것은 코다리 에이전트가 워드프레스 REST API를 사용하여 생성한 테스트 게시글입니다."
161	    # created_post = create_post(new_post_title, new_post_content, status="draft") # 초안으로 생성
162	    # if created_post:
163	    #     print(f"  Created Post ID: {created_post['id']}, Title: {created_post['title']['rendered']}, Status: {created_post['status']}")
164	    # else:
165	    #     print("  Failed to create post.")
166	
167	    # 카테고리 조회 (예시)
168	    print("\nGetting categories...")
169	    categories = get_categories()
170	    if categories:
171	        for cat in categories[:5]:
172	            print(f"  ID: {cat['id']}, Name: {cat['name']}")
173	    else:
174	        print("  No categories found or error occurred.")
175	
176	    # 태그 조회 (예시)
177	    print("\nGetting tags...")
178	    tags = get_tags()
179	    if tags:
180	        for tag in tags[:5]:
181	            print(f"  ID: {tag['id']}, Name: {tag['name']}")
182	    else:
183	        print("  No tags found or error occurred.")
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
