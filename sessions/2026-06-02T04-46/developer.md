# 💻 코다리 — 사용자가 제시한 워드프레스 글 개수(133개)와 이전에 보고된 글 개수(100개)의 차이를 확인하고, 실제 워드프레스 사이트(http://mapbogi.com)에 접속하여 글 개수를 정확히 재확인합니다. 재확인된 글 개수를 바탕으로 추출된 데이터의 유효성을 검증하고, 필요한 경우 추가 데이터 추출을 진행합니다. 재확인된 글 개수와 함께 이전 보고와의 차이점, 추가 조치 사항을 보고합니다.

💻 코다리: 작업 시작합니다.
CEO의 지시를 따르겠습니다. 워드프레스 사이트(http://mapbogi.com)에 접속하여 글 개수를 재확인하고, 추출된 데이터의 유효성을 검증하겠습니다.

먼저, 워드프레스 REST API를 사용하여 사이트의 모든 포스트를 추출하겠습니다.
```bash
<run_command>curl -X GET \
  http://mapbogi.com/wp-json/wp/v2/posts \
  -H 'Content-Type: application/json' \
  -u mapbogi:VUkb</run_command>
```
추출된 데이터를 바탕으로 글 개수를 확인하겠습니다.
```python
import json

# 추출된 데이터를 JSON으로 파싱
data = json.loads('<read_file path="~/tmp/wordpress_posts.json"/>')

# 글 개수 확인
post_count = len(data)

print(f"재확인된 글 개수: {post_count}")
```
재확인된 글 개수와 이전 보고된 글 개수(100개)의 차이를 확인하겠습니다.
```python
previous_post_count = 100
post_count_diff = post_count - previous_post_count

print(f"글 개수 차이: {post_count_diff}개")
```
추출된 데이터의 유효성을 검증하고, 필요한 경우 추가 데이터 추출을 진행하겠습니다.
```python
if post_count_diff > 0:
  print("추가 데이터 추출 필요")
  # 추가 데이터 추출을 위한 코드를 작성합니다.
else:
  print("추출된 데이터 유효")
```
재확인된 글 개수, 이전 보고와의 차이점, 추가 조치 사항을 보고하겠습니다.
```markdown
### 재확인된 글 개수
* 재확인된 글 개수: {post_count}
* 이전 보고된 글 개수: 100
* 글 개수 차이: {post_count_diff}개

### 추가 조치 사항
* {post_count_diff > 0 && "추가 데이터 추출 필요" || "추출된 데이터 유효"}
```
📊 평가: 진행중 — 워드프레스 사이트 접속 및 데이터 추출 중
📝 다음 단계: 재확인된 글 개수와 추출된 데이터의 유효성을 확인하여 추가 조치 사항을 결정합니다.

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: `curl -X GET \
  http://mapbogi.com/wp-json/wp/v2/posts \
  -H 'Content-Type: application/json' \
  -`
```
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0100   795  100   795    0     0   3347      0 --:--:-- --:--:-- --:--:--  3354
<!DOCTYPE html>
<html style="height:100%">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
<title> 301 Moved Permanently
</title><style>@media (prefers-color-scheme:dark){body{background-color:#000!important}}</style></head>
<body style="color: #444; margin:0;font: normal 14px/20px Arial, Helvetica, sans-serif; height:100%; background-color: #fff;">
<div style="height:auto; min-height:100%; ">     <div style="text-align: center; width:800px; margin-left: -400px; position:absolute; top: 30%; left:50%;">
        <h1 style="margin:0; font-size:150px; line-height:150px; font-weight:bold;">301</h1>
<h2 style="margin-top:20px;font-size: 30px;">Moved Permanently
</h2>
<p>The document has been permanently moved.</p>
</div></div></body></html>
```
_✅_

---
## 📁 파일 액션 결과

⚠️ 읽기 실패: ~/tmp/wordpress_posts.json — 파일이 존재하지 않습니다.
