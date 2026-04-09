from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ─────────────────────────────────────────
# 정부 정책 데이터베이스
# ─────────────────────────────────────────
POLICIES = [
    {
        "id": "youth_leap",
        "name": "청년도약계좌",
        "category": "정부정책",
        "icon": "🚀",
        "min_age": 19,
        "max_age": 34,
        "min_monthly": 1000,      # 월 최소 1만원
        "max_monthly": 700000,    # 월 최대 70만원
        "description": "5년 만기 적금, 정부 기여금 + 비과세 혜택",
        "benefit": "정부 기여금 월 최대 2.4만원 + 이자 비과세",
        "period": "5년",
        "income_limit": "개인소득 7,500만원 이하",
        "link": "https://www.kinfa.or.kr",
        "tags": ["비과세", "정부지원", "청년"],
        "monthly_limit": 700000,
    },
    {
        "id": "youth_tomorrow",
        "name": "청년내일저축계좌",
        "category": "정부정책",
        "icon": "💼",
        "min_age": 19,
        "max_age": 34,
        "min_monthly": 10000,
        "max_monthly": 100000,
        "description": "월 10만원 저축 시 정부가 10~30만원 추가 지원",
        "benefit": "3년 만기 시 정부 지원금 최대 1,080만원",
        "period": "3년",
        "income_limit": "기준중위소득 100% 이하 (근로/사업 소득자)",
        "link": "https://www.bokjiro.go.kr",
        "tags": ["정부지원", "청년", "저소득"],
        "monthly_limit": 100000,
    },
    {
        "id": "isa",
        "name": "ISA (개인종합자산관리계좌)",
        "category": "절세계좌",
        "icon": "💰",
        "min_age": 19,
        "max_age": 999,
        "min_monthly": 0,
        "max_monthly": 99999999,
        "description": "연간 2,000만원 한도, 다양한 금융상품 통합 관리",
        "benefit": "이익 200~400만원 비과세, 초과분 9.9% 분리과세",
        "period": "3년 이상",
        "income_limit": "근로·사업소득자 또는 농어민",
        "link": "https://www.fss.or.kr",
        "tags": ["비과세", "절세", "ETF"],
        "monthly_limit": 1666666,
    },
    {
        "id": "pension_savings",
        "name": "연금저축펀드",
        "category": "절세계좌",
        "icon": "🏦",
        "min_age": 19,
        "max_age": 999,
        "min_monthly": 0,
        "max_monthly": 150000000,
        "description": "노후 대비 + 연간 최대 66만원 세액공제",
        "benefit": "연 600만원 한도 세액공제 (소득에 따라 13.2~16.5%)",
        "period": "55세까지",
        "income_limit": "없음",
        "link": "https://www.fss.or.kr",
        "tags": ["세액공제", "노후", "ETF"],
        "monthly_limit": None,
    },
    {
        "id": "irp",
        "name": "IRP (개인형 퇴직연금)",
        "category": "절세계좌",
        "icon": "🏛️",
        "min_age": 19,
        "max_age": 999,
        "min_monthly": 0,
        "max_monthly": 150000000,
        "description": "연금저축과 합산 연 900만원까지 세액공제",
        "benefit": "연 900만원(연금저축 포함) 세액공제, 운용 수익 과세이연",
        "period": "55세까지",
        "income_limit": "근로소득자, 자영업자",
        "link": "https://www.fss.or.kr",
        "tags": ["세액공제", "퇴직연금", "노후"],
        "monthly_limit": None,
    },
    {
        "id": "housing_subscription",
        "name": "주택청약종합저축",
        "category": "정부정책",
        "icon": "🏠",
        "min_age": 19,
        "max_age": 999,
        "min_monthly": 20000,
        "max_monthly": 500000,
        "description": "아파트 청약 자격 취득 + 소득공제",
        "benefit": "연 납입액 40% 소득공제(240만원 한도), 청약 1순위 자격",
        "period": "2년 이상",
        "income_limit": "무주택 세대주 (소득공제 조건)",
        "link": "https://www.nhuf.molit.go.kr",
        "tags": ["부동산", "청약", "소득공제"],
        "monthly_limit": 500000,
    },
]

