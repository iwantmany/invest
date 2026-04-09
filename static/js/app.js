// ── 위험도 선택 ──
let selectedRisk = '보통';

document.querySelectorAll('.risk-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.risk-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedRisk = btn.dataset.value;
  });
});

// ── 숫자 실시간 표시 ──
function formatKRW(val) {
  if (!val || isNaN(val)) return '';
  const n = parseInt(val);
  if (n >= 100000000) return `약 ${(n / 100000000).toFixed(1)}억 원`;
  if (n >= 10000000)  return `약 ${(n / 10000000).toFixed(0)}천만 원`;
  if (n >= 10000)     return `약 ${Math.floor(n / 10000)}만 원`;
  return `${n.toLocaleString()}원`;
}

document.getElementById('monthly_amount').addEventListener('input', e => {
  document.getElementById('monthly-display').textContent = formatKRW(e.target.value);
});

document.getElementById('total_amount').addEventListener('input', e => {
  document.getElementById('total-display').textContent = formatKRW(e.target.value);
});

// ── 추천 API 호출 ──
async function getRecommendations() {
  const age = parseInt(document.getElementById('age').value);
  const monthly = parseInt(document.getElementById('monthly_amount').value) || 0;
  const total = parseInt(document.getElementById('total_amount').value) || 0;

  if (!age || age < 19 || age > 100) {
    alert('나이를 올바르게 입력해주세요 (19~100세)');
    return;
  }

  document.getElementById('loading').style.display = 'block';
  document.getElementById('results').style.display = 'none';

  try {
    const res = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        age,
        monthly_amount: monthly,
        total_amount: total,
        risk_level: selectedRisk,
      }),
    });

    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert('오류가 발생했어요. 다시 시도해주세요.');
  } finally {
    document.getElementById('loading').style.display = 'none';
  }
}

// ── 결과 렌더링 ──
function renderResults(data) {
  // 요약
  document.getElementById('summary-text').textContent = data.summary;
  document.getElementById('summary-banner').style.display = 'flex';

  // 정책 카드
  const policyContainer = document.getElementById('policy-cards');
  const policyEmpty = document.getElementById('policy-empty');
  policyContainer.innerHTML = '';

  document.getElementById('policy-count').textContent = `${data.policies.length}개`;

  if (data.policies.length === 0) {
    policyEmpty.style.display = 'block';
  } else {
    policyEmpty.style.display = 'none';
    data.policies.forEach(p => {
      policyContainer.appendChild(createPolicyCard(p));
    });
  }

  // 투자 카드
  const investContainer = document.getElementById('invest-cards');
  investContainer.innerHTML = '';
  document.getElementById('invest-count').textContent = `${data.investments.length}개`;

  data.investments.forEach(p => {
    investContainer.appendChild(createInvestCard(p));
  });

  // 결과 표시
  document.getElementById('results').style.display = 'block';
  document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function createPolicyCard(p) {
  const card = document.createElement('div');
  card.className = 'rec-card';

  const notes = p.notes && p.notes.length
    ? `<p class="rec-card-note">⚠️ ${p.notes.join(' / ')}</p>`
    : '';

  const tags = p.tags.map(t => `<span class="tag">${t}</span>`).join('');

  card.innerHTML = `
    <div class="rec-card-top">
      <div class="rec-card-icon icon-policy">${p.icon}</div>
      <span class="rec-card-category cat-${p.category}">${p.category}</span>
    </div>
    <div>
      <div class="rec-card-name">${p.name}</div>
      <p class="rec-card-desc">${p.description}</p>
    </div>
    <div class="rec-card-benefit">${p.benefit}</div>
    <div class="rec-card-meta">
      ${p.period ? `<span class="meta-chip">⏱ ${p.period}</span>` : ''}
      ${p.income_limit ? `<span class="meta-chip income">조건: ${p.income_limit}</span>` : ''}
    </div>
    ${notes}
    <div class="rec-card-tags">${tags}</div>
    <a class="rec-card-link" href="${p.link}" target="_blank" rel="noopener">공식 사이트 →</a>
  `;
  return card;
}

function createInvestCard(p) {
  const card = document.createElement('div');
  card.className = 'rec-card';

  const tags = p.tags.map(t => `<span class="tag">${t}</span>`).join('');
  const riskClass = `risk-${p.risk}`;

  card.innerHTML = `
    <div class="rec-card-top">
      <div class="rec-card-icon icon-invest">${p.icon}</div>
      <span class="rec-card-category cat-${p.category}">${p.category}</span>
    </div>
    <div>
      <div class="rec-card-name">${p.name}</div>
      <p class="rec-card-desc">${p.description}</p>
    </div>
    <div class="rec-card-benefit">기대수익: ${p.expected_return}</div>
    <div class="rec-card-meta">
      <span class="risk-badge ${riskClass}">위험 ${p.risk}</span>
      ${p.min_amount ? `<span class="meta-chip">최소 ${p.min_amount.toLocaleString()}원~</span>` : ''}
    </div>
    <div class="rec-card-tags">${tags}</div>
  `;
  return card;
}

// ── 엔터키로 제출 ──
document.addEventListener('keydown', e => {
  if (e.key === 'Enter') getRecommendations();
});
