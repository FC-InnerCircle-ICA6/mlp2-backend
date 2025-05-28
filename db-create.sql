-- UUID (Universally Unique Identifier)를 기본 키로 사용하기 위한 확장 기능 설치
-- UUID는 고유성을 보장하며 분산 환경에서 충돌 가능성이 낮습니다.
-- PostgreSQL 13 이상에서는 기본적으로 uuid_generate_v4() 함수를 제공할 수 있습니다.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users 테이블: 사용자 계정 정보를 저장합니다.
CREATE TABLE Users (
    -- id: 사용자의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- email: 사용자 이메일 주소 (고유하며, 로그인 ID로 사용)
    email VARCHAR(255) UNIQUE NOT NULL,
    -- password_hash: 사용자의 비밀번호 해시 값 (보안을 위해 원본 비밀번호 대신 해시 저장)
    password_hash VARCHAR(255) NOT NULL,
    -- name: 사용자의 표시 이름
    name VARCHAR(100) NOT NULL,
    -- bio: 사용자의 자기소개 또는 간단한 설명 (선택 사항)
    bio TEXT,
    -- language: 사용자 인터페이스 언어 설정 (기본값: 한국어 'ko')
    language VARCHAR(10) DEFAULT 'ko' NOT NULL,
    -- theme: 사용자 인터페이스 테마 설정 (예: 'dark', 'light')
    theme VARCHAR(20) DEFAULT 'dark' NOT NULL,
    -- email_notifications: 이메일 알림 수신 여부 (기본값: TRUE)
    email_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    -- push_notifications: 푸시 알림 수신 여부 (기본값: TRUE)
    push_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    -- marketing_emails: 마케팅 이메일 수신 여부 (기본값: FALSE)
    marketing_emails BOOLEAN DEFAULT FALSE NOT NULL,
    -- two_factor_auth_enabled: 2단계 인증 활성화 여부 (기본값: FALSE)
    two_factor_auth_enabled BOOLEAN DEFAULT FALSE NOT NULL,
    -- created_at: 사용자 레코드 생성 시간 (자동으로 현재 타임스탬프 기록)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- updated_at: 사용자 레코드 마지막 업데이트 시간 (자동으로 현재 타임스탬프 기록)
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 2. Certificates 테이블: 서비스에서 제공하는 자격증 또는 주요 학습 주제를 정의합니다.
CREATE TABLE Certificates (
    -- id: 자격증의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- name: 자격증 또는 학습 주제의 이름 (고유)
    name VARCHAR(255) UNIQUE NOT NULL,
    -- description: 자격증/학습 주제에 대한 설명 (선택 사항)
    description TEXT,
    -- difficulty_level: 자격증의 난이도 (1-5, 5가 가장 어려움)
    difficulty_level INTEGER,
    -- category: 자격증/학습 주제의 분류 (예: '자격증', '어학', '프로그래밍')
    category VARCHAR(50),
    -- is_premium: 해당 자격증 관련 콘텐츠가 프리미엄 플랜에 속하는지 여부 (기본값: FALSE)
    is_premium BOOLEAN DEFAULT FALSE NOT NULL
);

-- 3. LearningContent 테이블: 동영상, 문서, 텍스트 등 실제 학습 자료의 메타데이터를 저장합니다.
CREATE TABLE LearningContent (
    -- id: 학습 콘텐츠의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- certificate_id: 이 콘텐츠가 속한 자격증의 ID (Certificates 테이블의 Foreign Key)
    certificate_id UUID REFERENCES Certificates(id) ON DELETE SET NULL, -- 자격증 삭제 시 콘텐츠는 남을 수 있음
    -- type: 콘텐츠의 유형 (예: 'video', 'document', 'text', 'quiz_set')
    type VARCHAR(50) NOT NULL,
    -- source_url: 콘텐츠의 원본 URL (예: YouTube 영상 링크, 웹사이트 URL). 고유값으로 관리
    source_url VARCHAR(2048) UNIQUE NOT NULL,
    -- title: 콘텐츠의 제목
    title VARCHAR(255) NOT NULL,
    -- description: 콘텐츠에 대한 간단한 설명
    description TEXT,
    -- raw_text_content: 동영상 트랜스크립트, 문서 내용 등 AI 처리를 위한 원본 텍스트 데이터 (선택 사항)
    raw_text_content TEXT,
    -- processing_status: AI 처리 상태 (예: 'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')
    processing_status VARCHAR(50) DEFAULT 'PENDING' NOT NULL,
    -- duration_minutes: 비디오 콘텐츠의 길이 (분)
    duration_minutes INTEGER,
    -- qdrant_collection_name: 이 콘텐츠의 벡터 임베딩이 저장된 Qdrant 컬렉션의 이름 (AI 검색 활용)
    qdrant_collection_name VARCHAR(255),
    -- created_at: 콘텐츠 레코드 생성 시간
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- updated_at: 콘텐츠 레코드 마지막 업데이트 시간
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 4. ContentSections 테이블: 긴 학습 콘텐츠를 의미 있는 작은 단위(섹션)로 분할하여 저장합니다.
--    AI가 특정 부분에 대한 퀴즈를 생성하거나 답변할 때 활용됩니다.
CREATE TABLE ContentSections (
    -- id: 콘텐츠 섹션의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- content_id: 이 섹션이 속한 LearningContent의 ID (Foreign Key). 콘텐츠 삭제 시 관련 섹션도 삭제
    content_id UUID REFERENCES LearningContent(id) ON DELETE CASCADE NOT NULL,
    -- section_title: 섹션의 제목 (예: 비디오 타임라인 제목)
    section_title VARCHAR(255),
    -- section_text: 섹션의 실제 텍스트 내용 (예: 비디오 트랜스크립트의 해당 부분)
    section_text TEXT NOT NULL,
    -- start_timestamp: 비디오의 경우, 섹션의 시작 시간 (예: '00:00', '01:23:45')
    start_timestamp VARCHAR(20),
    -- end_timestamp: 비디오의 경우, 섹션의 종료 시간
    end_timestamp VARCHAR(20),
    -- order_index: 콘텐츠 내에서 이 섹션의 순서
    order_index INTEGER NOT NULL,
    -- qdrant_point_id: Qdrant 벡터 데이터베이스 내 이 섹션의 벡터 포인트 ID (AI 검색 활용)
    qdrant_point_id UUID
);

-- 5. Quizzes 테이블: 생성된 퀴즈 문제와 정답, 해설 정보를 저장합니다.
CREATE TABLE Quizzes (
    -- id: 퀴즈 문제의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- content_id: 이 퀴즈가 특정 학습 콘텐츠와 연관된 경우의 ID (Foreign Key). 콘텐츠 삭제 시 퀴즈는 유지 가능
    content_id UUID REFERENCES LearningContent(id) ON DELETE SET NULL,
    -- certificate_id: 이 퀴즈가 특정 자격증 모의고사와 연관된 경우의 ID (Foreign Key). 자격증 삭제 시 퀴즈 삭제
    certificate_id UUID REFERENCES Certificates(id) ON DELETE CASCADE,
    -- question_text: 퀴즈의 문제 내용
    question_text TEXT NOT NULL,
    -- options_json: 객관식 문제의 선택지 목록 (JSONB 형식으로 저장)
    options_json JSONB,
    -- correct_answer_id: 정답 선택지의 ID (예: 'A', 'B')
    correct_answer_id VARCHAR(10) NOT NULL,
    -- explanation_text: 문제에 대한 해설 내용 (선택 사항)
    explanation_text TEXT,
    -- difficulty: 퀴즈 문제의 난이도 (예: 'easy', 'normal', 'hard')
    difficulty VARCHAR(20) NOT NULL,
    -- question_type: 퀴즈 문제의 유형 (예: 'multiple' (객관식), 'subjective' (주관식), 'both' (혼합))
    question_type VARCHAR(20) NOT NULL,
    -- related_materials_json: 문제와 관련된 추가 학습 자료 링크 (JSONB 형식)
    related_materials_json JSONB,
    -- generated_by_ai: 이 문제가 AI에 의해 생성되었는지 여부 (기본값: FALSE)
    generated_by_ai BOOLEAN DEFAULT FALSE NOT NULL,
    -- created_at: 퀴즈 레코드 생성 시간
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 6. UserQuizAttempts 테이블: 사용자가 모의고사나 퀴즈 세트를 시도한 기록을 저장합니다.
CREATE TABLE UserQuizAttempts (
    -- id: 사용자 퀴즈 시도의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- user_id: 퀴즈를 시도한 사용자의 ID (Users 테이블의 Foreign Key). 사용자 삭제 시 시도 기록도 삭제
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE NOT NULL,
    -- certificate_id: 시도한 모의고사/퀴즈 세트가 속한 자격증의 ID (Certificates 테이블의 Foreign Key). 자격증 삭제 시 시도 기록도 삭제
    certificate_id UUID REFERENCES Certificates(id) ON DELETE CASCADE,
    -- exam_type: 모의고사의 유형 (예: 'full', 'spreadsheet', 'quick', 'custom')
    exam_type VARCHAR(50) NOT NULL,
    -- start_time: 퀴즈 시도 시작 시간 (자동으로 현재 타임스탬프 기록)
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- end_time: 퀴즈 시도 종료 시간 (선택 사항)
    end_time TIMESTAMP WITH TIME ZONE,
    -- time_taken_seconds: 퀴즈를 푸는데 소요된 시간 (초 단위)
    time_taken_seconds INTEGER,
    -- score: 퀴즈 시도의 최종 점수 (0-100점)
    score INTEGER,
    -- total_questions: 시도한 퀴즈 세트의 총 문제 수
    total_questions INTEGER NOT NULL,
    -- correct_count: 맞춘 문제 수
    correct_count INTEGER
);

-- 7. UserAnswers 테이블: 사용자가 각 퀴즈 문제에 대해 제출한 답변을 저장합니다.
CREATE TABLE UserAnswers (
    -- id: 사용자 답변의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- attempt_id: 이 답변이 속한 사용자 퀴즈 시도의 ID (UserQuizAttempts 테이블의 Foreign Key). 시도 기록 삭제 시 답변도 삭제
    attempt_id UUID REFERENCES UserQuizAttempts(id) ON DELETE CASCADE NOT NULL,
    -- quiz_id: 답변한 퀴즈 문제의 ID (Quizzes 테이블의 Foreign Key). 퀴즈 문제 삭제 시 답변도 삭제
    quiz_id UUID REFERENCES Quizzes(id) ON DELETE CASCADE NOT NULL,
    -- user_selected_option_id: 사용자가 선택한 객관식 선택지의 ID (예: 'A', 'B')
    user_selected_option_id VARCHAR(10),
    -- is_correct: 이 답변이 정답인지 여부
    is_correct BOOLEAN NOT NULL,
    -- bookmarked: 사용자가 이 문제를 북마크했는지 여부 (오답노트, 복습 기능 활용)
    bookmarked BOOLEAN DEFAULT FALSE NOT NULL,
    -- submitted_at: 답변이 제출된 시간 (자동으로 현재 타임스탬프 기록)
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 8. UserLearningProgress 테이블: 사용자의 개별 학습 콘텐츠에 대한 진행 상황을 추적합니다.
CREATE TABLE UserLearningProgress (
    -- id: 학습 진행 상황 기록의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- user_id: 학습 진행 상황을 추적하는 사용자의 ID (Users 테이블의 Foreign Key). 사용자 삭제 시 진행 기록도 삭제
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE NOT NULL,
    -- content_id: 학습 중인 LearningContent의 ID (Foreign Key). 콘텐츠 삭제 시 진행 기록도 삭제
    content_id UUID REFERENCES LearningContent(id) ON DELETE CASCADE NOT NULL,
    -- last_viewed_at: 사용자가 해당 콘텐츠를 마지막으로 조회한 시간
    last_viewed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    -- progress_percentage: 콘텐츠의 진행률 (0-100%)
    progress_percentage INTEGER,
    -- chat_history_json: AI 튜터와의 채팅 기록 (JSONB 형식으로 저장)
    chat_history_json JSONB,
    -- summary_count: AI 요약 기능을 사용한 횟수 (플랜 제한과 연동)
    summary_count INTEGER DEFAULT 0 NOT NULL,
    -- updated_at: 진행 기록 마지막 업데이트 시간
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 9. SubscriptionPlans 테이블: 서비스의 다양한 구독 플랜 정보를 정의합니다.
CREATE TABLE SubscriptionPlans (
    -- id: 구독 플랜의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- name: 플랜의 이름 (예: '무료 플랜', '월 구독 플랜', '크레딧 구매', 'Enterprise') (고유)
    name VARCHAR(100) UNIQUE NOT NULL,
    -- price_per_month: 월별 구독 가격 (소수점 2자리까지)
    price_per_month DECIMAL(10, 2),
    -- features_json: 플랜이 제공하는 기능 목록 (JSONB 형식)
    features_json JSONB,
    -- fast_test_limit: 빠른 테스트 생성 시 월별 최대 문항 수 제한 (INTEGER 또는 NULL)
    fast_test_limit INTEGER,
    -- slow_test_limit: 느린 테스트 생성 시 월별 최대 문항 수 제한 (INTEGER 또는 NULL)
    slow_test_limit INTEGER,
    -- summary_chat_limit_type: 학습 요약/채팅 요약 사용 한도 유형 (예: 'monthly', 'unlimited', 'per_credit')
    summary_chat_limit_type VARCHAR(50),
    -- summary_chat_limit_value: 학습 요약/채팅 요약 사용 한도 값 (예: 'monthly' 타입일 경우 10)
    summary_chat_limit_value INTEGER,
    -- is_active: 플랜이 현재 활성화되어 판매 중인지 여부 (기본값: TRUE)
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);

-- 10. UserSubscriptions 테이블: 사용자의 현재 구독 정보를 저장합니다.
CREATE TABLE UserSubscriptions (
    -- id: 사용자 구독 기록의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- user_id: 구독한 사용자의 ID (Users 테이블의 Foreign Key). 사용자 삭제 시 구독 정보도 삭제
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE NOT NULL,
    -- plan_id: 사용자가 구독한 플랜의 ID (SubscriptionPlans 테이블의 Foreign Key). 플랜 삭제 시 구독 정보도 삭제
    plan_id UUID REFERENCES SubscriptionPlans(id) ON DELETE CASCADE NOT NULL,
    -- start_date: 구독 시작 날짜 및 시간 (자동으로 현재 타임스탬프 기록)
    start_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- end_date: 구독 종료 날짜 및 시간 (만료되지 않는 구독은 NULL)
    end_date TIMESTAMP WITH TIME ZONE,
    -- status: 구독 상태 (예: 'active', 'cancelled', 'expired', 'trial')
    status VARCHAR(50) NOT NULL,
    -- credits_remaining: 크레딧 기반 플랜의 경우 남은 크레딧 수량 (기본값: 0)
    credits_remaining INTEGER DEFAULT 0 NOT NULL,
    -- last_billing_date: 마지막 결제가 발생한 날짜 (정기 결제 플랜용)
    last_billing_date TIMESTAMP WITH TIME ZONE
);

-- 11. LoginHistory 테이블: 사용자의 로그인 시도 기록을 저장합니다 (보안 및 분석 목적).
CREATE TABLE LoginHistory (
    -- id: 로그인 기록의 고유 식별자 (Primary Key, UUID v4로 자동 생성)
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- user_id: 로그인한 사용자의 ID (Users 테이블의 Foreign Key). 사용자 삭제 시 로그인 기록도 삭제
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE NOT NULL,
    -- login_time: 로그인 발생 날짜 및 시간 (자동으로 현재 타임스탬프 기록)
    login_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- ip_address: 로그인 시 사용된 IP 주소
    ip_address VARCHAR(45), -- IPv4는 15자, IPv6는 45자까지 가능
    -- device_info: 로그인 시 사용된 기기 정보 (예: 'iPhone 13', 'Windows PC')
    device_info VARCHAR(255),
    -- location: 로그인 발생 위치 (예: '서울, 대한민국')
    location VARCHAR(255)
);

-- 인덱스 추가 (쿼리 성능 최적화를 위한 인덱스)
-- 자주 조회되거나 외래 키로 사용되는 컬럼에 인덱스를 생성합니다.
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_learningcontent_certificate_id ON LearningContent(certificate_id);
CREATE INDEX idx_contentsections_content_id ON ContentSections(content_id);
CREATE INDEX idx_quizzes_content_id ON Quizzes(content_id);
CREATE INDEX idx_quizzes_certificate_id ON Quizzes(certificate_id);
CREATE INDEX idx_userquizattempts_user_id ON UserQuizAttempts(user_id);
CREATE INDEX idx_userquizattempts_certificate_id ON UserQuizAttempts(certificate_id);
CREATE INDEX idx_useranswers_attempt_id ON UserAnswers(attempt_id);
CREATE INDEX idx_useranswers_quiz_id ON UserAnswers(quiz_id);
CREATE INDEX idx_userlearningprogress_user_id ON UserLearningProgress(user_id);
CREATE INDEX idx_userlearningprogress_content_id ON UserLearningProgress(content_id);
CREATE INDEX idx_usersubscriptions_user_id ON UserSubscriptions(user_id);
CREATE INDEX idx_usersubscriptions_plan_id ON UserSubscriptions(plan_id);
CREATE INDEX idx_loginhistory_user_id ON LoginHistory(user_id);