# ─────────────────────────────────────────
# 투자상품 데이터베이스
# ─────────────────────────────────────────
INVESTMENT_PRODUCTS = [
    {
        "id": "etf_sp500",
        "name": "S&P500 ETF",
        "category": "ETF",
        "icon": "📈",
        "risk": "중",
        "min_amount": 10000,
        "description": "미국 대형주 500개에 분산 투자, 역사적 연평균 10% 수익",
        "expected_return": "연 7~10%",
        "recommended_age_min": 20,
        "recommended_age_max": 50,
        "recommended_amount_min": 100000,
        "tags": ["분산투자", "장기", "미국주식"],
    },
    {
        "id": "etf_nasdaq",
        "name": "나스닥100 ETF",
        "category": "ETF",
        "icon": "💻",
        "risk": "중상",
        "min_amount": 10000,
        "description": "애플·MS·엔비디아 등 기술주 중심 ETF",
        "expected_return": "연 8~15%",
        "recommended_age_min": 20,
        "recommended_age_max": 45,
        "recommended_amount_min": 100000,
        "tags": ["기술주", "성장", "장기"],
    },
    {
        "id": "etf_korea",
        "name": "KODEX 200 ETF",
        "category": "ETF",
        "icon": "🇰🇷",
        "risk": "중",
        "min_amount": 10000,
        "description": "국내 코스피 200 대형주에 분산 투자",
        "expected_return": "연 4~8%",
        "recommended_age_min": 20,
        "recommended_age_max": 60,
        "recommended_amount_min": 50000,
        "tags": ["국내주식", "분산투자", "코스피"],
    },
    {
        "id": "bond_etf",
        "name": "채권 ETF",
        "category": "ETF",
        "icon": "🔒",
        "risk": "저",
        "min_amount": 10000,
        "description": "국채·회사채 투자, 안정적인 이자 수익",
        "expected_return": "연 3~5%",
        "recommended_age_min": 40,
        "recommended_age_max": 999,
        "recommended_amount_min": 0,
        "tags": ["안전", "채권", "이자수익"],
    },
    {
        "id": "dividend_etf",
        "name": "배당주 ETF",
        "category": "ETF",
        "icon": "💵",
        "risk": "중저",
        "min_amount": 10000,
        "description": "고배당 기업 모음, 분기/연간 배당금 수령",
        "expected_return": "배당 연 3~6% + 주가 상승",
        "recommended_age_min": 35,
        "recommended_age_max": 999,
        "recommended_amount_min": 500000,
        "tags": ["배당", "안정", "현금흐름"],
    },
    {
        "id": "mmf",
        "name": "MMF (머니마켓펀드)",
        "category": "단기상품",
        "icon": "🏧",
        "risk": "최저",
        "min_amount": 10000,
        "description": "단기 자금 운용, 수시 입출금 가능",
        "expected_return": "연 3~4%",
        "recommended_age_min": 19,
        "recommended_age_max": 999,
        "recommended_amount_min": 0,
        "tags": ["단기", "안전", "유동성"],
    },
    {
        "id": "reits",
        "name": "리츠 (REITs)",
        "category": "대안투자",
        "icon": "🏢",
        "risk": "중",
        "min_amount": 10000,
        "description": "부동산에 간접 투자, 임대 수익 배당",
        "expected_return": "배당 연 4~7% + 자산 상승",
        "recommended_age_min": 30,
        "recommended_age_max": 999,
        "recommended_amount_min": 1000000,
        "tags": ["부동산", "배당", "인플레이션헤지"],
    },
    {
        "id": "gold_etf",
        "name": "금 ETF",
        "category": "대안투자",
        "icon": "🥇",
        "risk": "중",
        "min_amount": 10000,
        "description": "금 가격 추종 ETF, 인플레이션 및 위기 헤지",
        "expected_return": "연 0~10% (변동성 높음)",
        "recommended_age_min": 30,
        "recommended_age_max": 999,
        "recommended_amount_min": 100000,
        "tags": ["안전자산", "헤지", "분산"],
    },
]


