# 💻 코다리 — 코다리 작업 계속 진행하라고

<thought>*   User (CEO) is demanding progress: "Continue the work, Kodari."
    *   Previous context:
        *   Target: `http://mapbogi.com` (WordPress site) [근거: 의사결정 로그].
        *   Goal: API connection verification, listing posts, changing post status (to 'draft' for low-value content), and publishing new posts [근거: 의사결정 로그].
        *   Current status: A script `/home/coder/project/manage_wordpress.py` was created but there were issues with `pip install requests` and environment setup [근거: 통합 스케줄, 의사결정 로그].
        *   Latest instruction in decision logs: Resolve `pip` installation issues using `python3 -m pip` or virtual environments [근거: 의사결정 로그].

    *   The primary bottleneck is the execution environment for the Python script (`manage_wordpress.py`).
    *   I need to ensure the environment is ready (dependencies installed) and then actually run the script to verify the WordPress API connection and perform the requested tasks.

    *   Step 1: Check if `/home/coder/project/manage_wordpress.py` actually exists and read its content.
    *   Step 2: Check for `.env` file or credentials.
    *   Step 3: Attempt to install dependencies (`requests`, `python-dotenv`) using the recommended `python3 -m pip` method.
    *   Step 4: Run the script to verify connection and list posts.
    *   Step 5: If successful, report the result and proceed to the next phase (modifying posts).

    *   *Tone*: Senior Full-stack Engineer Kodari. Professional, responsible, "don't just move on without verification."
    *   *Constraints*: Use `<read_file>`, `<run_command>`, `<list_files>`. No guessing paths.

    *   *Action 1*: List files in `/home/coder/project/` to confirm the script's existence.
    *   *Action 2*: Read `manage_wordpress.py`.
    *   *Action 3*: Try installing dependencies.
    *   *Action 4*: Run the script.

    *Wait*, I can't see the output of `run_command` in the *current* turn. I have to set up the sequence.

    *Refined Plan for this turn*:
    1.  Confirm file existence and content.
    2.  Attempt dependency installation.
    3.  Execute the script to verify the API.

    *Self-Correction*: The user is impatient. I need to show *actual* execution.

    *Execution steps*:
    1. `<list_files path="/home/coder/project/">`
    2. `<read_file path="/home/coder/project/manage_wordpress.py">` (if it exists)
    3. `<run_command>python3 -m pip install requests python-dotenv</run_command>`
    4. `<run_command>python3 /home/coder/project/manage_wordpress.py</run_command>` (assuming the script has a main block for verification)

    *Check Decision Log*: The log says "pip install requests 못하는 이유" and "가상환경(venv)을 통해 진행한다". I should probably create a venv to be safe and professional.

    *Revised Execution Sequence*:
    1. `<list_files path="/home/coder/project/">`
    2. `<read_file path="/home/coder/project/manage_wordpress.py">`
    3. `<run_command>python3 -m venv /home/coder/project/venv && /home/coder/project/venv/bin/pip install requests python-dotenv</run_command>`
    4. `<run_command>/home/coder/project/venv/bin/python3 /home/coder/project/manage_wordpress.py</run_command>`

    *Actually, looking at the prompt*: I should use the provided tool paths if any, but this is a custom script.

    *Let's start by exploring*.</thought>💻 코다리: 작업 계속 진행합니다. CEO님, 계속 밀어붙이시는 만큼 속도 내겠습니다. 하지만 시니어로서 환경 설정 제대로 안 하고 코드부터 돌렸다가 에러 뿜는 건 제 스타일이 아닙니다. [근거: 개인 목표]

현재 상황은 `manage_wordpress.py` 스크립트는 준비되었으나, `pip` 설치 문제와 가상환경 설정 등 실행 환경에서 병목이 있었던 상태입니다. [근거: 통합 스케줄, 의사결정 로그]

**이번 턴에서 확실하게 끝낼 작업:**
1. 프로젝트 폴더 내 파일 구조 재확인 [근거: 작업 흐름 1단계]
2. `manage_wordpress.py` 코드 최신 상태 확인 [근거: 작업 흐름 2단계]
3. 가상환경(venv) 생성 및 필수 패키지(`requests`, `python-dotenv`) 설치 [근거: 의사결정 로그 2026-06-04]
4. 실제 워드프레스 API 연결 검증 및 포스트 목록 조회 실행 [근거: 의사결정 로그 2026-06-03]

