# 맞춤형 투자·정책 추천 웹 서비스 구축 포트폴리오

## 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트명 | 나이·금액 기반 맞춤 투자 & 정부정책 추천 웹서비스 |
| 개발 기간 | 2026년 4월 |
| 서버 환경 | Rocky Linux 8.1 / NHN Cloud |
| 접속 주소 | http://133.186.220.131:5000 |
| GitHub | https://github.com/iwantmany/invest |

---

## 서비스 소개

나이와 월 저축 가능 금액, 보유 투자금, 위험 선호도를 입력하면  
**정부 지원 정책**과 **투자 상품**을 자동으로 추천해주는 웹 서비스

### 주요 기능
- 나이·금액 조건에 맞는 정부정책 자동 필터링 (청년도약계좌, ISA, IRP 등)
- 위험 선호도 기반 투자상품 추천 (ETF, 채권, 리츠 등)
- 입력 금액 한국어 실시간 변환 표시 (예: 5,000,000 → 약 500만 원)
- 모바일 반응형 UI

---

## 기술 스택

| 구분 | 사용 기술 |
|---|---|
| 백엔드 | Python 3.8, Flask 2.0.3 |
| 프론트엔드 | HTML5, CSS3, Vanilla JavaScript |
| 서버 | Rocky Linux 8.1 (NHN Cloud VPS) |
| 배포 | GitHub → SSH → nohup 백그라운드 실행 |
| 버전 관리 | Git, GitHub |

---

## 프로젝트 구조

```
invest/
├── app.py                  # Flask 백엔드 (추천 API)
├── requirements.txt        # 패키지 의존성
├── .gitignore
├── templates/
│   └── index.html          # 메인 페이지 (한국어 UI)
└── static/
    ├── css/
    │   └── style.css       # 반응형 스타일시트
    └── js/
        └── app.js          # 프론트엔드 로직
```

---

## 구현 내용

### 1. 백엔드 (app.py)

**정부정책 데이터베이스 (6종)**

| 정책명 | 대상 나이 | 조건 |
|---|---|---|
| 청년도약계좌 | 19~34세 | 소득 7,500만원 이하, 월 최대 70만원 |
| 청년내일저축계좌 | 19~34세 | 중위소득 100% 이하 |
| ISA | 19세 이상 | 근로·사업소득자 |
| 연금저축펀드 | 전 연령 | 세액공제 연 600만원 한도 |
| IRP | 19세 이상 | 근로소득자, 세액공제 연 900만원 |
| 주택청약종합저축 | 전 연령 | 무주택 세대주 |

**투자상품 데이터베이스 (8종)**

| 상품명 | 위험도 | 기대수익 |
|---|---|---|
| S&P500 ETF | 중 | 연 7~10% |
| 나스닥100 ETF | 중상 | 연 8~15% |
| KODEX 200 ETF | 중 | 연 4~8% |
| 채권 ETF | 저 | 연 3~5% |
| 배당주 ETF | 중저 | 배당 연 3~6% |
| MMF | 최저 | 연 3~4% |
| 리츠(REITs) | 중 | 배당 연 4~7% |
| 금 ETF | 중 | 연 0~10% |

**추천 로직**
- 나이 범위 조건 필터링
- 월 납입 금액 조건 필터링
- 위험 선호도와 상품 위험도 매칭 점수 계산
- 맞춤 요약 메시지 자동 생성

### 2. 프론트엔드

- 위험 선호도 버튼 선택 UI (낮음 / 보통 / 높음)
- 금액 입력 시 실시간 한국어 변환 (만원 단위)
- 정책·투자상품 카드 그리드 렌더링
- 공식 사이트 링크 연결

### 3. API 설계

```
POST /api/recommend
Content-Type: application/json

Request:
{
  "age": 27,
  "monthly_amount": 300000,
  "total_amount": 5000000,
  "risk_level": "보통"
}

Response:
{
  "policies": [...],
  "investments": [...],
  "summary": "청년 대상 정부지원 정책을 최우선으로 활용하세요."
}
```

---

## 배포 과정

### 1단계. 로컬 개발 환경 세팅 (Windows)

```bash
# Git 초기 설정
git config --global user.email "이메일"
git config --global user.name "이름"

# 프로젝트 Git 초기화
cd investment-advisor
git init
git add .
git commit -m "첫 배포"
```

### 2단계. GitHub 업로드

```bash
git remote add origin https://github.com/iwantmany/invest.git
git branch -M main
git push -u origin main
```

### 3단계. NHN Cloud 보안그룹 설정

서버 외부 통신을 위해 콘솔에서 보안그룹 규칙 추가

| 방향 | 프로토콜 | 포트 | 대상 | 목적 |
|---|---|---|---|---|
| 송신 | 임의 | - | 0.0.0.0/0 | 외부 인터넷 접근 (패키지 설치) |
| 수신 | TCP | 5000 | 0.0.0.0/0 | 웹 서비스 외부 접속 허용 |

> 기본 설정에 송신 IPv4 전체 허용이 없어서 `dnf install` 이 타임아웃되는 문제 발생 → 보안그룹 규칙 추가로 해결

### 4단계. 서버(Rocky Linux 8.1) 환경 세팅

```bash
# SSH 접속
ssh rocky@133.186.220.131

# Python 3.8 설치 (기본 Python 3.6은 버전 호환 문제)
sudo dnf install -y python38 python38-pip git

# 코드 클론
cd ~
git clone https://github.com/iwantmany/invest.git
cd invest

# 패키지 설치
python3.8 -m pip install --user -r requirements.txt
```

> Rocky Linux 8.1 기본 Python 버전이 3.6이라 Flask 2.0.3 설치 불가 → python38 패키지 별도 설치로 해결  
> 시스템 경로 권한 문제 → `--user` 옵션으로 해결

### 5단계. 백그라운드 실행

```bash
# nohup으로 SSH 끊겨도 유지되게 실행
nohup python3 app.py > app.log 2>&1 &

# 로그 확인
cat app.log
```

### 6단계. 접속 확인

```
http://133.186.220.131:5000 → 정상 접속 완료
```

---

## 트러블슈팅 요약

| 문제 | 원인 | 해결 |
|---|---|---|
| `dnf install` 타임아웃 | NHN Cloud 보안그룹 송신 IPv4 규칙 없음 | 송신 임의 0.0.0.0/0 규칙 추가 |
| Flask 3.0.3 설치 불가 | 서버 pip가 구버전 (Python 3.6용) | requirements.txt를 Flask 2.0.3으로 다운그레이드 |
| PermissionError | 시스템 경로에 쓰기 권한 없음 | `pip install --user` 옵션 사용 |
| `firewall-cmd` 없음 | NHN Cloud는 서버 방화벽 대신 보안그룹 사용 | 콘솔에서 5000 포트 수신 규칙 추가 |
| git remote already exists | 잘못된 remote 주소 등록 | `git remote remove origin` 후 재등록 |

---

## 향후 개선 계획

- [ ] 도메인 연결 (DNS 설정)
- [ ] HTTPS 적용 (Let's Encrypt)
- [ ] Nginx + Gunicorn 프로덕션 서버 구성
- [ ] 정책 데이터 DB화 (SQLite → PostgreSQL)
- [ ] Claude AI API 연동으로 더 정교한 맞춤 추천
- [ ] 사용자 저장 기능 (로그인)
