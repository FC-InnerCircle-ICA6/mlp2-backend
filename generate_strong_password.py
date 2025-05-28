import secrets
import string

def generate_strong_password(length=20):
    # 비밀번호에 포함될 문자셋 정의
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # 최소한 하나씩 포함되도록 보장
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    # 나머지 길이를 채우기
    password += [secrets.choice(alphabet) for _ in range(length - len(password))]
    # 무작위로 섞기
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

db_password = generate_strong_password(24) # 24자 길이로 생성
print(db_password)