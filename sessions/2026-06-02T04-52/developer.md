# 💻 코다리 — business 에이전트의 전략과 writer 에이전트의 기획안을 바탕으로, 기존 문제 글의 상태 변경(비활성화/수정) 및 신규 글 발행을 위한 워드프레스 REST API 스크립트를 준비합니다. 이 스크립트는 향후 자동화된 글 관리 및 발행에 활용될 수 있도록 구성합니다.

💻 코다리: 작업 시작하겠습니다. CEO님의 지시에 따라 business 에이전트의 전략과 writer 에이전트의 기획안을 바탕으로, 기존 글 관리 및 신규 글 발행을 위한 워드프레스 REST API 스크립트를 준비하겠습니다. 이 스크립트는 향후 자동화된 글 관리에 활용될 수 있도록 모듈화된 형태로 구성할 것입니다.

먼저, 기존에 작성했던 `get_wordpress_posts.py` 스크립트를 기반으로 워드프레스 REST API와 상호작용하는 유틸리티 함수들을 정의하겠습니다. 이 유틸리티는 다음과 같은 기능을 포함할 것입니다.

1.  **게시글 조회**: 특정 ID의 게시글 또는 모든 게시글을 조회합니다.
2.  **게시글 수정**: 특정 ID의 게시글 내용을 수정합니다 (예: 상태 변경, 내용 업데이트).
3.  **새 게시글 발행**: 새로운 게시글을 작성하고 발행합니다.

이 기능을 수행하는 `wordpress_api_utils.py` 파일을 생성하겠습니다. 이 파일은 인증 정보와 기본 API 엔드포인트를 포함하며, 각 기능별 함수를 제공할 것입니다.

<create_file path="wordpress_api_utils.py">import requests
import json
import base64

# 워드프레스 정보 (환경 변수 또는 설정 파일에서 로드하는 것이 보안상 더 좋습니다)
WORDPRESS_URL = "http://mapbogi.com"
USERNAME = "mapbogi"
APPLICATION_PASSWORD = "VUkb" # 애플리케이션 비밀번호

# REST API 엔드포인트
POSTS_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
CATEGORIES_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/categories"
TAGS_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/tags"

# 인증 헤더 생성
credentials = f"{USERNAME}:{APPLICATION_PASSWORD}"
token = base64.b64encode(credentials.encode())
AUTH_HEADERS = {
    "Authorization": f"Basic {token.decode('utf-8')}",
    "Content-Type": "application/json"
}

