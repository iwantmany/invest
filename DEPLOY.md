# 배포 가이드

## 로컬 실행 (테스트)

```bash
cd investment-advisor
pip install -r requirements.txt
python app.py
```
브라우저에서 http://localhost:5000 접속

---

## 배포 옵션 (추천순)

### 1. Railway (무료, 가장 간단) ⭐
1. https://railway.app 가입
2. "New Project" → "Deploy from GitHub"
3. 이 폴더를 GitHub에 업로드 후 연결
4. 자동 배포 완료 (도메인 자동 발급)

### 2. Render (무료 플랜 있음)
1. https://render.com 가입
2. "New Web Service" → GitHub 연결
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`

### 3. PythonAnywhere (무료 플랜 있음)
1. https://www.pythonanywhere.com 가입
2. Files 탭에서 파일 업로드
3. Web 탭에서 Flask 앱 설정
4. `.pythonanywhere.com` 도메인 무료 제공

### 4. 본인 VPS (AWS/GCP/DigitalOcean 등)
```bash
# Ubuntu 서버 기준
sudo apt install python3-pip nginx -y
pip3 install -r requirements.txt gunicorn

# gunicorn으로 실행
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Nginx 리버스 프록시 설정 (선택)
```

---

## GitHub 업로드 방법

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/investment-advisor.git
git push -u origin main
```
