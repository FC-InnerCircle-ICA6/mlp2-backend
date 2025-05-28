from sqlalchemy import Column, String, Boolean, Integer, Text, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .connection import Base

# User 모델
class User(Base):
    __tablename__ = "users"
    __table_args__ = {'comment': '사용자 계정 정보를 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='사용자의 고유 식별자')
    email = Column(String, unique=True, index=True, nullable=False, comment='사용자 이메일 주소 (로그인 ID 및 고유 식별자)') #
    password_hash = Column(String, nullable=False, comment='사용자의 비밀번호 해시 값')
    name = Column(String, nullable=False, comment='사용자의 표시 이름') #
    bio = Column(Text, comment='사용자의 자기소개 또는 간단한 설명') #
    language = Column(String, default='ko', nullable=False, comment='사용자 인터페이스 언어 설정 (예: ko, en)') #
    theme = Column(String, default='dark', nullable=False, comment='사용자 인터페이스 테마 설정 (예: dark, light)') #
    email_notifications = Column(Boolean, default=True, nullable=False, comment='이메일 알림 수신 여부') #
    push_notifications = Column(Boolean, default=True, nullable=False, comment='푸시 알림 수신 여부') #
    marketing_emails = Column(Boolean, default=False, nullable=False, comment='마케팅 이메일 수신 여부') #
    two_factor_auth_enabled = Column(Boolean, default=False, nullable=False, comment='2단계 인증 활성화 여부') #
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='사용자 레코드 생성 시간')
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment='사용자 레코드 마지막 업데이트 시간')

    # Relationships
    attempts = relationship("UserQuizAttempt", back_populates="user")
    progresses = relationship("UserLearningProgress", back_populates="user")
    subscriptions = relationship("UserSubscription", back_populates="user")
    login_histories = relationship("LoginHistory", back_populates="user")


# Certificate 모델
class Certificate(Base):
    __tablename__ = "certificates"
    __table_args__ = {'comment': '서비스에서 제공하는 자격증 또는 주요 학습 주제를 정의합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='자격증의 고유 식별자')
    name = Column(String, unique=True, index=True, nullable=False, comment='자격증 또는 학습 주제의 이름 (고유)') #
    description = Column(Text, comment='자격증/학습 주제에 대한 설명')
    difficulty_level = Column(Integer, comment='자격증의 난이도 (1-5, 5가 가장 어려움)') #
    category = Column(String, comment='자격증/학습 주제의 분류 (예: "자격증", "어학", "프로그래밍")')
    is_premium = Column(Boolean, default=False, nullable=False, comment='해당 자격증 관련 콘텐츠가 프리미엄 플랜에 속하는지 여부')

    # Relationships
    contents = relationship("LearningContent", back_populates="certificate")
    quizzes = relationship("Quiz", back_populates="certificate")
    attempts = relationship("UserQuizAttempt", back_populates="certificate")


# LearningContent 모델
class LearningContent(Base):
    __tablename__ = "learningcontent"
    __table_args__ = {'comment': '동영상, 문서, 텍스트 등 실제 학습 자료의 메타데이터를 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='학습 콘텐츠의 고유 식별자')
    certificate_id = Column(UUID(as_uuid=True), ForeignKey("certificates.id"), nullable=True, comment='이 콘텐츠가 속한 자격증의 ID') #
    type = Column(String, nullable=False, comment='콘텐츠의 유형 (예: "video", "document", "text", "quiz_set")')
    source_url = Column(String, unique=True, nullable=False, comment='콘텐츠의 원본 URL (예: YouTube 영상 링크, 웹사이트 URL)') #
    title = Column(String, nullable=False, comment='콘텐츠의 제목') #
    description = Column(Text, comment='콘텐츠에 대한 간단한 설명') #
    raw_text_content = Column(Text, comment='동영상 트랜스크립트, 문서 내용 등 AI 처리를 위한 원본 텍스트 데이터')
    processing_status = Column(String, default='PENDING', nullable=False, comment='AI 처리 상태 (예: "PENDING", "PROCESSING", "COMPLETED", "FAILED")')
    duration_minutes = Column(Integer, comment='비디오 콘텐츠의 길이 (분)') #
    qdrant_collection_name = Column(String, comment='이 콘텐츠의 벡터 임베딩이 저장된 Qdrant 컬렉션의 이름')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='콘텐츠 레코드 생성 시간')
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment='콘텐츠 레코드 마지막 업데이트 시간')

    # Relationships
    certificate = relationship("Certificate", back_populates="contents")
    sections = relationship("ContentSection", back_populates="content")
    quizzes = relationship("Quiz", back_populates="content")
    user_progresses = relationship("UserLearningProgress", back_populates="content")