바로 실행합니다. ⚙️

<list_files path="/home/coder/project/"/>
<read_file path="/home/coder/project/manage_wordpress.py"/>
<run_command>python3 -m venv /home/coder/project/venv && /home/coder/project/venv/bin/pip install requests python-dotenv</run_command>
<run_command>/home/coder/project/venv/bin/python3 /home/coder/project/manage_wordpress.py</run_command>

자가검증: 사실 4개 / 추측 0개 [근거: 의사결정 로그, 통합 스케줄, 개인 목표, 작업 흐름]

📊 평가: 진행중 — 실행 환경 구축 및 API 연결 검증 단계 진입
📝 다음 단계: API 연결 결과 확인 후, '가치 없는 콘텐츠' 비공개 처리 스크립트 실행 및 보고

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: ``, `<list_files>`. No guessing paths.

    *   *Action 1*: List files in `/home/coder/project/` to c`
```
/bin/sh: 2: Syntax error: Unterminated quoted string
```
_❌ exit 2_

### 🔧 실행: `python3 /home/coder/project/manage_wordpress.py`
```
Traceback (most recent call last):
  File "/home/coder/project/manage_wordpress.py", line 2, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```
_❌ exit 1_

### 🔧 실행: `python3 -m venv /home/coder/project/venv && /home/coder/project/venv/bin/pip install requests python`
```
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.13-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /home/coder/project/venv/bin/python3
```
_❌ exit 1_

### 🔧 실행: `/home/coder/project/venv/bin/python3 /home/coder/project/manage_wordpress.py`
```
Traceback (most recent call last):
  File "/home/coder/project/manage_wordpress.py", line 2, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```
_❌ exit 1_

### 🔧 실행: `python3 -m venv /home/coder/project/venv && /home/coder/project/venv/bin/pip install requests python`
```
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.13-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /home/coder/project/venv/bin/python3
```
_❌ exit 1_

### 🔧 실행: `/home/coder/project/venv/bin/python3 /home/coder/project/manage_wordpress.py`
```
Traceback (most recent call last):
  File "/home/coder/project/manage_wordpress.py", line 2, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```
_❌ exit 1_

---
## 📁 파일 액션 결과

📖 읽기: /home/coder/project/manage_wordpress.py (122줄, 4.3KB)
```
 1	import os
 2	import requests
 3	from requests.auth import HTTPBasicAuth
 4	from dotenv import load_dotenv
 5	import logging
 6	import sys
 7	import argparse
 8	import time
 9	
10	# 로깅 설정: 운영 환경에서도 추적 가능하도록 설정
...
```
📖 읽기: /home/coder/project/manage_wordpress.py (122줄, 4.3KB)
```
 1	import os
 2	import requests
 3	from requests.auth import HTTPBasicAuth
 4	from dotenv import load_dotenv
 5	import logging
 6	import sys
 7	import argparse
 8	import time
 9	
10	# 로깅 설정: 운영 환경에서도 추적 가능하도록 설정
...
```
📖 읽기: /home/coder/project/manage_wordpress.py (122줄, 4.3KB)
```
 1	import os
 2	import requests
 3	from requests.auth import HTTPBasicAuth
 4	from dotenv import load_dotenv
 5	import logging
 6	import sys
 7	import argparse
 8	import time
 9	
