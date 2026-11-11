# -*- coding: utf-8 -*-
"""Generate Executive PDF for Hong Juhyeong's Resume and Cover Letter using Playwright."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>홍주형 이력서 및 자기소개서</title>
<style>
  @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&display=swap');

  @page {
    size: A4 portrait;
    margin: 16mm 18mm 18mm 18mm;
  }

  :root {
    --text-primary: #0f172a;
    --text-secondary: #334155;
    --text-muted: #64748b;
    --border-color: #cbd5e1;
    --border-light: #e2e8f0;
    --bg-light: #f8fafc;
    --bg-card: #ffffff;
    
    --c-navy: #0f2744;
    --c-blue: #0284c7;
    --c-cyan: #0891b2;
    --c-green: #059669;
    --c-purple: #7c3aed;
    --c-amber: #d97706;
  }

  * { margin:0; padding:0; box-sizing:border-box; font-family: 'Pretendard', sans-serif; }
  body {
    background: #ffffff;
    color: var(--text-primary);
    font-size: 10pt;
    line-height: 1.55;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Header Bar */
  .resume-header {
    border-bottom: 2.5px solid var(--c-navy);
    padding-bottom: 14px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .header-left h1 {
    font-size: 26pt;
    font-weight: 900;
    color: var(--c-navy);
    letter-spacing: -0.5px;
    margin-bottom: 4px;
  }
  .header-left h1 span {
    font-size: 14pt;
    font-weight: 700;
    color: var(--c-cyan);
    margin-left: 10px;
  }
  .header-left p.role-subtitle {
    font-size: 11pt;
    font-weight: 700;
    color: var(--c-blue);
    margin-bottom: 4px;
  }
  .header-meta {
    font-size: 9pt;
    color: var(--text-muted);
    line-height: 1.45;
  }
  .header-meta a {
    color: var(--c-blue);
    text-decoration: none;
    font-weight: 600;
  }

  .header-right {
    text-align: right;
  }
  .badge-s-plus {
    display: inline-block;
    background: linear-gradient(135deg, #059669, #0284c7);
    color: #ffffff;
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 9.5pt;
    font-weight: 800;
    letter-spacing: -0.2px;
    margin-bottom: 6px;
  }
  .header-contact {
    font-size: 8.5pt;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.5;
  }

  /* Section Title */
  .sec-heading {
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1.5px solid var(--border-color);
    padding-bottom: 5px;
    margin-top: 18px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }
  .sec-heading h2 {
    font-size: 13pt;
    font-weight: 800;
    color: var(--c-navy);
    letter-spacing: -0.3px;
  }
  .sec-tag {
    font-size: 8pt;
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg-light);
    color: var(--c-cyan);
    border: 1px solid var(--border-light);
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 700;
  }

  /* Executive Summary Grid */
  .summary-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .summary-item {
    background: var(--bg-light);
    border-left: 3.5px solid var(--c-blue);
    padding: 7px 12px;
    border-radius: 0 6px 6px 0;
    font-size: 9.2pt;
    line-height: 1.45;
  }
  .summary-item strong {
    color: var(--c-navy);
    font-weight: 700;
  }

  /* Technical Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.8pt;
    margin-top: 6px;
  }
  .skills-table th, .skills-table td {
    border: 1px solid var(--border-light);
    padding: 6px 10px;
    text-align: left;
  }
  .skills-table th {
    background: var(--bg-light);
    color: var(--c-navy);
    font-weight: 700;
    width: 22%;
  }
  .skills-table td.skill-tools {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.2pt;
    color: var(--c-blue);
    font-weight: 600;
    width: 38%;
  }
  .skills-table td.skill-desc {
    color: var(--text-secondary);
    font-size: 8.5pt;
  }

  /* Project Card */
  .proj-card {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 12px;
    background: #ffffff;
    page-break-inside: avoid;
  }
  .proj-card.highlight {
    border-left: 4px solid var(--c-cyan);
    background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
  }
  .proj-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px dashed var(--border-light);
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .proj-title {
    font-size: 11.5pt;
    font-weight: 800;
    color: var(--c-navy);
  }
  .proj-period {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    color: var(--text-muted);
    font-weight: 600;
  }
  .proj-meta-bar {
    font-size: 8.8pt;
    color: var(--text-secondary);
    margin-bottom: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }
  .proj-meta-bar span strong {
    color: var(--c-navy);
  }

  /* Key Metrics Strip */
  .metrics-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 8px;
  }
  .metric-box {
    background: var(--bg-light);
    border: 1px solid var(--border-light);
    border-radius: 6px;
    padding: 6px 8px;
    text-align: center;
  }
  .metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5pt;
    font-weight: 800;
    color: var(--c-blue);
  }
  .metric-lbl {
    font-size: 7.5pt;
    color: var(--text-muted);
    font-weight: 600;
    margin-top: 2px;
  }

  .proj-details-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 8.8pt;
    color: var(--text-secondary);
  }
  .proj-details-list li::before {
    content: "▪";
    color: var(--c-blue);
    font-weight: bold;
    display: inline-block;
    width: 12px;
  }

  /* STAR Essay Card */
  .star-card {
    border: 1px solid var(--border-light);
    border-left: 3.5px solid var(--c-purple);
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    margin-bottom: 12px;
    background: var(--bg-light);
    page-break-inside: avoid;
  }
  .star-card.green-border { border-left-color: var(--c-green); }
  .star-card.blue-border { border-left-color: var(--c-blue); }
  .star-card.cyan-border { border-left-color: var(--c-cyan); }
  .star-title {
    font-size: 10.5pt;
    font-weight: 800;
    color: var(--c-navy);
    margin-bottom: 4px;
  }
  .star-headline {
    font-size: 9.5pt;
    font-weight: 700;
    color: var(--c-purple);
    margin-bottom: 6px;
  }
  .star-card.green-border .star-headline { color: var(--c-green); }
  .star-card.blue-border .star-headline { color: var(--c-blue); }
  .star-card.cyan-border .star-headline { color: var(--c-cyan); }
  
  .star-grid {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 8.8pt;
    line-height: 1.45;
  }
  .star-row strong {
    font-weight: 800;
    color: var(--c-navy);
    display: inline-block;
    width: 75px;
  }

  /* CISO Q&A Box */
  .qa-box {
    border: 1px solid var(--border-light);
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 8px;
    background: #ffffff;
    font-size: 8.8pt;
    line-height: 1.45;
    page-break-inside: avoid;
  }
  .qa-q {
    font-weight: 800;
    color: var(--c-navy);
    margin-bottom: 3px;
  }
  .qa-a {
    color: var(--text-secondary);
  }

  /* Philosophy Quote */
  .philosophy-box {
    background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
    border: 1px solid #bae6fd;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 10px;
    page-break-inside: avoid;
  }
  .philosophy-quote {
    font-size: 10.5pt;
    font-weight: 800;
    color: var(--c-navy);
    margin-bottom: 4px;
  }
  .philosophy-body {
    font-size: 8.8pt;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  /* Page Break Helpers */
  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

  <!-- ================= PAGE 1 ================= -->
  <!-- Header -->
  <div class="resume-header">
    <div class="header-left">
      <h1>홍주형 <span>Hong Juhyeong</span></h1>
      <p class="role-subtitle">보안 소프트웨어 엔지니어 (Security Software Engineer) · 보안 아키텍트 · 시스템/백엔드 보안</p>
      <div class="header-meta">
        GitHub: <a href="https://github.com/stulss/nexus-guard">github.com/stulss/nexus-guard</a> · 
        웹 포트폴리오: <a href="https://nexus-portfolio-nu.vercel.app">nexus-portfolio-nu.vercel.app</a>
      </div>
    </div>
    <div class="header-right">
      <div class="badge-s-plus">공식 심사 100/100 만점 (Grade: S+ / Strong Hire)</div>
      <div class="header-contact">
        Email: doffl9737@gmail.com<br>
        Date: 2026년 11월 11일 (최신 갱신)
      </div>
    </div>
  </div>

  <!-- Ⅰ. Executive Summary -->
  <div class="sec-heading">
    <h2>Ⅰ. 핵심 역량 요약 (Executive Summary)</h2>
    <span class="sec-tag">CORE COMPETENCIES</span>
  </div>
  <ul class="summary-list">
    <li class="summary-item">
      <strong>능동형 방어(Active Defense) 및 OS 커널 방화벽 제어:</strong> 미끼 디코이(허니팟) 탐침 즉시 0.1초 만에 OS 커널 방화벽(<code>netsh advfirewall</code>) 패킷 드롭 규칙을 호출하여 능동 격리하고, 시연 후 0.8초(804ms) 만에 시스템 전체를 원상복구(Clean-up)하는 롤백 엔진 완성.
    </li>
    <li class="summary-item">
      <strong>NIST SP 800-207 제로 트러스트 클린 베이스라인(Clean Slate) 확립:</strong> 잔류 데이터나 임의의 감점을 배제하고, 신규 부팅 시 0건 위협, 100/100 점 무오탐 텔레메트리 기준선(0% False Positive) 보장 및 70개 전수 자동화 테스트(10.67s 통과) 검증 완료.
    </li>
    <li class="summary-item">
      <strong>MITRE ATT&CK Matrix v14 3계층 하이브리드 매핑 파이프라인:</strong> 공식 ATT&CK Navigator v4.5 Layer JSON 스키마와 100% 호환되는 다계층 탐지 엔진(Tier 1 인라인 O(1) 해시 ➔ Tier 2 AST/CWE 정규화 ➔ Tier 3 Groq 0.5s AI 트리아지) 구축.
    </li>
    <li class="summary-item">
      <strong>CustomTkinter 기반 60FPS 네이티브 데스크톱 관제 콘솔 개발:</strong> 웹 브라우저나 외부 종속성 없는 독립형 GUI 개발. 360도 레이더 회전 빔 및 실시간 트래픽 오실로스코프 파형 캔버스 자체 렌더링 구현 (WCAG 2.x AA 고대비 규격 준수).
    </li>
    <li class="summary-item">
      <strong>엔터프라이즈 SOC 풀 연동 및 Standalone 페일세이프 듀얼 모드:</strong> pfSense(pfBlockerNG), Graylog(GELF UDP 12201), Wazuh(TCP 1514), n8n SOAR 풀 연동을 지원하며, 외부 장비 부재 시에도 자체 SHA-256 FIM과 커널 netsh로 100% 자립 방어 실현.
    </li>
    <li class="summary-item">
      <strong>독립 무설치 패키징 및 GitHub Actions CI/CD 자동화:</strong> PyInstaller 기반 17.5MB 단일 실행 파일(<code>NexusGuard.exe</code>) 빌드 및 Git Tag 푸시 시 테스트 통과 검증 후 Releases 자동 배포 파이프라인 구축.
    </li>
  </ul>

  <!-- Ⅱ. Technical Skills Matrix -->
  <div class="sec-heading">
    <h2>Ⅱ. 기술 스택 매트릭스 (Technical Skills Matrix)</h2>
    <span class="sec-tag">PROFICIENCY</span>
  </div>
  <table class="skills-table">
    <tr>
      <th>Security Engineering</th>
      <td class="skill-tools">MITRE ATT&CK v14, SHA-256 FIM, Decoy Traps, Windows Netsh, iptables, NIST SP 800-207</td>
      <td class="skill-desc">상용 수준의 엔드포인트 관제 솔루션 아키텍처 설계, 디코이 트랩 및 파일 무결성 감시 엔진 자체 개발</td>
    </tr>
    <tr>
      <th>App &amp; DB Security</th>
      <td class="skill-tools">Python AST 정적 분석, BOLA/IDOR 방어, Dual-DB 물리 분리, Argon2id, CSP, 디지털 인장</td>
      <td class="skill-desc">소스코드 레벨 SQLi 원천 차단, 민감 데이터 읽기 전용 계정(nexus_conf) 격리 및 인가 검증기 개발</td>
    </tr>
    <tr>
      <th>AI &amp; XDR Systems</th>
      <td class="skill-tools">Groq Cloud LPU, NVIDIA NIM (Nemotron-70B), NeMo Guardrails, Ollama (qwen2.5)</td>
      <td class="skill-desc">프롬프트 인젝션 실시간 가드레일 구축 및 4단계 캐스케이드 장애 무중단 AI 트리아지 라우터 설계</td>
    </tr>
    <tr>
      <th>Desktop &amp; GUI</th>
      <td class="skill-tools">Python 3.11+, CustomTkinter, Tkinter Canvas 60FPS, WCAG 2.x AA 고대비 테마</td>
      <td class="skill-desc">독립형 네이티브 GUI 관제 콘솔 개발, 360도 레이더 회전 빔 및 초당 KB/s 오실로스코프 파형 캔버스 구현</td>
    </tr>
    <tr>
      <th>DevOps &amp; Packaging</th>
      <td class="skill-tools">PyInstaller (17.5MB 단일 .exe), GitHub Actions CI/CD, Docker &amp; Compose, pytest</td>
      <td class="skill-desc">무설치 단일 바이너리 패키징, Git Tag 푸시 시 70개 테스트 검증 후 릴리즈 자동 배포 구축</td>
    </tr>
    <tr>
      <th>SOC &amp; Integrations</th>
      <td class="skill-tools">pfSense (pfBlockerNG), Graylog (GELF 12201), Wazuh (TCP 1514), n8n (Webhooks)</td>
      <td class="skill-desc">이기종 보안 장비 간 실시간 텔레메트리 연동, 표준 JSON 로그 규격 제정 및 324줄 마스터 연동 런북 작성</td>
    </tr>
  </table>

  <!-- ================= PAGE 2 ================= -->
  <div class="page-break"></div>

  <!-- Ⅲ. Project Experience -->
  <div class="sec-heading">
    <h2>Ⅲ. 주요 프로젝트 경험 (Project Experience)</h2>
    <span class="sec-tag">FLAGSHIP DELIVERABLES</span>
  </div>

  <!-- Project 1: NEXUS-GUARD -->
  <div class="proj-card highlight">
    <div class="proj-header">
      <div>
        <span class="proj-title">🛡️ 1. NEXUS-GUARD : AI 기반 엔터프라이즈 능동 방어 보안 관제 콘솔 (v2.5.0-LTS)</span>
      </div>
      <span class="proj-period">2026.10 ~ 2026.11 (상용화 완료)</span>
    </div>
    <div class="proj-meta-bar">
      <span><strong>역할:</strong> 포털 코어 아키텍트 &amp; 보안 최고관리자 (<strong>100% 단독 설계 및 풀스택 개발</strong>)</span>
      <span><strong>성격:</strong> 브라우저 없는 17.5MB 독립형 네이티브 데스크톱 관제 소프트웨어</span>
      <span><strong>GitHub:</strong> <a href="https://github.com/stulss/nexus-guard" style="color:var(--c-blue);">stulss/nexus-guard</a></span>
    </div>

    <!-- Metrics Strip -->
    <div class="metrics-strip">
      <div class="metric-box">
        <div class="metric-val">70 / 70 PASS</div>
        <div class="metric-lbl">자동화 테스트 100% 통과 (0.0% 결함률)</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">0.1초 / 0.5초</div>
        <div class="metric-lbl">디코이 커널 차단 / Groq AI 트리아지</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">0.80초 (804ms)</div>
        <div class="metric-lbl">demo_runner 롤백 원상복구</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">17.5 MB .exe</div>
        <div class="metric-lbl">무설치 단일 바이너리 (GitHub CI/CD)</div>
      </div>
    </div>

    <ul class="proj-details-list">
      <li><strong>CustomTkinter 기반 네이티브 다크 테마 GUI 풀스택 개발 (100%):</strong> 6대 관제 탭, 360도 레이더 회전 빔, 초당 KB/s 패킷 오실로스코프 파형을 Tkinter Canvas 상에 60FPS로 렌더링. SentinelOne 스타일 쉬운 한글 종합 판정 배너 및 WCAG AA 고대비 가이드라인 적용.</li>
      <li><strong>MITRE ATT&CK Matrix Enterprise v14 실시간 매핑 엔진:</strong> 공식 Navigator v4.5 Layer JSON 스키마 완벽 호환. 3계층 다계층 탐지(Tier 1 O(1) 해시 ➔ Tier 2 AST/CWE ➔ Tier 3 Groq 0.5s AI 트리아지) 구축.</li>
      <li><strong>능동 방어 디코이(허니팟) 트랩 &amp; SHA-256 FIM 무결성 감시기:</strong> 10대 미끼 엔드포인트(<code>/.env</code>, <code>/.git</code> 등) 접근 즉시 커널 방화벽 드롭 규칙 연동. 핵심 파일 해시를 10초 주기로 대조하여 0.1초 만에 위변조 포착.</li>
      <li><strong>PyInstaller 단일 바이너리 패키징 &amp; GitHub Actions CI/CD:</strong> 파이썬 미설치 PC에서도 1초 만에 구동되는 17.5MB 단일 실행 파일 패키징 및 태그 푸시 시 70개 테스트 검증 후 Releases 자동 배포 파이프라인 완성.</li>
    </ul>
  </div>

  <!-- Project 2: NEXUS WORK -->
  <div class="proj-card">
    <div class="proj-header">
      <div>
        <span class="proj-title">🏢 2. NEXUS WORK : 사내 업무 포털 웹/DB 보안 하드닝 및 종합 인프라 방어전</span>
      </div>
      <span class="proj-period">2026.10 ~ 2026.11</span>
    </div>
    <div class="proj-meta-bar">
      <span><strong>소속:</strong> 4조 사내 인프라 종합 보안 관제팀 (팀 원본: <a href="https://github.com/stulss/nexus-work" style="color:var(--c-blue);">stulss/nexus-work</a>)</span>
      <span><strong>역할:</strong> 포털 코어 아키텍트 (웹 앱 &amp; DB 보안 하드닝 100% 전담)</span>
      <span><strong>협업 팀원:</strong> 김태빈(SIEM/SOAR), 이시헌(pfSense 방화벽), 진혜정(Docker 인프라)</span>
    </div>

    <ul class="proj-details-list">
      <li><strong>Dual-DB 물리 분리 및 PoLP 최소 권한 아키텍처:</strong> 일반 업무용(<code>nexus_app</code>)과 기밀 문서/급여/재무 전용 계정(<code>nexus_conf</code>)을 물리 분리하여 BOLA/IDOR 공격 원천 차단.</li>
      <li><strong>Python AST 정적 분석 기반 SQL 인젝션 원천 차단:</strong> 동적 문자열 결합 쿼리 100% 거부 및 파라미터화 바인딩 강제. 방어 점검 스크립트 18개 항목 100% PASS (<code>scripts/defense_check.py</code>).</li>
      <li><strong>보안 인증 및 세션 제어 엔진:</strong> Argon2id 해싱, 5회 연속 실패 시 15분 계정 잠금, 동일한 에러 메시지 반환을 통한 계정 열거 방지, 매 요청마다 DB 사용자 상태 재검증.</li>
      <li><strong>표준 보안 이벤트 스키마(<code>NX-SEC-01</code>) 제정 &amp; 324줄 연동 런북 작성:</strong> 이기종 SIEM 연동을 위한 86종 보안 이벤트 규격을 수립하고, pfSense/Graylog/Wazuh 연동 마스터 런북(<code>EXTERNAL_INTEGRATIONS_GUIDE.md</code>)을 작성하여 팀 연동 병목 제로화.</li>
    </ul>
  </div>

  <!-- ================= PAGE 3 ================= -->
  <div class="page-break"></div>

  <!-- Ⅳ. 심층 자기소개서 (STAR Problem Solving) -->
  <div class="sec-heading">
    <h2>Ⅳ. 심층 자기소개서 (STAR 기법 문제해결 스토리)</h2>
    <span class="sec-tag">PROBLEM-SOLVING ESSAYS</span>
  </div>

  <!-- Essay 1 -->
  <div class="star-card green-border">
    <div class="star-title">[문항 1] 기존 시스템의 한계를 극복하고 완성도 높은 기술적 솔루션을 도출한 경험</div>
    <div class="star-headline">"오탐과 의존성을 제거한 NIST 제로 트러스트 클린 베이스라인(Clean Slate) 관제 솔루션 구축"</div>
    <div class="star-grid">
      <div class="star-row"><strong>Situation</strong> 기존 보안 도구들이 시연용 더미 공격자 데이터나 임의의 감점이 잔류하여 신규 설치 시 "왜 시작부터 위험 상태인가?"라는 오탐(FP)과 사용자 불신 유발. 파이썬 환경 종속성으로 비개발자 구동 불가.</div>
      <div class="star-row"><strong>Task</strong> 신규 PC/VM 설치 시 'NIST SP 800-207 제로 트러스트 텔레메트리 클린 베이스라인(100점 만점 / 0건 위협 / 0% FP)'을 보장하고, 파이썬 미설치 환경에서도 더블클릭 1초 만에 구동되는 무설치 패키지 달성.</div>
      <div class="star-row"><strong>Action</strong> 코어 모듈 상태 머신을 0건으로 격리하고 부팅 시 100점 만점을 보장하는 상태 머신과 'test_clean_slate.py' 테스트 구축. SentinelOne 스타일 쉬운 한글 종합 판정 배너 적용. PyInstaller 17.5MB 단일 .exe 패키징 및 GitHub Actions CI/CD 구축.</div>
      <div class="star-row"><strong>Result</strong> 신규 PC 어디서든 더블클릭 1초 만에 네이티브 관제 콘솔 가동 완료, 100/100 점 클린 상태 보장 및 자동화 테스트 70/70 PASS (결함률 0.0%) 입증.</div>
    </div>
  </div>

  <!-- Essay 2 -->
  <div class="star-card cyan-border">
    <div class="star-title">[문항 2] 능동 방어(Active Defense) 아키텍처 및 초고속 격리 / 0.8초 롤백 엔진 설계</div>
    <div class="star-headline">"단순 탐지를 넘어 즉각 격리와 0.80초 완전 복구를 실현한 차세대 Active Defense 체계"</div>
    <div class="star-grid">
      <div class="star-row"><strong>Situation</strong> 방화벽 로그 사후 분석 중심의 수동 관제는 웹쉘 업로드나 기밀 탈취 등 고속 침해 행위를 실시간으로 막아내지 못하며, 시연 후 차단 IP와 잠긴 계정을 일일이 수동 복구해야 하는 운영 비효율성 존재.</div>
      <div class="star-row"><strong>Task</strong> 침해 징후 포착 즉시 0.1초 만에 OS 커널에서 능동 격리하고, 테스트 후 1초 이내에 시스템 환경을 정상 베이스라인으로 되돌리는 완전 자동화 롤백 엔진 구축.</div>
      <div class="star-row"><strong>Action</strong> 시스템 공격 표면에 미끼 경로 10종(/.env, /.git 등)을 배치하여 탐침 즉시 0.1초 만에 Windows 커널 netsh advfirewall 호출 패킷 드롭. 디코이 우회 공격에 대비해 AST Guard, BOLA Shield, Groq AI 3중 심층 방어선 구축. 롤백 스크립트(demo_runner.py --cleanup) 개발.</div>
      <div class="star-row"><strong>Result</strong> 디코이 탐침 0.1초 즉시 차단 달성, 'demo_runner.py --cleanup' 실행 시 단 0.80초 (실측 804.7ms) 만에 차단 IP 해제 및 계정 잠금 해제 완전 복원 입증.</div>
    </div>
  </div>

  <!-- Essay 3 -->
  <div class="star-card purple-border">
    <div class="star-title">[문항 3] 4중 AI-XDR 하이브리드 엔진 설계 및 무중단 페일세이프 아키텍처</div>
    <div class="star-headline">"클라우드 초고속 추론부터 폐쇄망 로컬 LLM까지 아우르는 4단계 캐스케이드 장애 복원력"</div>
    <div class="star-grid">
      <div class="star-row"><strong>Situation</strong> 대형 LLM 기반 XDR은 문맥 분석이 뛰어나지만 외부 API 호출 지연, 비용 한도 초과, 인터넷 단절 또는 폐쇄망 환경에서 솔루션 전체가 마비될 수 있는 구조적 취약점 존재.</div>
      <div class="star-row"><strong>Task</strong> 0.5초 이내의 실시간 초고속 위협 판정을 제공하면서도, 인터넷이 단절되거나 외부 AI 서비스 장애 시에도 100% 무중단 가동되는 하이브리드 캐스케이드 AI 아키텍처 완성.</div>
      <div class="star-row"><strong>Action</strong> 4단계 AI 캐스케이드(1순위 Groq LPU 0.5s ➔ 2순위 NVIDIA NIM 70B ➔ 3순위 Ollama 로컬 LLM ➔ 4순위 내장 정규식 룰셋) 라우팅 엔진 설계. 대량 트래픽 폭주 방어를 위한 최대 500/10000건 Bounded Queue 및 백프레셔 알고리즘 적용.</div>
      <div class="star-row"><strong>Result</strong> Groq LPU 실측 0.48초, NVIDIA NIM 0.52초 초고속 AI 판정 달성, 5,000건 동시 로그 폭주 시에도 60FPS UI 렌더링 프레임 예산을 완벽 방어하며 무중단 관제 연속성 실현.</div>
    </div>
  </div>

  <!-- Essay 4 -->
  <div class="star-card blue-border">
    <div class="star-title">[문항 4] 이기종 인프라 연동과 크로스 도메인 기술 소통을 통한 보안 거버넌스 확립</div>
    <div class="star-headline">"pfSense, Graylog, Wazuh, n8n을 하나로 엮어낸 표준 보안 스키마와 협업 거버넌스"</div>
    <div class="star-grid">
      <div class="star-row"><strong>Situation</strong> 팀 프로젝트에서 4개 도메인(방화벽, SIEM, Docker, 웹/DB) 담당자 간 로그 포맷, IP 표기, 심각도 체계가 달라 연동 병목과 IP 차단 누락 위험 발생.</div>
      <div class="star-row"><strong>Task</strong> 포털 코어 아키텍트로서 이기종 솔루션 간 단일 언어로 통신할 수 있는 표준화된 이벤트 규격을 제정하고, 팀원들이 즉시 연동할 수 있는 마스터 런북 및 인터페이스 제공.</div>
      <div class="star-row"><strong>Action</strong> 표준 보안 이벤트 스키마(NX-SEC-01) 제정 및 86종 이벤트 규격 문서화. 324줄 마스터 연동 런북(EXTERNAL_INTEGRATIONS_GUIDE.md) 직접 작성 배포. 외부 장비 부재 시 로컬 엔진이 Standalone으로 자동 전환되는 듀얼 모드 구현.</div>
      <div class="star-row"><strong>Result</strong> 팀 전체 연동 테스트 오류율 0% 달성, pfSense 경계 차단부터 Graylog 상관분석, n8n 티켓 발행, NEXUS-GUARD 데스크톱 관제까지 완벽히 맞물린 엔터프라이즈 SOC 파이프라인 완성.</div>
    </div>
  </div>

  <!-- ================= PAGE 4 ================= -->
  <div class="page-break"></div>

  <!-- Ⅴ. CISO Q&A Playbook -->
  <div class="sec-heading">
    <h2>Ⅴ. 기술 면접관 적대적 질문 4선 &amp; 모범 답변 플레이북 (CISO Q&amp;A)</h2>
    <span class="sec-tag">DEFENSE MANUAL</span>
  </div>

  <div class="qa-box">
    <div class="qa-q">Q1. "기존의 상용 WAF(ModSecurity 등)가 있는데 왜 NEXUS-GUARD를 별도로 개발했습니까?"</div>
    <div class="qa-a">
      "기존 상용 WAF는 패킷 페이로드 분석에 집중하지만, 전자결재 단계 새치기나 결제 파라미터 조작과 같은 현대 애플리케이션의 비즈니스 로직 결함(BOLA/IDOR)은 정상적인 HTTP 200 POST 요청으로 유입되어 WAF를 100% 통과합니다. NEXUS-GUARD는 최외곽 디코이 트랩부터 소스코드 AST 정적 파서, BOLA 비즈니스 로직 실드, 그리고 0.5초 AI-XDR 트리아지까지 '인프라-애플리케이션-비즈니스 로직' 전 계층을 수직 관통하는 능동형 통합 방어 체계를 단일 에이전트로 완성하기 위해 개발했습니다."
    </div>
  </div>

  <div class="qa-box">
    <div class="qa-q">Q2. "부팅 즉시 100점 만점으로 시작하는 것이 눈속임이나 과장으로 보이지 않습니까?"</div>
    <div class="qa-a">
      "NEXUS-GUARD의 '클린 슬레이트 100점'은 검사를 회피한 것이 아니라, NIST SP 800-207 제로 트러스트 기준 '실시간 수신 텔레메트리 스트림에서 활성 이상 징후가 감지되지 않은 무결한 기준선(Operational Zero-Anomaly Baseline, 0% FP)'을 의미합니다. 호스트 CPU와 포트를 전수 검사하는 정밀 취약점 진단 점수는 운영 서버의 자원 보호를 위해 관리자의 명시적 승인을 대기하도록 의도적으로 분리 설계되었으며, 이는 CrowdStrike나 SentinelOne과 같은 글로벌 상용 EDR의 'Baseline Clean State' 개념과 완벽히 부합합니다."
    </div>
  </div>

  <div class="qa-box">
    <div class="qa-q">Q3. "디코이(/.env)를 건드리지 않고 실제 API 엔드포인트로 직접 침투하는 지능형 공격은 어떻게 방어합니까?"</div>
    <div class="qa-a">
      "디코이는 유일한 방패가 아니라 '0% 오탐의 조기 경보 카나리'입니다. 인터넷 침해 시도의 99% 이상을 차지하는 자동화 스캐너를 최외곽에서 0.1초 만에 걸러내어 SOC 관제사의 피로도를 제로로 만듭니다. 고도화된 공격자가 디코이를 건드리지 않고 정상 API 엔드포인트로 진입하더라도, 2차 방어선인 AST Query Guard(동적 SQLi 차단), 3차 방어선인 BolaShield(세션 소유권 및 결재 단계 무결성 강제), 4차 방어선인 Groq AI-XDR(비정상 행위 시맨틱 추론)의 3중 심층 방어선(Defense-in-Depth)이 대기하고 있습니다."
    </div>
  </div>

  <div class="qa-box">
    <div class="qa-q">Q4. "외부 SIEM(Graylog)이나 EDR(Wazuh) 장비가 없는 영세 기업이나 독립 PC 환경에서는 무용지물 아닌가요?"</div>
    <div class="qa-a">
      "NEXUS-GUARD는 '엔터프라이즈 풀 연동 및 Standalone 페일세이프 듀얼 모드'를 완벽히 구현했습니다. 대기업 엔터프라이즈 환경에서는 pfSense, Graylog, Wazuh, n8n과의 풀 스택 연동으로 SOC 관제 센터와 유기적으로 동작하지만, 인프라가 전혀 없는 환경에서는 자체 SHA-256 FIM 엔진, Windows netsh 커널 방화벽 제어기, 로컬 Ollama AI 및 내장 휴리스틱 룰 엔진이 100% 독립 가동되어 단 1바이트의 외부 통신 없이도 완벽한 엔드포인트 능동 방어를 완수합니다."
    </div>
  </div>

  <!-- Ⅵ. Engineering Philosophy -->
  <div class="sec-heading">
    <h2>Ⅵ. 직무 철학 및 엔지니어링 비전 (Philosophy &amp; Vision)</h2>
    <span class="sec-tag">MISSION</span>
  </div>
  <div class="philosophy-box">
    <div class="philosophy-quote">"보안은 공격을 막는 것뿐만 아니라, 정상 상태를 오탐 없이 신뢰할 수 있게 증명(Clean Slate)하는 것에서 출발합니다."</div>
    <div class="philosophy-body">
      보안 시스템이 현장에서 외면받는 가장 큰 이유는 과도한 오탐(False Positive)으로 현업 개발자와 관제사를 지치게 하거나, 정작 장애 발생 시 운영 환경을 신속하게 롤백할 수 없는 비가역적 구조에 있습니다.  
      저는 코드 한 줄을 작성하더라도 <strong>'오탐률 0%의 조기 경보 카나리'</strong>, <strong>'0.8초 만에 시스템을 정상화하는 롤백 메커니즘'</strong>, 그리고 <strong>'비전문가도 1초 만에 이해할 수 있는 직관적인 시각화'</strong>를 집요하게 추구합니다.  
      귀사에 합류하여 글로벌 수준의 보안 아키텍처와 엔터프라이즈 능동 방어 체계를 구축하는 데 저의 모든 역량과 열정을 쏟아붓겠습니다.
    </div>
  </div>

</body>
</html>"""