# ContentSection 모델
class ContentSection(Base):
    __tablename__ = "contentsections"
    __table_args__ = {'comment': '긴 학습 콘텐츠를 의미 있는 작은 단위(섹션)로 분할하여 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='콘텐츠 섹션의 고유 식별자')
    content_id = Column(UUID(as_uuid=True), ForeignKey("learningcontent.id", ondelete="CASCADE"), nullable=False, comment='이 섹션이 속한 LearningContent의 ID')
    section_title = Column(String, comment='섹션의 제목 (예: 비디오 타임라인 제목)') #
    section_text = Column(Text, nullable=False, comment='섹션의 실제 텍스트 내용 (예: 비디오 트랜스크립트의 해당 부분)') #
    start_timestamp = Column(String, comment='비디오의 경우, 섹션의 시작 시간 (예: "00:00")') #
    end_timestamp = Column(String, comment='비디오의 경우, 섹션의 종료 시간')
    order_index = Column(Integer, nullable=False, comment='콘텐츠 내에서 이 섹션의 순서')
    qdrant_point_id = Column(UUID(as_uuid=True), comment='Qdrant 벡터 데이터베이스 내 이 섹션의 벡터 포인트 ID')

    # Relationships
    content = relationship("LearningContent", back_populates="sections")


# Quiz 모델
class Quiz(Base):
    __tablename__ = "quizzes"
    __table_args__ = {'comment': '생성된 퀴즈 문제와 정답, 해설 정보를 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='퀴즈 문제의 고유 식별자')
    content_id = Column(UUID(as_uuid=True), ForeignKey("learningcontent.id", ondelete="SET NULL"), nullable=True, comment='이 퀴즈가 특정 학습 콘텐츠와 연관된 경우의 ID') #
    certificate_id = Column(UUID(as_uuid=True), ForeignKey("certificates.id", ondelete="CASCADE"), nullable=True, comment='이 퀴즈가 특정 자격증 모의고사와 연관된 경우의 ID') #
    question_text = Column(Text, nullable=False, comment='퀴즈의 문제 내용') #
    options_json = Column(JSONB, comment='객관식 문제의 선택지 목록 (JSONB 형식)') #
    correct_answer_id = Column(String, nullable=False, comment='정답 선택지의 ID (예: "A", "B")') #
    explanation_text = Column(Text, comment='문제에 대한 해설 내용') #
    difficulty = Column(String, nullable=False, comment='퀴즈 문제의 난이도 (예: "easy", "normal", "hard")') #
    question_type = Column(String, nullable=False, comment='퀴즈 문제의 유형 (예: "multiple" (객관식), "subjective" (주관식), "both" (혼합))') #
    related_materials_json = Column(JSONB, comment='문제와 관련된 추가 학습 자료 링크 (JSONB 형식)') #
    generated_by_ai = Column(Boolean, default=False, nullable=False, comment='이 문제가 AI에 의해 생성되었는지 여부')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='퀴즈 레코드 생성 시간')

    # Relationships
    content = relationship("LearningContent", back_populates="quizzes")
    certificate = relationship("Certificate", back_populates="quizzes")
    user_answers = relationship("UserAnswer", back_populates="quiz")


# UserQuizAttempt 모델
class UserQuizAttempt(Base):
    __tablename__ = "userquizattempts"
    __table_args__ = {'comment': '사용자가 모의고사나 퀴즈 세트를 시도한 기록을 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='사용자 퀴즈 시도의 고유 식별자')
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment='퀴즈를 시도한 사용자의 ID')
    certificate_id = Column(UUID(as_uuid=True), ForeignKey("certificates.id", ondelete="CASCADE"), nullable=True, comment='시도한 모의고사/퀴즈 세트가 속한 자격증의 ID') #
    exam_type = Column(String, nullable=False, comment='모의고사의 유형 (예: "full", "spreadsheet", "quick", "custom")') #
    start_time = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='퀴즈 시도 시작 시간')
    end_time = Column(TIMESTAMP(timezone=True), comment='퀴즈 시도 종료 시간')
    time_taken_seconds = Column(Integer, comment='퀴즈를 푸는데 소요된 시간 (초 단위)') #
    score = Column(Integer, comment='퀴즈 시도의 최종 점수 (0-100점)') #
    total_questions = Column(Integer, nullable=False, comment='시도한 퀴즈 세트의 총 문제 수') #
    correct_count = Column(Integer, comment='맞춘 문제 수') #

    # Relationships
    user = relationship("User", back_populates="attempts")
    certificate = relationship("Certificate", back_populates="attempts")
    user_answers = relationship("UserAnswer", back_populates="attempt")


# UserAnswer 모델
class UserAnswer(Base):
    __tablename__ = "useranswers"
    __table_args__ = {'comment': '사용자가 각 퀴즈 문제에 대해 제출한 답변을 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='사용자 답변의 고유 식별자')
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("userquizattempts.id", ondelete="CASCADE"), nullable=False, comment='이 답변이 속한 사용자 퀴즈 시도의 ID')
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, comment='답변한 퀴즈 문제의 ID')
    user_selected_option_id = Column(String, comment='사용자가 선택한 객관식 선택지의 ID (예: "A", "B")') #
    is_correct = Column(Boolean, nullable=False, comment='이 답변이 정답인지 여부')
    bookmarked = Column(Boolean, default=False, nullable=False, comment='사용자가 이 문제를 북마크했는지 여부 (오답노트, 복습 기능 활용)') #
    submitted_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='답변이 제출된 시간')

    # Relationships
    attempt = relationship("UserQuizAttempt", back_populates="user_answers")
    quiz = relationship("Quiz", back_populates="user_answers")