10	# 로깅 설정: 운영 환경에서도 추적 가능하도록 설정
...
```
📂 목록: /home/coder/project/
```
📄 Autonomous_Backup.md
📄 P-Reinforce_Architecture.md
📄 README.md
📄 blog_post_guidelines.md
📄 company_state.json
📄 get_wordpress_posts.py
📄 manage_wordpress.py
📄 publishflow-ai-2.89.223.vsix
📄 safe_git_push.bat
📁 sessions/
📁 venv/
📄 wordpress_api_utils.py
📄 마크다운.md
```
📂 목록: /home/coder/project/
```
📄 Autonomous_Backup.md
📄 P-Reinforce_Architecture.md
📄 README.md
📄 blog_post_guidelines.md
📄 company_state.json
📄 get_wordpress_posts.py
📄 manage_wordpress.py
📄 publishflow-ai-2.89.223.vsix
📄 safe_git_push.bat
📁 sessions/
📁 venv/
📄 wordpress_api_utils.py
📄 마크다운.md
```
📂 목록: /home/coder/project/
```
📄 Autonomous_Backup.md
📄 P-Reinforce_Architecture.md
📄 README.md
📄 blog_post_guidelines.md
📄 company_state.json
📄 get_wordpress_posts.py
📄 manage_wordpress.py
📄 publishflow-ai-2.89.223.vsix
📄 safe_git_push.bat
📁 sessions/
📁 venv/
📄 wordpress_api_utils.py
📄 마크다운.md
```

[시스템: read_file 결과]
파일: /home/coder/project/manage_wordpress.py (122줄)
```
  1	import os
  2	import requests
  3	from requests.auth import HTTPBasicAuth
  4	from dotenv import load_dotenv
  5	import logging
  6	import sys
  7	import argparse
  8	import time
  9	
 10	# 로깅 설정: 운영 환경에서도 추적 가능하도록 설정
 11	logging.basicConfig(
 12	    level=logging.INFO,
 13	    format='%(asctime)s [%(levelname)s] %(message)s',
 14	    handlers=[
 15	        logging.FileHandler("wordpress_manage.log"),
 16	        logging.StreamHandler(sys.stdout)
 17	    ]
 18	)
 19	logger = logging.getLogger(__name__)
 20	
 21	load_dotenv()
 22	
 23	class WordPressManager:
 24	    def __init__(self):
 25	        self.site_url = os.getenv("WP_URL", "http://mapbogi.com").rstrip('/')
 26	        self.username = os.getenv("WP_USER")
 27	        self.password = os.getenv("WP_PASS")
 28	        
 29	        if not self.username or not self.password:
 30	            logger.error("환경 변수 WP_USER 또는 WP_PASS가 설정되지 않았습니다. .env 파일을 확인하세요.")
 31	            sys.exit(1)
 32	            
 33	        self.auth = HTTPBasicAuth(self.username, self.password)
 34	        self.api_base = f"{self.site_url}/wp-json/wp/v2"
 35	
 36	    def _request(self, method, endpoint, data=None):
 37	        url = f"{self.api_base}/{endpoint}"
 38	        try:
 39	            response = requests.request(
 40	                method, url, auth=self.auth, json=data, timeout=10
 41	            )
 42	            response.raise_for_status()
 43	            return response.json()
 44	        except requests.exceptions.HTTPError as e:
 45	            logger.error(f"HTTP Error: {e} | Response: {response.text}")
 46	            return None
 47	        except Exception as e:
 48	            logger.error(f"Unexpected Error: {e}")
 49	            return None
 50	
 51	    def get_all_posts(self, per_page=100):
 52	        """모든 게시글 목록을 가져옵니다. (페이징 처리 포함)"""
 53	        posts = []
 54	        page = 1
 55	        while True:
 56	            logger.info(f"Fetching posts page {page}...")
 57	            data = self._request("GET", f"posts?per_page={per_page}&page={page}")
 58	            if not data:
 59	                break
 60	            posts.extend(data)
 61	            if len(data) < per_page:
 62	                break
 63	            page += 1
 64	        logger.info(f"Total {len(posts)} posts retrieved.")
 65	        return posts
 66	
 67	    def update_post_status(self, post_id, status="draft"):
 68	        """특정 게시글의 상태를 변경합니다. (예: 'publish' -> 'draft')"""
 69	        logger.info(f"Updating post {post_id} status to {status}...")
 70	        data = {"status": status}
 71	        result = self._request("POST", f"posts/{post_id}", data=data)
 72	        if result:
 73	            logger.info(f"Successfully updated post {post_id} to {status}.")
 74	            return True
 75	        return False
 76	
 77	    def create_post(self, title, content, status="publish", categories=None, tags=None):
 78	        """신규 게시글을 발행합니다."""
 79	        logger.info(f"Creating new post: {title}...")
 80	        data = {
 81	            "title": title,
 82	            "content": content,
 83	            "status": status,
 84	        }
 85	        if categories: data["categories"] = categories
 86	        if tags: data["tags"] = tags
 87	        
 88	        result = self._request("POST", "posts", data=data)
 89	        if result:
 90	            logger.info(f"Successfully created post ID: {result.get('id')}")
 91	            return result.get('id')
 92	        return None
 93	
 94	def main():
 95	    parser = argparse.ArgumentParser(description="WordPress Management Script")
 96	    parser.add_argument("action", choices=["list", "draft", "publish"], help="Action to perform")
 97	    parser.add_argument("--id", type=int, help="Post ID for draft action")
 98	    parser.add_argument("--title", type=str, help="Title for publish action")
 99	    parser.add_argument("--content", type=str, help="Content for publish action")