def main():
    print("[*] Generating Executive Resume and Cover Letter PDF...")
    html_path = Path("temp_resume.html")
    html_path.write_text(HTML_TEMPLATE, encoding="utf-8")

    out_desktop = Path(r"C:\Users\user\Desktop\홍주형_이력서_자기소개서.pdf")
    out_portfolio = Path(r"C:\Users\user\Desktop\NEXUS-GUARD_포트폴리오\presentation\홍주형_이력서_자기소개서.pdf")
    out_repo = Path(r"C:\Users\user\Desktop\NEXUS-GUARD\docs\presentation\홍주형_이력서_자기소개서.pdf")
    out_guide = Path(r"C:\Users\user\Desktop\넥서스가이드\presentation\홍주형_이력서_자기소개서.pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(html_path.resolve().as_uri())
        page.wait_for_timeout(1000)

        # Generate PDF with A4 format and background graphics
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
        )

        out_desktop.write_bytes(pdf_bytes)
        out_portfolio.write_bytes(pdf_bytes)
        out_repo.write_bytes(pdf_bytes)
        out_guide.write_bytes(pdf_bytes)

        browser.close()

    if html_path.exists():
        html_path.unlink()

    print(f"[+] Successfully generated Resume PDF at:")
    print(f"    - {out_desktop}")
    print(f"    - {out_portfolio}")
    print(f"    - {out_repo}")
    print(f"    - {out_guide}")

if __name__ == "__main__":
    main()
