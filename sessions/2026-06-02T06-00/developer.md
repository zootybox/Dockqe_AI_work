# 💻 코다리 — manage_wordpress.py 스크립트 개발을 계속 진행하고, 게시물 상태 변경, 신규 발행, 전체 목록 조회 기능을 포함하여 운영 환경에 배포 가능한 상태로 만듭니다. 스크립트의 환경 변수를 통한 인증 정보 관리를 구현합니다. [근거: CEO 개인 메모리]

<thought>The CEO wants me to continue developing `manage_wordpress.py`.
Specifically, it needs:
1.  Post status change (e.g., to 'draft').
2.  New post publishing.
3.  List all posts.
4.  Production-ready state.
5.  Environment variable-based authentication (via `.env`).

Looking at the "Recently worked files":
- `/home/coder/project/manage_wordpress.py` (Edited 2 mins ago)
- `/home/coder/project/.env.example` (Created 2 mins ago)

I need to:
1.  Read the current state of `/home/coder/project/manage_wordpress.py`.
2.  Read `/home/coder/project/.env.example` to see the expected format.
3.  Implement/Refine the `WordPressManager` class to ensure all requested features are fully functional and robust.
4.  Verify the code using `python -m py_compile`.
5.  Ensure it's production-ready (logging, error handling, clear naming).

Plan:
1.  `<read_file path="/home/coder/project/manage_wordpress.py"/>`
2.  `<read_file path="/home/coder/project/.env.example"/>`
3.  Modify `manage_wordpress.py` to complete the requested features if missing or improve them.
4.  Run a compile check.
5.  Reveal the file.</thought>💻 코다리: 작업 시작합니다. CEO님, 계속 밀어붙이시는 만큼 속도 내겠습니다. 하지만 시니어로서 코드 검증 없이 그냥 돌리는 건 제 자존심이 허락 안 합니다. ⚙️

우선 현재 구현된 `/home/coder/project/manage_wordpress.py`와 `.env.example` 상태를 확인하고, 요청하신 3대 핵심 기능(상태 변경, 신규 발행, 목록 조회)이 운영 환경 수준으로 완벽하게 구현되었는지 검토하겠습니다.

<read_file path="/home/coder/project/manage_wordpress.py"/>
<read_file path="/home/coder/project/.env.example"/>

📊 평가: 진행중 — 현재 코드 상태 확인 후 최종 보완 작업 예정
📝 다음 단계: 코드 분석 후 누락된 기능 보완 및 `py_compile` 검증 진행

---
## 📁 파일 액션 결과

📖 읽기: /home/coder/project/manage_wordpress.py (108줄, 4.0KB)
```
 1	import os
 2	import requests
 3	from requests.auth import HTTPBasicAuth
 4	from dotenv import load_dotenv
 5	import logging
 6	
 7	# 로깅 설정 - 운영 환경에서 추적이 가능하도록 설정
 8	logging.basicConfig(
 9	    level=logging.INFO,
10	    format='%(asctime)s [%(levelname)s] %(message)s',
...
```
📖 읽기: /home/coder/project/.env.example (4줄, 0.1KB)
```
1	# WordPress Configuration
2	WP_URL=http://mapbogi.com
3	WP_USERNAME=your_username
4	WP_APP_PASSWORD=your_application_password_here
```
📖 읽기: /home/coder/project/manage_wordpress.py (108줄, 4.0KB)
```
 1	import os
 2	import requests
 3	from requests.auth import HTTPBasicAuth
 4	from dotenv import load_dotenv
 5	import logging
 6	
 7	# 로깅 설정 - 운영 환경에서 추적이 가능하도록 설정
 8	logging.basicConfig(
 9	    level=logging.INFO,
10	    format='%(asctime)s [%(levelname)s] %(message)s',
...
```
📖 읽기: /home/coder/project/.env.example (4줄, 0.1KB)
```
1	# WordPress Configuration
2	WP_URL=http://mapbogi.com
3	WP_USERNAME=your_username
4	WP_APP_PASSWORD=your_application_password_here
```

