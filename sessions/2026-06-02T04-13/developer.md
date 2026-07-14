# 💻 코다리 — 제공된 워드프레스 주소(http://mapbogi.com), 사용자 이름(mapbogi), 애플리케이션 비밀번호를 사용하여 워드프레스 사이트에 접속합니다. 사이트의 전반적인 상태(테마, 플러그인, 설정 등)를 확인하고, 특히 발행된 모든 글의 목록과 내용을 추출하여 검토 준비를 합니다. 애드센스 광고 코드 삽입 여부도 확인합니다.

💻 코다리: 작업 시작합니다.
워드프레스 사이트의 상태를 확인하고, 발행된 글의 목록과 내용을 추출하여 검토 준비를 하겠습니다.

먼저, 워드프레스 REST API를 사용하여 사이트의 정보를 추출하겠습니다.
```bash
<run_command>curl -X GET \
  http://mapbogi.com/wp-json/wp/v2/posts \
  -u mapbogi:VUkb3AlfKPCXK38xOKAoK8Cf \
  -H 'Content-Type: application/json'</run_command>
```
이 명령어를 실행하면, 워드프레스 사이트의 모든 글의 목록과 내용을 JSON 형식으로 추출할 수 있습니다.

다음으로, 추출된 데이터를 검토하여 애드센스 광고 코드 삽입 여부를 확인하겠습니다.
```markdown
### 발행된 글 목록

* 제목: [글 제목]
* 내용: [글 내용]
* 애드센스 광고 코드: [삽입 여부]
```
위 형식으로 추출된 데이터를 검토하여, 애드센스 승인 가치없는 콘텐츠로 거절상태인지 확인하겠습니다.

📊 평가: 진행중 — 워드프레스 사이트의 정보를 추출하여 검토 중입니다.
📝 다음 단계: 워드프레스 사이트의 정보를 추출하여 검토하고, 애드센스 승인 가치없는 콘텐츠로 거절상태인지 확인합니다.

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: `curl -X GET \
  http://mapbogi.com/wp-json/wp/v2/posts \
  -u mapbogi:VUkb3AlfKPCXK38xOKAoK8Cf \
  -`
```
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0100   795  100   795    0     0   8610      0 --:--:-- --:--:-- --:--:--  8641
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