100	    
101	    args = parser.parse_args()
102	    wp = WordPressManager()
103	
104	    if args.action == "list":
105	        posts = wp.get_all_posts()
106	        for p in posts:
107	            print(f"ID: {p['id']} | Status: {p['status']} | Title: {p['title']['rendered']}")
108	            
109	    elif args.action == "draft":
110	        if not args.id:
111	            print("Error: --id is required for draft action.")
112	            return
113	        wp.update_post_status(args.id, "draft")
114	        
115	    elif args.action == "publish":
116	        if not args.title or not args.content:
117	            print("Error: --title and --content are required for publish action.")
118	            return
119	        wp.create_post(args.title, args.content)
120	
121	if __name__ == "__main__":
122	    main()
```

[시스템: read_file 결과]
파일: /home/coder/project/manage_wordpress.py (122줄)
```
  1	import os
  2	import requests
  3	from requests.auth import HTTPBasicAuth
  4	from dotenv import load_dotenv
  5	import logging
  6	import sys
  7	import argparse
  8	import time
  9	
 10	# 로깅 설정: 운영 환경에서도 추적 가능하도록 설정
 11	logging.basicConfig(
 12	    level=logging.INFO,
 13	    format='%(asctime)s [%(levelname)s] %(message)s',
 14	    handlers=[
 15	        logging.FileHandler("wordpress_manage.log"),
 16	        logging.StreamHandler(sys.stdout)
 17	    ]
 18	)
 19	logger = logging.getLogger(__name__)
 20	
 21	load_dotenv()
 22	
 23	class WordPressManager:
 24	    def __init__(self):
 25	        self.site_url = os.getenv("WP_URL", "http://mapbogi.com").rstrip('/')
 26	        self.username = os.getenv("WP_USER")
 27	        self.password = os.getenv("WP_PASS")
 28	        
 29	        if not self.username or not self.password:
 30	            logger.error("환경 변수 WP_USER 또는 WP_PASS가 설정되지 않았습니다. .env 파일을 확인하세요.")
 31	            sys.exit(1)
 32	            
 33	        self.auth = HTTPBasicAuth(self.username, self.password)
 34	        self.api_base = f"{self.site_url}/wp-json/wp/v2"
 35	
 36	    def _request(self, method, endpoint, data=None):
 37	        url = f"{self.api_base}/{endpoint}"
 38	        try:
 39	            response = requests.request(
 40	                method, url, auth=self.auth, json=data, timeout=10
 41	            )
 42	            response.raise_for_status()
 43	            return response.json()
 44	        except requests.exceptions.HTTPError as e:
 45	            logger.error(f"HTTP Error: {e} | Response: {response.text}")
 46	            return None
 47	        except Exception as e:
 48	            logger.error(f"Unexpected Error: {e}")
 49	            return None
 50	
 51	    def get_all_posts(self, per_page=100):
 52	        """모든 게시글 목록을 가져옵니다. (페이징 처리 포함)"""
 53	        posts = []
 54	        page = 1
 55	        while True:
 56	            logger.info(f"Fetching posts page {page}...")
 57	            data = self._request("GET", f"posts?per_page={per_page}&page={page}")
 58	            if not data:
 59	                break
 60	            posts.extend(data)
 61	            if len(data) < per_page:
 62	                break
 63	            page += 1
 64	        logger.info(f"Total {len(posts)} posts retrieved.")
 65	        return posts
 66	
 67	    def update_post_status(self, post_id, status="draft"):
 68	        """특정 게시글의 상태를 변경합니다. (예: 'publish' -> 'draft')"""
 69	        logger.info(f"Updating post {post_id} status to {status}...")
 70	        data = {"status": status}
 71	        result = self._request("POST", f"posts/{post_id}", data=data)
 72	        if result:
 73	            logger.info(f"Successfully updated post {post_id} to {status}.")
 74	            return True
 75	        return False
 76	
 77	    def create_post(self, title, content, status="publish", categories=None, tags=None):
 78	        """신규 게시글을 발행합니다."""
 79	        logger.info(f"Creating new post: {title}...")
 80	        data = {
 81	            "title": title,
 82	            "content": content,
 83	            "status": status,
 84	        }
 85	        if categories: data["categories"] = categories
 86	        if tags: data["tags"] = tags
 87	        
 88	        result = self._request("POST", "posts", data=data)
 89	        if result:
 90	            logger.info(f"Successfully created post ID: {result.get('id')}")
 91	            return result.get('id')
 92	        return None
 93	
 94	def main():
 95	    parser = argparse.ArgumentParser(description="WordPress Management Script")
 96	    parser.add_argument("action", choices=["list", "draft", "publish"], help="Action to perform")
 97	    parser.add_argument("--id", type=int, help="Post ID for draft action")
 98	    parser.add_argument("--title", type=str, help="Title for publish action")
 99	    parser.add_argument("--content", type=str, help="Content for publish action")