[시스템: read_file 결과]
파일: /home/coder/project/manage_wordpress.py (108줄)
```
  1	import os
  2	import requests
  3	from requests.auth import HTTPBasicAuth
  4	from dotenv import load_dotenv
  5	import logging
  6	
  7	# 로깅 설정 - 운영 환경에서 추적이 가능하도록 설정
  8	logging.basicConfig(
  9	    level=logging.INFO,
 10	    format='%(asctime)s [%(levelname)s] %(message)s',
 11	    datefmt='%Y-%m-%d %H:%M:%S'
 12	)
 13	logger = logging.getLogger(__name__)
 14	
 15	# 환경 변수 로드
 16	load_dotenv()
 17	
 18	class WordPressManager:
 19	    """
 20	    WordPress REST API를 통해 사이트를 관리하는 시니어 엔지니어 설계 클래스.
 21	    SRP(단일 책임 원칙)를 준수하여 각 기능을 메서드로 분리함.
 22	    """
 23	    def __init__(self):
 24	        self.url = os.getenv("WP_URL", "").rstrip('/')
 25	        self.username = os.getenv("WP_USERNAME")
 26	        self.app_password = os.getenv("WP_APP_PASSWORD")
 27	
 28	        if not all([self.url, self.username, self.app_password]):
 29	            logger.error("❌ 필수 환경 변수가 누락되었습니다: WP_URL, WP_USERNAME, WP_APP_PASSWORD")
 30	            raise EnvironmentError("Missing required WordPress environment variables.")
 31	
 32	        self.auth = HTTPBasicAuth(self.username, self.app_password)
 33	        self.api_base_url = f"{self.url}/wp-json/wp/v2"
 34	
 35	    def _request(self, method, endpoint, data=None, params=None):
 36	        """공통 요청 처리 메서드. 에러 핸들링 및 로깅 포함."""
 37	        url = f"{self.api_base_url}/{endpoint}"
 38	        try:
 39	            response = requests.request(
 40	                method=method,
 41	                url=url,
 42	                auth=self.auth,
 43	                json=data,
 44	                params=params,
 45	                timeout=30
 46	            )
 47	            response.raise_for_status()
 48	            return response.json()
 49	        except requests.exceptions.HTTPError as e:
 50	            logger.error(f"HTTP Error occurred: {e} | Response: {response.text}")
 51	            raise
 52	        except Exception as e:
 53	            logger.error(f"Unexpected error occurred: {e}")
 54	            raise
 55	
 56	    def get_all_posts(self, per_page=100):
 57	        """전체 게시글 목록 조회. (Pagination 고려 가능)"""
 58	        logger.info("Fetching all posts...")
 59	        params = {"per_page": per_page}
 60	        return self._request("GET", "posts", params=params)
 61	
 62	    def update_post_status(self, post_id, status="draft"):
 63	        """
 64	        게시글 상태 변경.
 65	        status: 'publish', 'draft', 'pending', 'private'
 66	        """
 67	        logger.info(f"Updating post {post_id} status to {status}...")
 68	        data = {"status": status}
 69	        return self._request("POST", f"posts/{post_id}", data=data)
 70	
 71	    def create_post(self, title, content, status="publish", categories=None, tags=None):
 72	        """신규 게시글 발행."""
 73	        logger.info(f"Creating new post: {title}...")
 74	        data = {
 75	            "title": title,
 76	            "content": content,
 77	            "status": status,
 78	        }
 79	        if categories: data["categories"] = categories
 80	        if tags: data["tags"] = tags
 81	        
 82	        return self._request("POST", "posts", data=data)
 83	
 84	if __name__ == "__main__":
 85	    # 테스트 코드 (운영 환경에서는 별도 스크립트로 호출)
 86	    try:
 87	        wp = WordPressManager()
 88	        
 89	        # 1. 목록 조회 테스트
 90	        posts = wp.get_all_posts()
 91	        logger.info(f"✅ Total posts fetched: {len(posts)}")
 92	
 93	        # 2. 상태 변경 테스트 (첫 번째 글을 초안으로 변경 - 주의: 테스트용)
 94	        # if posts:
 95	        #     first_post_id = posts[0]['id']
 96	        #     wp.update_post_status(first_post_id, "draft")
 97	        #     logger.info(f"✅ Post {first_post_id} changed to draft.")
 98	
 99	        # 3. 신규 발행 테스트
100	        # new_post = wp.create_post(
101	        #     title="코다리가 작성한 테스트 글",
102	        #     content="이 글은 REST API를 통해 자동으로 발행되었습니다. ✅",
103	        #     status="publish"
104	        # )
105	        # logger.info(f"✅ New post created. ID: {new_post['id']}")
106	
107	    except Exception as e:
108	        logger.error(f"Main process failed: {e}")
```

[시스템: read_file 결과]
파일: /home/coder/project/.env.example (4줄)
```
1	# WordPress Configuration
2	WP_URL=http://mapbogi.com
3	WP_USERNAME=your_username
4	WP_APP_PASSWORD=your_application_password_here
```

