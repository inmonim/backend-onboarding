# API 명세서

## users api

- prefix = `/users`

1. 유저 생성

- endpoint = `/`
- method = `post`
- success code = 201

- request:
  - body:
    - nickname : string, max(20), require
    - username : string, max(50), require
    - password : string, max(50), require

- response:
  - nickname : string

- exception:
  - 422:
    - username, password가 규격에 맞지 않는 경우
  - 409:
    - 이미 존재하는 nickname인 경우
    - 이미 존재하는 username인 경우

2. 유저 조회

- endpoint = `/<pk>`
- method = `get`
- success code = 200

- request:
  - path params:
    - pk : interger, require

- response:
  - user_id : int
  - nickname : string

- exception:
  - 404:
    - 존재하지 않는 유저

3. 유저 삭제

- endpoint = `/<pk>`
- method = `delete`
- success code = 204

- request:
  - path params:
    - pk : integer, require

- response:
  - None

- exception:
  - 404:
    - 존재하지 않는 유저
  - 403:
    - 다른 유저가 삭제하려고 시도함

4. 로그인

- endpoint = `/login`
- method = `post`
- success code = 200

- request:
  - body:
    - username : string, max(50), require
    - password : string, max(50), require
  
- response:
  - access_token : string
  - refresh_token : string

- exception:
  - 404:
    - 아이디 또는 비밀번호가 맞지 않음
  - 403:
    - header에 이미 토큰이 있는 채로 요청

5. 로그아웃

- endpoint = `/logout`
- method = `post`
- success code = `204`

- request:
  - None

- response:
  - None

- exception:
  - 401:
    - 토큰이 없는 채로 요청

## articles api

- prefix = `/articles`

1. 아티클 생성 / 수정

- endpoint = `/`
- method = `post, put`
- success code = `201`

- request:
  - header:
    - jwt
  - body:
    - title : string, max(255), require
    - content : string
    - is_public : int, 0 or 1, default 1
    - category_id : int, require

- response:
  - article_id : int

- exception:
  - 401:
    - 토큰 없음
  - 403:
    - 타 유저의 비공개 처리된 카테고리 id 사용
  - 404:
    - 정확하지 않은 카테고리 id

2. 아티클 페이지네이션 조회

- endpoint = `/`
- method = `get`
- success code = `200`

- request:
  - query param:
    - page : int
    - page_size : int [20, 40], default 20
    - sort_by : string [created_at, title], default created_at
    - order : string [asc, desc], default asc
    - category : int, default null
    - q : string, default null

- response:
  - list[
    {
      article_id : int,
      title : string,
      category_id : int,
      category : string,
      created_at : datetime,
      updated_at : datetime
    }
  ]

- exception:
  - 400:
    - 쿼리 파라미터가 손상되어 읽을 수 없음
  - 422:
    - 쿼리 파라미터 자체는 정상적으로 들어왔으나, 값에 대한 유효성 검사에서 문제가 발생함.

3. 아티클 상세 조회

> 카테고리를 선택하여 조회하는 경우, 하나의 id로 하위 카테고리 게시글을 검색할 수 있음.

- endpoint = `/<pk:int>`
- method = `get`
- success code = 200

- request:
  - path params:
    - article_id : int, require

- response:
  - article_id : int
  - title : string
  - content : string
  - categories : [
    [category_id, category]
  ]
  - author : {
    user_id : int,
    nickname : string
  }
  - created_at : datetime
  - updated_at : datetime

- exception :
  - 403:
    - 비공개 게시글에 다른 유저가 접근할 경우
  - 404:
    - 해당 id에 맞는 아티클이 존재하지 않음
  - 410:
    - 삭제된 아티클에 접근

4. 아티클 삭제

- endpoint = `/<pk:int>`
- method = `delete`
- success code = 204

- request:
  - header:
    - token : require

- reponse:
  - None

- exception:
  - 401:
    - 토큰이 없는 상태에서 요청
  - 403:
    - 다른 유저의 아티클에 대한 삭제를 요청
  - 404:
    - 아티클을 찾을 수 없음

5. 카테고리 생성

- endpoint = `/category`
- method = `post`
- success code = 201

- request:
  - header:
    - token : require
  - body:
    - category_name: string, max(50), require
    - is_public: int, 0 or 1, default 1
    - parent_category_id: int

- response:
  - category_id

- exception:
  - 401:
    - 토큰 없음
  - 404:
    - 부모 카테고리 id를 찾을 수 없음
  - 409:
    - (공개된 카테고리 중에서) 카테고리명이 중복됨

6. 카테고리 조회 (필요할까??)

- endpoint = `category/<pk:int>`
- method = `get`
- success code = 200

- request:
  - 

7. 카테고리 삭제

> 삭제 시에는, 하위 카테고리 id를 삭제한 카테고리의 상위 카테고리(조부모)의 자식으로 입양시키기

- endpoint = `category/<pk:int>`
- method = `delete`
- success code = 204

- request:
  - header:
    - token
  - path params:
    - category_id : int, require

- response:
  - None

- exception:
  - 403:
    - 다른 유저의 카테고리에 접근
  - 404:
    - 해당 카테고리가 없는 경우

## comments api

- prefix = `/alticles/<int:article_id>/comments`
  - 기본적으로 댓글은 아티클에 무조건 종속되어있음

1. 댓글 조회

- endpint = `/`
- method = `get`
- success code = 200

- request:
  - query params:
    - article_id : int, require

- response:
  - list[{
    user_id : int,
    nickname : string,
    comment : string,
    created_at : datetime,
    updated_at : datetime,
  }]

- exception:
  - 404:
    - 해당하는 아티클이 없는 경우

2. 댓글 생성 / 수정

- endpoint = `/`
- method = `post, put`
- success code = 201

- request:
  - header:
    - 토큰
  - body:
    - comment : string, max(1023), require

- response:
  - comment_id : int

- exception:
  - 404:
    - 게시글을 찾을 수 없음
  - 403:
    - 비공개된 게시글에 타인이 댓글을 다는 경우

3. 댓글 삭제

- endpoint = `/<int:pk>`
- method = `delete`
- success code = 204

- request:
  - header:
    - 토큰

- repsonse:
  - None

- exception:
  - 404:
    - 찾을 수 없는 댓글
  - 403:
    - 남을 댓글 삭제하려 시도
  - 410:
    - 이미 삭제된 댓글
