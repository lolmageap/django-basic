# django mission

🎯 미션: 간단한 할 일 관리 API 만들기
Django REST framework(DRF)를 사용하여 할 일 관리(To-Do List) API를 개발하세요.
제약 조건을 따라 간결하게 구현하고, RESTful API의 기본적인 기능을 익히는 것이 목표입니다.

📌 제약 조건
모델

Todo: 사용자가 할 일을 등록할 수 있는 엔터티
필수 필드:
title: 문자열 (최대 100자)
description: 문자열 (선택적, 최대 300자)
is_completed: 불리언 (기본값: False)
created_at: 자동 생성 날짜
기능

할 일 생성 (POST /todos/)
할 일 목록 조회 (GET /todos/)
단일 할 일 조회 (GET /todos/{id}/)
할 일 수정 (PUT /todos/{id}/)
할 일 삭제 (DELETE /todos/{id}/)
제약 사항

JWT 인증 적용 (로그인한 사용자만 할 일 관리 가능)
페이지네이션 적용 (GET /todos/ 요청 시 10개씩 반환)
특정 사용자의 할 일만 조회하도록 필터링 (GET /todos/?user_id={id})

🔗 API 명세
Django REST framework 사용 (Class-based View, APIView 또는 ViewSet 활용)
created_at 필드는 자동 생성되도록 설정
is_completed 값을 기본적으로 False로 설정
Django ORM을 활용하여 CRUD 구현
API 응답은 JSON 형식으로 반환