100	    
101	    args = parser.parse_args()
102	    wp = WordPressManager()
103	
104	    if args.action == "list":
105	        posts = wp.get_all_posts()
106	        for p in posts:
107	            print(f"ID: {p['id']} | Status: {p['status']} | Title: {p['title']['rendered']}")
108	            
109	    elif args.action == "draft":
110	        if not args.id:
111	            print("Error: --id is required for draft action.")
112	            return
113	        wp.update_post_status(args.id, "draft")
114	        
115	    elif args.action == "publish":
116	        if not args.title or not args.content:
117	            print("Error: --title and --content are required for publish action.")
118	            return
119	        wp.create_post(args.title, args.content)
120	
121	if __name__ == "__main__":
122	    main()
```

[시스템: read_file 결과]
파일: /home/coder/project/manage_wordpress.py (122줄)
```
  1	import os
  2	import requests
  3	from requests.auth import HTTPBasicAuth
  4	from dotenv import load_dotenv
  5	import logging
  6	import sys
  7	import argparse
  8	import time
  9	
 10	# 로깅 설정: 운영 환경에서도 추적 가능하도록 설정
 11	logging.basicConfig(
 12	    level=logging.INFO,
 13	    format='%(asctime)s [%(levelname)s] %(message)s',
 14	    handlers=[
 15	        logging.FileHandler("wordpress_manage.log"),
 16	        logging.StreamHandler(sys.stdout)
 17	    ]
 18	)
 19	logger = logging.getLogger(__name__)
 20	
 21	load_dotenv()
 22	
 23	class WordPressManager:
 24	    def __init__(self):
 25	        self.site_url = os.getenv("WP_URL", "http://mapbogi.com").rstrip('/')
 26	        self.username = os.getenv("WP_USER")
 27	        self.password = os.getenv("WP_PASS")
 28	        
 29	        if not self.username or not self.password:
 30	            logger.error("환경 변수 WP_USER 또는 WP_PASS가 설정되지 않았습니다. .env 파일을 확인하세요.")
 31	            sys.exit(1)
 32	            
 33	        self.auth = HTTPBasicAuth(self.username, self.password)
 34	        self.api_base = f"{self.site_url}/wp-json/wp/v2"
 35	
 36	    def _request(self, method, endpoint, data=None):
 37	        url = f"{self.api_base}/{endpoint}"
 38	        try:
 39	            response = requests.request(
 40	                method, url, auth=self.auth, json=data, timeout=10
 41	            )
 42	            response.raise_for_status()
 43	            return response.json()
 44	        except requests.exceptions.HTTPError as e:
 45	            logger.error(f"HTTP Error: {e} | Response: {response.text}")
 46	            return None
 47	        except Exception as e:
 48	            logger.error(f"Unexpected Error: {e}")
 49	            return None
 50	
 51	    def get_all_posts(self, per_page=100):
 52	        """모든 게시글 목록을 가져옵니다. (페이징 처리 포함)"""
 53	        posts = []
 54	        page = 1
 55	        while True:
 56	            logger.info(f"Fetching posts page {page}...")
 57	            data = self._request("GET", f"posts?per_page={per_page}&page={page}")
 58	            if not data:
 59	                break
 60	            posts.extend(data)
 61	            if len(data) < per_page:
 62	                break
 63	            page += 1
 64	        logger.info(f"Total {len(posts)} posts retrieved.")
 65	        return posts
 66	
 67	    def update_post_status(self, post_id, status="draft"):
 68	        """특정 게시글의 상태를 변경합니다. (예: 'publish' -> 'draft')"""
 69	        logger.info(f"Updating post {post_id} status to {status}...")
 70	        data = {"status": status}
 71	        result = self._request("POST", f"posts/{post_id}", data=data)
 72	        if result:
 73	            logger.info(f"Successfully updated post {post_id} to {status}.")
 74	            return True
 75	        return False
 76	
 77	    def create_post(self, title, content, status="publish", categories=None, tags=None):
 78	        """신규 게시글을 발행합니다."""
 79	        logger.info(f"Creating new post: {title}...")
 80	        data = {
 81	            "title": title,
 82	            "content": content,
 83	            "status": status,
 84	        }
 85	        if categories: data["categories"] = categories
 86	        if tags: data["tags"] = tags
 87	        
 88	        result = self._request("POST", "posts", data=data)
 89	        if result:
 90	            logger.info(f"Successfully created post ID: {result.get('id')}")
 91	            return result.get('id')
 92	        return None
 93	
 94	def main():
 95	    parser = argparse.ArgumentParser(description="WordPress Management Script")
 96	    parser.add_argument("action", choices=["list", "draft", "publish"], help="Action to perform")
 97	    parser.add_argument("--id", type=int, help="Post ID for draft action")
 98	    parser.add_argument("--title", type=str, help="Title for publish action")
 99	    parser.add_argument("--content", type=str, help="Content for publish action")