def get_posts(post_id=None, status=None, per_page=100, page=1):
    """
    워드프레스 게시글을 조회합니다.
    :param post_id: 조회할 게시글의 ID (선택 사항)
    :param status: 조회할 게시글의 상태 (예: 'publish', 'draft', 'private', 'trash')
    :param per_page: 페이지당 게시글 수
    :param page: 조회할 페이지 번호
    :return: 게시글 목록 또는 단일 게시글 딕셔너리
    """
    params = {"per_page": per_page, "page": page}
    if status:
        params["status"] = status

    url = POSTS_API_ENDPOINT
    if post_id:
        url = f"{POSTS_API_ENDPOINT}/{post_id}"
        params = {} # 단일 게시글 조회 시 per_page, page는 필요 없음

    try:
        response = requests.get(url, headers=AUTH_HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching posts: {e}")
        return None

def update_post(post_id, data):
    """
    특정 게시글의 내용을 수정합니다.
    :param post_id: 수정할 게시글의 ID
    :param data: 수정할 내용을 담은 딕셔너리 (예: {"status": "draft", "title": "새 제목"})
    :return: 수정된 게시글 딕셔너리 또는 None
    """
    url = f"{POSTS_API_ENDPOINT}/{post_id}"
    try:
        response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating post {post_id}: {e}")
        return None

def create_post(title, content, status="publish", categories=None, tags=None):
    """
    새로운 게시글을 생성하고 발행합니다.
    :param title: 게시글 제목
    :param content: 게시글 내용
    :param status: 게시글 상태 (기본 'publish')
    :param categories: 카테고리 ID 목록 (예: [1, 2])
    :param tags: 태그 ID 목록 (예: [10, 11])
    :return: 생성된 게시글 딕셔너리 또는 None
    """
    data = {
        "title": title,
        "content": content,
        "status": status
    }
    if categories:
        data["categories"] = categories
    if tags:
        data["tags"] = tags

    try:
        response = requests.post(POSTS_API_ENDPOINT, headers=AUTH_HEADERS, data=json.dumps(data), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating post: {e}")
        return None

def get_categories(name=None):
    """
    워드프레스 카테고리를 조회합니다.
    :param name: 특정 카테고리 이름 (선택 사항)
    :return: 카테고리 목록 딕셔너리
    """
    params = {}
    if name:
        params["search"] = name
    try:
        response = requests.get(CATEGORIES_API_ENDPOINT, headers=AUTH_HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching categories: {e}")
        return None

def get_tags(name=None):
    """
    워드프레스 태그를 조회합니다.
    :param name: 특정 태그 이름 (선택 사항)
    :return: 태그 목록 딕셔너리
    """
    params = {}
    if name:
        params["search"] = name
    try:
        response = requests.get(TAGS_API_ENDPOINT, headers=AUTH_HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tags: {e}")
        return None

if __name__ == "__main__":
    print("--- Testing WordPress API Utilities ---")

    # 모든 게시글 조회 (예시)
    print("\nGetting all published posts...")
    posts = get_posts(status="publish")
    if posts:
        for post in posts[:5]: # 상위 5개만 출력
            print(f"  ID: {post['id']}, Title: {post['title']['rendered']}, Status: {post['status']}")
    else:
        print("  No posts found or error occurred.")

    # 특정 게시글 조회 (예시: 첫 번째 게시글)
    if posts and posts[0]:
        first_post_id = posts[0]['id']
        print(f"\nGetting post with ID: {first_post_id}...")
        single_post = get_posts(post_id=first_post_id)
        if single_post:
            print(f"  Title: {single_post['title']['rendered']}, Content: {single_post['content']['rendered'][:50]}...")
        else:
            print("  Post not found or error occurred.")

    # 게시글 상태 수정 (예시: 첫 번째 게시글을 'draft'로 변경 시도 - 실제 적용은 주석 해제 후)
    # print(f"\nUpdating status of post {first_post_id} to draft...")
    # updated_post = update_post(first_post_id, {"status": "draft"})
    # if updated_post:
    #     print(f"  Updated Post ID: {updated_post['id']}, New Status: {updated_post['status']}")
    # else:
    #     print("  Failed to update post.")

    # 새 게시글 생성 (예시 - 실제 적용은 주석 해제 후)
    # print("\nCreating a new post...")
    # new_post_title = "새로운 테스트 게시글 by 코다리"
    # new_post_content = "이것은 코다리 에이전트가 워드프레스 REST API를 사용하여 생성한 테스트 게시글입니다."
    # created_post = create_post(new_post_title, new_post_content, status="draft") # 초안으로 생성
    # if created_post:
    #     print(f"  Created Post ID: {created_post['id']}, Title: {created_post['title']['rendered']}, Status: {created_post['status']}")
    # else:
    #     print("  Failed to create post.")

    # 카테고리 조회 (예시)
    print("\nGetting categories...")
    categories = get_categories()
    if categories:
        for cat in categories[:5]:
            print(f"  ID: {cat['id']}, Name: {cat['name']}")
    else:
        print("  No categories found or error occurred.")

    # 태그 조회 (예시)
    print("\nGetting tags...")
    tags = get_tags()
    if tags:
        for tag in tags[:5]:
            print(f"  ID: {tag['id']}, Name: {tag['name']}")
    else:
        print("  No tags found or error occurred.")
</create_file>

`wordpress_api_utils.py` 스크립트를 생성했습니다. 이제 이 유틸리티를 사용하여 다음 단계를 진행할 수 있습니다.

1.  **기존 문제 글 검토 및 상태 변경**: researcher 에이전트의 분석 결과가 나오면, 해당 글들의 ID를 받아 `update_post` 함수를 사용하여 'draft' (초안) 또는 'trash' (휴지통)으로 상태를 변경하거나, 내용을 수정할 수 있습니다.
2.  **신규 글 발행**: writer 에이전트가 기획한 새 글의 제목과 내용을 `create_post` 함수를 사용하여 발행할 수 있습니다.

이 스크립트는 향후 자동화된 워드프레스 글 관리를 위한 핵심 모듈이 될 것입니다.

📊 평가: 진행중 — 워드프레스 API 유틸리티 스크립트를 준비했습니다.
📝 다음 단계: researcher 에이전트의 기존 글 분석 결과와 writer 에이전트의 신규 글 기획안을 받아, 이 스크립트를 활용하여 실제 워드프레스 글 관리 작업을 수행합니다.

---
## 📁 파일 액션 결과

✅ 생성: /home/coder/project/wordpress_api_utils.py
