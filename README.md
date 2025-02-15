# django mission

🎯 미션: 간단한 할 일 관리 API 만들기
Django REST framework(DRF)를 사용하여 할 일 관리(To-Do List) API를 개발하기
제약 조건을 따라 간결하게 구현하고, RESTful API의 기본적인 기능을 익히는 것이 목표

## 📌 조건

### 모델

회원 (User)

- Django 기본 User 모델을 사용  
- username: 문자열 (최대 150자)  
- password: 문자열 (최대 128자)  
- email: 문자열 (최대 254자)  
- role: 문자열 (선택적, 최대 50자)  
- created_at: 자동 생성 날짜

할 일 (Todo)

- title: 문자열 (최대 100자)
- description: 문자열 (선택적, 최대 300자)
- is_completed: 불리언 (기본값: False)
- created_at: 자동 생성 날짜

### API

- 회원 가입 (POST /sign-up)
- 로그인 (POST /login)
- 로그아웃 (POST /logout)

- 할 일 생성 (POST /todos)
- 할 일 목록 조회 (GET /todos)
- 단일 할 일 조회 (GET /todos/{id})
- 할 일 수정 (PUT /todos/{id})
- 할 일 삭제 (DELETE /todos/{id})

### 제약 사항

JWT 인증 적용 (로그인한 사용자만 할 일 관리 가능)  
무한 스크롤링을 고려하여 페이징 기능 추가 (GET /todos)  

## 🔗 API 명세
- Django REST framework 사용 (Class-based View, APIView 또는 ViewSet 활용)
- created_at 필드는 자동 생성되도록 설정
- is_completed 값을 기본적으로 False로 설정
- Django ORM을 활용하여 CRUD 구현
- API 응답은 JSON 형식으로 반환