100	    
101	    args = parser.parse_args()
102	    wp = WordPressManager()
103	
104	    if args.action == "list":
105	        posts = wp.get_all_posts()
106	        for p in posts:
107	            print(f"ID: {p['id']} | Status: {p['status']} | Title: {p['title']['rendered']}")
108	            
109	    elif args.action == "draft":
110	        if not args.id:
111	            print("Error: --id is required for draft action.")
112	            return
113	        wp.update_post_status(args.id, "draft")
114	        
115	    elif args.action == "publish":
116	        if not args.title or not args.content:
117	            print("Error: --title and --content are required for publish action.")
118	            return
119	        wp.create_post(args.title, args.content)
120	
121	if __name__ == "__main__":
122	    main()
```

[시스템: list_files 결과]
디렉토리: /home/coder/project/
📄 Autonomous_Backup.md
📄 P-Reinforce_Architecture.md
📄 README.md
📄 blog_post_guidelines.md
📄 company_state.json
📄 get_wordpress_posts.py
📄 manage_wordpress.py
📄 publishflow-ai-2.89.223.vsix
📄 safe_git_push.bat
📁 sessions/
📁 venv/
📄 wordpress_api_utils.py
📄 마크다운.md

[시스템: list_files 결과]
디렉토리: /home/coder/project/
📄 Autonomous_Backup.md
📄 P-Reinforce_Architecture.md
📄 README.md
📄 blog_post_guidelines.md
📄 company_state.json
📄 get_wordpress_posts.py
📄 manage_wordpress.py
📄 publishflow-ai-2.89.223.vsix
📄 safe_git_push.bat
📁 sessions/
📁 venv/
📄 wordpress_api_utils.py
📄 마크다운.md

[시스템: list_files 결과]
디렉토리: /home/coder/project/
📄 Autonomous_Backup.md
📄 P-Reinforce_Architecture.md
📄 README.md
📄 blog_post_guidelines.md
📄 company_state.json
📄 get_wordpress_posts.py
📄 manage_wordpress.py
📄 publishflow-ai-2.89.223.vsix
📄 safe_git_push.bat
📁 sessions/
📁 venv/
📄 wordpress_api_utils.py
📄 마크다운.md