# UserLearningProgress 모델
class UserLearningProgress(Base):
    __tablename__ = "userlearningprogress"
    __table_args__ = {'comment': '사용자의 개별 학습 콘텐츠에 대한 진행 상황을 추적합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='학습 진행 상황 기록의 고유 식별자')
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment='학습 진행 상황을 추적하는 사용자의 ID')
    content_id = Column(UUID(as_uuid=True), ForeignKey("learningcontent.id", ondelete="CASCADE"), nullable=False, comment='학습 중인 LearningContent의 ID')
    last_viewed_at = Column(TIMESTAMP(timezone=True), nullable=False, comment='사용자가 해당 콘텐츠를 마지막으로 조회한 시간')
    progress_percentage = Column(Integer, comment='콘텐츠의 진행률 (0-100%)')
    chat_history_json = Column(JSONB, comment='AI 튜터와의 채팅 기록 (JSONB 형식)') #
    summary_count = Column(Integer, default=0, nullable=False, comment='AI 요약 기능을 사용한 횟수 (플랜 제한과 연동)') #
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment='진행 기록 마지막 업데이트 시간')

    # Relationships
    user = relationship("User", back_populates="progresses")
    content = relationship("LearningContent", back_populates="user_progresses")


# SubscriptionPlan 모델
class SubscriptionPlan(Base):
    __tablename__ = "subscriptionplans"
    __table_args__ = {'comment': '서비스의 다양한 구독 플랜 정보를 정의합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='구독 플랜의 고유 식별자')
    name = Column(String, unique=True, nullable=False, comment='플랜의 이름 (예: "무료 플랜", "월 구독 플랜")') #
    price_per_month = Column(DECIMAL(10, 2), comment='월별 구독 가격 (소수점 2자리까지)') #
    features_json = Column(JSONB, comment='플랜이 제공하는 기능 목록 (JSONB 형식)') #
    fast_test_limit = Column(Integer, comment='빠른 테스트 생성 시 월별 최대 문항 수 제한') #
    slow_test_limit = Column(Integer, comment='느린 테스트 생성 시 월별 최대 문항 수 제한') #
    summary_chat_limit_type = Column(String, comment='학습 요약/채팅 요약 사용 한도 유형 (예: "monthly", "unlimited", "per_credit")') #
    summary_chat_limit_value = Column(Integer, comment='학습 요약/채팅 요약 사용 한도 값 (예: "monthly" 타입일 경우 10)') #
    is_active = Column(Boolean, default=True, nullable=False, comment='플랜이 현재 활성화되어 판매 중인지 여부')


# UserSubscription 모델
class UserSubscription(Base):
    __tablename__ = "usersubscriptions"
    __table_args__ = {'comment': '사용자의 현재 구독 정보를 저장합니다.'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='사용자 구독 기록의 고유 식별자')
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment='구독한 사용자의 ID')
    plan_id = Column(UUID(as_uuid=True), ForeignKey("subscriptionplans.id", ondelete="CASCADE"), nullable=False, comment='사용자가 구독한 플랜의 ID')
    start_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='구독 시작 날짜 및 시간')
    end_date = Column(TIMESTAMP(timezone=True), comment='구독 종료 날짜 및 시간 (만료되지 않는 구독은 NULL)')
    status = Column(String, nullable=False, comment='구독 상태 (예: "active", "cancelled", "expired", "trial")')
    credits_remaining = Column(Integer, default=0, nullable=False, comment='크레딧 기반 플랜의 경우 남은 크레딧 수량') #
    last_billing_date = Column(TIMESTAMP(timezone=True), comment='마지막 결제가 발생한 날짜 (정기 결제 플랜용)')

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")


# LoginHistory 모델
class LoginHistory(Base):
    __tablename__ = "loginhistory"
    __table_args__ = {'comment': '사용자의 로그인 시도 기록을 저장합니다 (보안 및 분석 목적).'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4(), comment='로그인 기록의 고유 식별자')
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment='로그인한 사용자의 ID')
    login_time = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='로그인 발생 날짜 및 시간') #
    ip_address = Column(String, comment='로그인 시 사용된 IP 주소')
    device_info = Column(String, comment='로그인 시 사용된 기기 정보 (예: "iPhone 13", "Windows PC")') #
    location = Column(String, comment='로그인 발생 위치 (예: "서울, 대한민국")') #

    # Relationships
    user = relationship("User", back_populates="login_histories")