# 💻 코다리 — 워드프레스 REST API 스크립트 개발을 즉시 완료하고, 기존 문제 글의 상태 변경(비활성화/수정) 및 신규 글 발행을 위한 스크립트를 즉시 테스트하고 적용합니다. 완료 후 secretary에게 보고합니다.

💻 코다리: 작업을 즉시 진행합니다.

현재 워드프레스 REST API를 사용하여 기존 문제 글의 상태 변경과 신규 글 발행을 위한 스크립트를 개발해야 합니다. 이 스크립트는 향후 자동화된 글 관리 및 발행에 활용될 수 있도록 구성해야 합니다.

먼저, 워드프레스 REST API를 사용하여 기존 글의 목록을 추출하고, 문제 글을 식별하여 상태를 변경(비활성화/수정)해야 합니다. 이후, 신규 글 발행을 위한 스크립트를 개발하여 테스트하고 적용해야 합니다.

다음은 워드프레스 REST API를 사용하여 기존 글의 목록을 추출하고, 문제 글을 식별하여 상태를 변경하는 예시 스크립트입니다.
```python
import requests

# 워드프레스 REST API 엔드포인트
endpoint = "http://mapbogi.com/wp-json/wp/v2/posts"

# 워드프레스 REST API 인증 정보
username = "mapbogi"
password = "VUkb"

# 문제 글을 식별하기 위한 조건
problem_conditions = {
    "status": "publish",
    "categories": [1]  # 예시 카테고리 ID
}

# 워드프레스 REST API를 사용하여 기존 글의 목록을 추출
response = requests.get(endpoint, auth=(username, password))
posts = response.json()

# 문제 글을 식별하여 상태를 변경
for post in posts:
    if post["status"] == problem_conditions["status"] and post["categories"][0]["id"] == problem_conditions["categories"][0]:
        # 문제 글의 상태를 비활성화
        post["status"] = "draft"
        requests.put(endpoint + "/" + str(post["id"]), json=post, auth=(username, password))
```
이 스크립트는 워드프레스 REST API를 사용하여 기존 글의 목록을 추출하고, 문제 글을 식별하여 상태를 변경합니다. 이후, 신규 글 발행을 위한 스크립트를 개발하여 테스트하고 적용해야 합니다.

다음은 신규 글 발행을 위한 예시 스크립트입니다.
```python
import requests

# 워드프레스 REST API 엔드포인트
endpoint = "http://mapbogi.com/wp-json/wp/v2/posts"

# 워드프레스 REST API 인증 정보
username = "mapbogi"
password = "VUkb"

# 신규 글 정보
new_post = {
    "title": "신규 글 제목",
    "content": "신규 글 내용",
    "status": "publish",
    "categories": [1]  # 예시 카테고리 ID
}

# 워드프레스 REST API를 사용하여 신규 글을 발행
response = requests.post(endpoint, json=new_post, auth=(username, password))
```
이 스크립트는 워드프레스 REST API를 사용하여 신규 글을 발행합니다.

위의 두 스크립트를 개발하여 테스트하고 적용하면, 기존 문제 글의 상태를 변경하고, 신규 글을 발행할 수 있습니다.

작업이 완료되면, secretary에게 보고합니다.

📊 평가: 진행중 — 스크립트 개발 중
📝 다음 단계: 스크립트 테스트 및 적용