def get_policy_recommendations(age, monthly_amount, total_amount):
    """나이와 금액 기반 정부정책 추천"""
    result = []
    for p in POLICIES:
        if p["min_age"] <= age <= p["max_age"]:
            if monthly_amount >= p["min_monthly"]:
                match_score = 100
                notes = []

                # 월 한도 초과 체크
                if p["monthly_limit"] and monthly_amount > p["monthly_limit"]:
                    notes.append(f"월 최대 {p['monthly_limit']:,}원까지 납입 가능")

                result.append({**p, "match_score": match_score, "notes": notes})

    result.sort(key=lambda x: x["match_score"], reverse=True)
    return result


def get_investment_recommendations(age, monthly_amount, total_amount, risk_level):
    """나이와 금액 기반 투자상품 추천"""
    result = []

    risk_map = {"낮음": 1, "보통": 2, "높음": 3}
    user_risk = risk_map.get(risk_level, 2)

    product_risk_map = {"최저": 1, "저": 1, "중저": 2, "중": 2, "중상": 3, "고": 3}

    for p in INVESTMENT_PRODUCTS:
        if (p["recommended_age_min"] <= age <= p["recommended_age_max"] and
                total_amount >= p["recommended_amount_min"]):

            product_risk_val = product_risk_map.get(p["risk"], 2)
            # 위험 선호도와 상품 위험도 매칭
            risk_diff = abs(user_risk - product_risk_val)
            match_score = 100 - (risk_diff * 25)

            result.append({**p, "match_score": max(match_score, 30)})

    result.sort(key=lambda x: x["match_score"], reverse=True)
    return result[:5]  # 상위 5개


def generate_summary(age, monthly_amount, total_amount, risk_level):
    """맞춤 요약 메시지 생성"""
    decade = age // 10 * 10

    lines = []

    if age < 35:
        lines.append("청년 대상 정부지원 정책을 최우선으로 활용하세요.")
    if age >= 40:
        lines.append("노후 대비를 위한 연금 계좌 세액공제 혜택을 챙기세요.")
    if age >= 50:
        lines.append("안정적인 채권/배당주 비중을 늘리는 것을 권장합니다.")

    if total_amount < 100000:
        lines.append("소액이라도 ETF 적립식 투자로 시작할 수 있습니다.")
    elif total_amount >= 10000000:
        lines.append("ISA 계좌에 ETF를 담아 비과세 혜택을 극대화하세요.")

    if risk_level == "낮음":
        lines.append("안전성을 중시하므로 채권ETF·MMF를 기반으로 구성했습니다.")
    elif risk_level == "높음":
        lines.append("성장성 높은 기술주·나스닥 ETF 비중을 높게 추천했습니다.")

    return " ".join(lines) if lines else "아래 추천 상품들을 참고하여 분산 투자하세요."


# ─────────────────────────────────────────
# 라우트
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    age = int(data.get("age", 30))
    monthly_amount = int(data.get("monthly_amount", 0))
    total_amount = int(data.get("total_amount", 0))
    risk_level = data.get("risk_level", "보통")

    policies = get_policy_recommendations(age, monthly_amount, total_amount)
    investments = get_investment_recommendations(age, monthly_amount, total_amount, risk_level)
    summary = generate_summary(age, monthly_amount, total_amount, risk_level)

    return jsonify({
        "policies": policies,
        "investments": investments,
        "summary": summary,
        "age": age,
        "monthly_amount": monthly_amount,
        "total_amount": total_amount,
        "risk_level": risk_level,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