[시스템: read_file 결과]
파일: /home/coder/project/manage_wordpress.py (108줄)
```
  1	import os
  2	import requests
  3	from requests.auth import HTTPBasicAuth
  4	from dotenv import load_dotenv
  5	import logging
  6	
  7	# 로깅 설정 - 운영 환경에서 추적이 가능하도록 설정
  8	logging.basicConfig(
  9	    level=logging.INFO,
 10	    format='%(asctime)s [%(levelname)s] %(message)s',
 11	    datefmt='%Y-%m-%d %H:%M:%S'
 12	)
 13	logger = logging.getLogger(__name__)
 14	
 15	# 환경 변수 로드
 16	load_dotenv()
 17	
 18	class WordPressManager:
 19	    """
 20	    WordPress REST API를 통해 사이트를 관리하는 시니어 엔지니어 설계 클래스.
 21	    SRP(단일 책임 원칙)를 준수하여 각 기능을 메서드로 분리함.
 22	    """
 23	    def __init__(self):
 24	        self.url = os.getenv("WP_URL", "").rstrip('/')
 25	        self.username = os.getenv("WP_USERNAME")
 26	        self.app_password = os.getenv("WP_APP_PASSWORD")
 27	
 28	        if not all([self.url, self.username, self.app_password]):
 29	            logger.error("❌ 필수 환경 변수가 누락되었습니다: WP_URL, WP_USERNAME, WP_APP_PASSWORD")
 30	            raise EnvironmentError("Missing required WordPress environment variables.")
 31	
 32	        self.auth = HTTPBasicAuth(self.username, self.app_password)
 33	        self.api_base_url = f"{self.url}/wp-json/wp/v2"
 34	
 35	    def _request(self, method, endpoint, data=None, params=None):
 36	        """공통 요청 처리 메서드. 에러 핸들링 및 로깅 포함."""
 37	        url = f"{self.api_base_url}/{endpoint}"
 38	        try:
 39	            response = requests.request(
 40	                method=method,
 41	                url=url,
 42	                auth=self.auth,
 43	                json=data,
 44	                params=params,
 45	                timeout=30
 46	            )
 47	            response.raise_for_status()
 48	            return response.json()
 49	        except requests.exceptions.HTTPError as e:
 50	            logger.error(f"HTTP Error occurred: {e} | Response: {response.text}")
 51	            raise
 52	        except Exception as e:
 53	            logger.error(f"Unexpected error occurred: {e}")
 54	            raise
 55	
 56	    def get_all_posts(self, per_page=100):
 57	        """전체 게시글 목록 조회. (Pagination 고려 가능)"""
 58	        logger.info("Fetching all posts...")
 59	        params = {"per_page": per_page}
 60	        return self._request("GET", "posts", params=params)
 61	
 62	    def update_post_status(self, post_id, status="draft"):
 63	        """
 64	        게시글 상태 변경.
 65	        status: 'publish', 'draft', 'pending', 'private'
 66	        """
 67	        logger.info(f"Updating post {post_id} status to {status}...")
 68	        data = {"status": status}
 69	        return self._request("POST", f"posts/{post_id}", data=data)
 70	
 71	    def create_post(self, title, content, status="publish", categories=None, tags=None):
 72	        """신규 게시글 발행."""
 73	        logger.info(f"Creating new post: {title}...")
 74	        data = {
 75	            "title": title,
 76	            "content": content,
 77	            "status": status,
 78	        }
 79	        if categories: data["categories"] = categories
 80	        if tags: data["tags"] = tags
 81	        
 82	        return self._request("POST", "posts", data=data)
 83	
 84	if __name__ == "__main__":
 85	    # 테스트 코드 (운영 환경에서는 별도 스크립트로 호출)
 86	    try:
 87	        wp = WordPressManager()
 88	        
 89	        # 1. 목록 조회 테스트
 90	        posts = wp.get_all_posts()
 91	        logger.info(f"✅ Total posts fetched: {len(posts)}")
 92	
 93	        # 2. 상태 변경 테스트 (첫 번째 글을 초안으로 변경 - 주의: 테스트용)
 94	        # if posts:
 95	        #     first_post_id = posts[0]['id']
 96	        #     wp.update_post_status(first_post_id, "draft")
 97	        #     logger.info(f"✅ Post {first_post_id} changed to draft.")
 98	
 99	        # 3. 신규 발행 테스트
100	        # new_post = wp.create_post(
101	        #     title="코다리가 작성한 테스트 글",
102	        #     content="이 글은 REST API를 통해 자동으로 발행되었습니다. ✅",
103	        #     status="publish"
104	        # )
105	        # logger.info(f"✅ New post created. ID: {new_post['id']}")
106	
107	    except Exception as e:
108	        logger.error(f"Main process failed: {e}")
```

[시스템: read_file 결과]
파일: /home/coder/project/.env.example (4줄)
```
1	# WordPress Configuration
2	WP_URL=http://mapbogi.com
3	WP_USERNAME=your_username
4	WP_APP_PASSWORD=your_application_password_here
```
