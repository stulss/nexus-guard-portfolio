# -*- coding: utf-8 -*-
"""Render NEXUS-GUARD Integrated Security Architecture Diagram into High-Resolution PNG."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>NEXUS-GUARD AI 엔터프라이즈 능동 방어 통합 관제 아키텍처</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');

  :root {
    --bg-main: #060911;
    --card-bg: #0d1527;
    --card-inner: #131f38;
    --border-color: #1e2e4f;
    --border-bright: #2d4575;
    
    --c-cyan: #00e5ff;
    --c-green: #00e676;
    --c-red: #ff3864;
    --c-purple: #b388ff;
    --c-gold: #ffd600;
    --c-blue: #38bdf8;
    
    --text-white: #f8fafc;
    --text-sub: #94a3b8;
    --text-dim: #64748b;
  }

  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    width: 2400px;
    height: 1350px;
    background-color: var(--bg-main);
    background-image: 
      radial-gradient(circle at 10% 15%, rgba(0, 229, 255, 0.08) 0%, transparent 45%),
      radial-gradient(circle at 90% 85%, rgba(179, 136, 255, 0.07) 0%, transparent 45%),
      linear-gradient(rgba(30, 46, 79, 0.15) 1px, transparent 1px),
      linear-gradient(90deg, rgba(30, 46, 79, 0.15) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
    font-family: 'Pretendard', sans-serif;
    color: var(--text-white);
    padding: 36px 50px;
    position: relative;
    overflow: hidden;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 22px;
    margin-bottom: 28px;
  }
  .title-wrap h4 {
    font-size: 19px;
    font-weight: 800;
    color: var(--c-cyan);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .title-wrap h4 span {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--c-cyan);
    box-shadow: 0 0 10px var(--c-cyan);
  }
  .title-wrap h1 {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -1px;
    color: var(--text-white);
    margin-bottom: 8px;
  }
  .title-wrap h1 em {
    font-style: normal;
    color: var(--c-cyan);
    text-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
  }
  .title-wrap p {
    font-size: 18px;
    color: var(--text-sub);
    font-weight: 500;
  }
  .header-badges {
    display: flex;
    gap: 12px;
  }
  .h-badge {
    padding: 8px 18px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 700;
    background: rgba(13, 21, 39, 0.9);
    border: 1px solid var(--border-bright);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .h-badge.cyan { color: var(--c-cyan); border-color: rgba(0, 229, 255, 0.4); }
  .h-badge.green { color: var(--c-green); border-color: rgba(0, 230, 118, 0.4); }
  .h-badge.purple { color: var(--c-purple); border-color: rgba(179, 136, 255, 0.4); }

  /* Main Grid */
  .grid-container {
    display: grid;
    grid-template-columns: 380px 1fr 480px;
    gap: 26px;
    height: 1070px;
  }

  /* Section Box */
  .sec-card {
    background: var(--card-bg);
    border: 1.5px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    position: relative;
  }
  .sec-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 14px;
    margin-bottom: 18px;
  }
  .sec-title {
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .sec-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 700;
    text-transform: uppercase;
  }

  /* Column 1: Attack & Ingress */
  .col-attack {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .node-box {
    background: var(--card-inner);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 18px;
    position: relative;
  }
  .node-box.red-glow {
    border-color: rgba(255, 56, 100, 0.5);
    background: linear-gradient(135deg, rgba(255,56,100,0.08) 0%, rgba(19,31,56,0.9) 100%);
  }
  .node-box.cyan-glow {
    border-color: rgba(0, 229, 255, 0.5);
    background: linear-gradient(135deg, rgba(0,229,255,0.08) 0%, rgba(19,31,56,0.9) 100%);
  }
  .node-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .node-desc {
    font-size: 13px;
    color: var(--text-sub);
    line-height: 1.5;
    margin-bottom: 12px;
  }
  .vector-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .vector-item {
    background: rgba(6, 9, 17, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .vector-tag {
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 3px;
    font-weight: 700;
  }

  /* Center Column: NEXUS-GUARD CORE SUITE (Main Attraction) */
  .col-center {
    display: flex;
    flex-direction: column;
    gap: 20px;
    background: linear-gradient(180deg, rgba(13,21,39,0.95) 0%, rgba(10,16,30,0.98) 100%);
    border: 2px solid var(--c-cyan);
    box-shadow: 0 0 40px rgba(0, 229, 255, 0.15), inset 0 0 30px rgba(0, 229, 255, 0.04);
  }
  .center-header-box {
    background: linear-gradient(90deg, rgba(0,229,255,0.15), transparent);
    border-left: 4px solid var(--c-cyan);
    padding: 14px 20px;
    border-radius: 0 8px 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .center-title h2 {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: var(--text-white);
  }
  .center-title p {
    font-size: 14px;
    color: var(--text-sub);
    margin-top: 2px;
  }
  .ownership-pill {
    background: var(--c-green);
    color: #000;
    font-weight: 900;
    font-size: 13px;
    padding: 6px 16px;
    border-radius: 20px;
    letter-spacing: -0.2px;
    box-shadow: 0 0 15px rgba(0, 230, 118, 0.5);
  }

  /* HUD Subsystems inside Core */
  .hud-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
  }
  .hud-block {
    background: var(--card-inner);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
  }
  .hud-block h4 {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--c-cyan);
  }
  .hud-stat-box {
    background: rgba(6, 9, 17, 0.7);
    border-radius: 8px;
    padding: 12px;
    margin-top: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 1.6;
    border: 1px solid rgba(255,255,255,0.06);
  }

  /* Active Defense Engine Quad */
  .engines-container {
    background: var(--card-inner);
    border: 1px solid var(--border-bright);
    border-radius: 14px;
    padding: 20px;
  }
  .engines-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 14px;
    color: var(--c-green);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .engines-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }
  .eng-card {
    background: rgba(6, 9, 17, 0.8);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 14px;
  }
  .eng-card h5 {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .eng-card p {
    font-size: 12px;
    color: var(--text-sub);
    line-height: 1.45;
  }

  /* 4-Tier AI Cascade Strip */
  .ai-cascade-strip {
    background: var(--card-inner);
    border: 1.5px solid var(--c-purple);
    border-radius: 14px;
    padding: 20px;
  }
  .ai-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 14px;
    color: var(--c-purple);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .ai-tiers-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }
  .ai-tier-card {
    background: rgba(6, 9, 17, 0.85);
    border: 1px solid rgba(179, 136, 255, 0.3);
    border-radius: 10px;
    padding: 14px;
    position: relative;
  }
  .ai-tier-card.tier1 { border-color: var(--c-cyan); }
  .ai-tier-card.tier2 { border-color: var(--c-green); }
  .ai-tier-card.tier3 { border-color: var(--c-gold); }
  .ai-tier-card.tier4 { border-color: var(--c-purple); }
  .ai-tier-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    color: var(--text-dim);
    margin-bottom: 4px;
  }
  .ai-tier-name {
    font-size: 14px;
    font-weight: 800;
    color: var(--text-white);
  }
  .ai-tier-speed {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 800;
    margin: 4px 0 6px 0;
  }
  .ai-tier-desc {
    font-size: 11px;
    color: var(--text-sub);
    line-height: 1.4;
  }

  /* Dual Containment Mode Banner */
  .dual-mode-banner {
    background: linear-gradient(90deg, rgba(255,214,0,0.1) 0%, rgba(0,230,118,0.1) 100%);
    border: 1.5px solid rgba(255, 214, 0, 0.4);
    border-radius: 12px;
    padding: 16px 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: center;
  }
  .mode-box h4 {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .mode-box p {
    font-size: 12.5px;
    color: var(--text-sub);
    line-height: 1.4;
  }

  /* Column 3: Enterprise SOC & Perimeter */
  .col-soc {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .soc-item {
    background: var(--card-inner);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .soc-item.blue-border { border-left: 4px solid var(--c-blue); }
  .soc-item.green-border { border-left: 4px solid var(--c-green); }
  .soc-item.purple-border { border-left: 4px solid var(--c-purple); }
  .soc-item.gold-border { border-left: 4px solid var(--c-gold); }

  .soc-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .soc-name {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-white);
  }
  .soc-port {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--c-cyan);
    background: rgba(0, 229, 255, 0.1);
    padding: 2px 8px;
    border-radius: 4px;
  }
  .soc-desc {
    font-size: 12.5px;
    color: var(--text-sub);
    line-height: 1.45;
  }
  .soc-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 4px;
  }
  .soc-chip {
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    background: rgba(6, 9, 17, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 3px 8px;
    border-radius: 4px;
    color: var(--text-sub);
  }

  /* Bottom Legend Footer */
  .footer-legend {
    margin-top: 20px;
    border-top: 1px solid var(--border-color);
    padding-top: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .legend-items {
    display: flex;
    gap: 28px;
    align-items: center;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
  }
  .legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 3px;
  }
  .legend-dot.red { background: var(--c-red); box-shadow: 0 0 8px var(--c-red); }
  .legend-dot.blue { background: var(--c-blue); box-shadow: 0 0 8px var(--c-blue); }
  .legend-dot.green { background: var(--c-green); box-shadow: 0 0 8px var(--c-green); }
  .legend-dot.purple { background: var(--c-purple); box-shadow: 0 0 8px var(--c-purple); }
  .legend-dot.gold { background: var(--c-gold); box-shadow: 0 0 8px var(--c-gold); }

  .footer-right {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--text-dim);
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <div class="title-wrap">
      <h4><span></span> NEXUS-GUARD Enterprise Endpoint Security Architecture</h4>
      <h1>AI 기반 엔터프라이즈 <em>능동 방어 통합 관제</em> 아키텍처</h1>
      <p>단일 독립형 관제 콘솔(Standalone)과 엔터프라이즈 분산 SOC의 텔레메트리 융합 및 0.1초 능동 격리 체계</p>
    </div>
    <div class="header-badges">
      <div class="h-badge green"><span>●</span> NIST SP 800-207 ZERO TRUST</div>
      <div class="h-badge cyan"><span>⚡</span> MITRE ATT&CK v14 MAPPING</div>
      <div class="h-badge purple"><span>🛡️</span> COMMERCIAL GRADE v2.5.0-LTS</div>
    </div>
  </div>

  <!-- Main 3-Column Topology -->
  <div class="grid-container">
    
    <!-- LEFT COLUMN: Attack Vector & Perimeter Ingress -->
    <div class="sec-card col-attack">
      <div class="sec-header">
        <div class="sec-title">
          <span>🎯</span> 공격 벡터 &amp; 진입로
        </div>
        <span class="sec-tag" style="background:rgba(255,56,100,0.15); color:var(--c-red); border:1px solid rgba(255,56,100,0.3);">
          00 · ATTACK SURFACE
        </span>
      </div>

      <!-- Kali Node -->
      <div class="node-box red-glow">
        <div class="node-title" style="color:var(--c-red);">
          <span>💀</span> 공격자 침투 호스트 (Kali Linux)
        </div>
        <div class="node-desc">
          IP: <code>192.168.3.11</code> (VMware NAT 환경) · 실측 모의 침투 수행
        </div>
        <div class="vector-list">
          <div class="vector-item">
            <span>🔍 1. 디코이 미끼 파일 프로빙</span>
            <span class="vector-tag" style="background:rgba(255,56,100,0.2); color:var(--c-red);">/.env, /.git</span>
          </div>
          <div class="vector-item">
            <span>🔑 2. 인증 브루트포스 로그인</span>
            <span class="vector-tag" style="background:rgba(255,214,0,0.2); color:var(--c-gold);">R1 스프레이</span>
          </div>
          <div class="vector-item">
            <span>💉 3. SQLi &amp; BOLA 권한 탈취</span>
            <span class="vector-tag" style="background:rgba(179,136,255,0.2); color:var(--c-purple);">IDOR / AST</span>
          </div>
          <div class="vector-item">
            <span>🤖 4. 사내 AI 프롬프트 인젝션</span>
            <span class="vector-tag" style="background:rgba(0,229,255,0.2); color:var(--c-cyan);">R2 탈옥</span>
          </div>
          <div class="vector-item">
            <span>📝 5. 웹쉘 업로드 &amp; FIM 변조</span>
            <span class="vector-tag" style="background:rgba(255,56,100,0.2); color:var(--c-red);">T1562.001</span>
          </div>
        </div>
      </div>

      <!-- Edge Boundary pfSense -->
      <div class="node-box cyan-glow">
        <div class="node-title" style="color:var(--c-cyan);">
          <span>🧱</span> 네트워크 경계 방화벽 (pfSense)
        </div>
        <div class="node-desc">
          IP: <code>192.168.3.10:5070</code> ➔ HAProxy WAF / NAT 전달
        </div>
        <div class="vector-list">
          <div class="vector-item">
            <span>GeoBlock &amp; Suricata IDS</span>
            <span class="vector-tag" style="background:rgba(0,229,255,0.15); color:var(--c-cyan);">인바운드 감시</span>
          </div>
          <div class="vector-item">
            <span>pfBlockerNG 자동 Drop 피드</span>
            <span class="vector-tag" style="background:rgba(0,230,118,0.15); color:var(--c-green);">XDR_BLOCKED</span>
          </div>
        </div>
      </div>

      <!-- Target Web/DB -->
      <div class="node-box">
        <div class="node-title" style="color:var(--c-blue);">
          <span>🏢</span> 감시 대상 포털 &amp; 엔터프라이즈 DB
        </div>
        <div class="node-desc">
          포털: <code>192.168.3.14:5070</code> (Flask) / DB: <code>3307</code> (MySQL 8.4 Docker)
        </div>
        <div style="font-size:12px; color:var(--text-sub); line-height:1.5;">
          • 43개 RDBMS 테이블 불변 감사 트리거 내장<br>
          • WAF 인그레스 미들웨어 연동 (보안 헤더 &amp; 403 차단 피드)
        </div>
      </div>

    </div>

    <!-- CENTER COLUMN: NEXUS-GUARD CORE (Hong Juhyeong Solo Development 100%) -->
    <div class="sec-card col-center">
      
      <div class="center-header-box">
        <div class="center-title">
          <h2>🛡️ NEXUS-GUARD 엔드포인트 능동 방어 관제센터</h2>
          <p>CustomTkinter 네이티브 GUI 관제 콘솔 · 60 FPS 하드웨어 가속 · 100% 단독 설계 및 풀스택 개발</p>
        </div>
        <div class="ownership-pill">★ 홍주형 단독 100% 소유권</div>
      </div>

      <!-- HUD 3-Block Row -->
      <div class="hud-grid">
        <div class="hud-block">
          <h4><span>⭕</span> 24틱 헥사 게이지</h4>
          <p style="font-size:12px; color:var(--text-sub);">100/100 점 제로 트러스트 클린 베이스라인 (0% False-Positive 무오탐 보장)</p>
          <div class="hud-stat-box">
            STATUS: <span style="color:var(--c-green); font-weight:bold;">SECURE (100점)</span><br>
            THREATS: <span style="color:var(--c-cyan);">0 ACTIVE ALERTS</span>
          </div>
        </div>
        <div class="hud-block">
          <h4><span>📡</span> 360° 위협 레이더</h4>
          <p style="font-size:12px; color:var(--text-sub);">PORTAL, KALI, pfSense, SIEM 4대 인프라 실시간 회전 스윕 빔 감시</p>
          <div class="hud-stat-box">
            SWEEP: <span style="color:var(--c-cyan);">400ms BEAM</span><br>
            BLIPS: <span style="color:var(--c-red);">DYNAMIC SHOCKWAVE</span>
          </div>
        </div>
        <div class="hud-block">
          <h4><span>📈</span> 트래픽 오실로스코프</h4>
          <p style="font-size:12px; color:var(--text-sub);">초당 KB/s 패킷 오실로스코프 (정상 48KB/s ➔ 공격 시 12.4MB/s 스파이크)</p>
          <div class="hud-stat-box">
            BASE: <span style="color:var(--c-green);">50 KB/s NORMAL</span><br>
            ALERT: <span style="color:var(--c-red);">CRIMSON SPIKE</span>
          </div>
        </div>
      </div>

      <!-- Active Defense Engines Quad -->
      <div class="engines-container">
        <div class="engines-title">
          <span>⚡</span> 4대 핵심 능동 방어(Active Defense) 엔진 서브시스템
        </div>
        <div class="engines-grid">
          <div class="eng-card">
            <h5 style="color:var(--c-red);"><span>🍯</span> 1. 디코이(허니팟) 카나리 트랩</h5>
            <p><code>/.env</code>, <code>/.git</code>, <code>/admin.php</code> 등 10개 미끼 경로 탐침 즉시 <strong>0.1초 만에 403 차단</strong> 및 방화벽 격리</p>
          </div>
          <div class="eng-card">
            <h5 style="color:var(--c-green);"><span>📁</span> 2. SHA-256 FIM 무결성 감시</h5>
            <p>핵심 소스코드 및 설정 파일의 SHA-256 해시 기준선을 10초 주기로 폴링하여 <strong>무단 위변조 0.1초 감지</strong></p>
          </div>
          <div class="eng-card">
            <h5 style="color:var(--c-purple);"><span>🛡️</span> 3. AST Guard &amp; BOLA Shield</h5>
            <p>파이썬 AST 정적 구문 분석 기반 SQLi 원천 방어 및 세부 인가(<code>users.manage</code>) 누락 결함 실시간 차단</p>
          </div>
          <div class="eng-card">
            <h5 style="color:var(--c-gold);"><span>⚡</span> 4. 1초 원상복구(Clean-up) 롤백</h5>
            <p><code>demo_runner.py --cleanup</code> 실행 시 <strong>단 0.80초 (804ms)</strong> 만에 방화벽 차단 목록 및 잠금 상태 완전 복원</p>
          </div>
        </div>
      </div>

      <!-- 4-Tier AI Cascade Strip -->
      <div class="ai-cascade-strip">
        <div class="ai-title">
          <span>🧠 4중 AI-XDR 하이브리드 추론 캐스케이드 (무중단 100% 가용성 보장)</span>
          <span style="font-family:'JetBrains Mono'; font-size:12px; color:var(--text-sub);">PRIORITY ROUTING PIPELINE</span>
        </div>
        <div class="ai-tiers-grid">
          <div class="ai-tier-card tier1">
            <div class="ai-tier-num">TIER 1 (PRIMARY)</div>
            <div class="ai-tier-name">Groq Cloud LPU</div>
            <div class="ai-tier-speed" style="color:var(--c-cyan);">⚡ 0.48s 초고속</div>
            <div class="ai-tier-desc">openai/gpt-oss-120b 기반 실시간 침해 시맨틱 트리아지</div>
          </div>
          <div class="ai-tier-card tier2">
            <div class="ai-tier-num">TIER 2 (ENTERPRISE)</div>
            <div class="ai-tier-name">NVIDIA NIM</div>
            <div class="ai-tier-speed" style="color:var(--c-green);">🧠 0.52s 심층</div>
            <div class="ai-tier-desc">Llama-3.1-Nemotron-70B 복합 공격 체인(Kill-Chain) 추론</div>
          </div>
          <div class="ai-tier-card tier3">
            <div class="ai-tier-num">TIER 3 (ON-PREMISE)</div>
            <div class="ai-tier-name">Ollama 로컬 LLM</div>
            <div class="ai-tier-speed" style="color:var(--c-gold);">🔒 폐쇄망 11434</div>
            <div class="ai-tier-desc">인터넷 단절/보안망 환경 qwen2.5:7b 자율 오프라인 추론</div>
          </div>
          <div class="ai-tier-card tier4">
            <div class="ai-tier-num">TIER 4 (FALLBACK)</div>
            <div class="ai-tier-name">내장 규칙 엔진</div>
            <div class="ai-tier-speed" style="color:var(--c-purple);">⚙️ 0.001s 인라인</div>
            <div class="ai-tier-desc">AI 인프라 전체 단절 시에도 100% 무장애 정규식 즉각 판정</div>
          </div>
        </div>
      </div>

      <!-- Dual Mode Banner -->
      <div class="dual-mode-banner">
        <div class="mode-box">
          <h4 style="color:var(--c-gold);"><span>⚡</span> [MODE A] Standalone 무중단 페일세이프</h4>
          <p>외부 SIEM/EDR 장비 부재 시에도 Windows 커널 <code>netsh advfirewall</code> (0.001s) 패킷 드롭 및 자체 FIM으로 100% 자율 방어</p>
        </div>
        <div class="mode-box">
          <h4 style="color:var(--c-green);"><span>🌐</span> [MODE B] 엔터프라이즈 SOC 풀 연동</h4>
          <p>pfSense 방화벽 커스텀 피드 동기화, Graylog GELF UDP 12201 스트리밍, Wazuh Syscheck, n8n SOAR 자동 격리</p>
        </div>
      </div>

    </div>

    <!-- RIGHT COLUMN: Enterprise SOC & Perimeter Integrations -->
    <div class="sec-card col-soc">
      <div class="sec-header">
        <div class="sec-title">
          <span>📡</span> 엔터프라이즈 SOC 연동망
        </div>
        <span class="sec-tag" style="background:rgba(0,229,255,0.15); color:var(--c-cyan); border:1px solid rgba(0,229,255,0.3);">
          03 / 04 · SOC &amp; SOAR
        </span>
      </div>

      <!-- Graylog -->
      <div class="soc-item blue-border">
        <div class="soc-head">
          <span class="soc-name">Graylog 중앙 SIEM</span>
          <span class="soc-port">GELF UDP 12201</span>
        </div>
        <div class="soc-desc">
          서버 IP: <code>192.168.3.15:9000</code> · R1~R12 스트림 보안 이벤트 실시간 수집 및 상관분석 룰 검증
        </div>
        <div class="soc-chips">
          <span class="soc-chip">NEXUS_AUTH (R1,R5~R7)</span>
          <span class="soc-chip">NEXUS_AI (R2~R4,R11~R12)</span>
          <span class="soc-chip">NEXUS_WEB (R8~R10, FIM)</span>
        </div>
      </div>

      <!-- Wazuh -->
      <div class="soc-item green-border">
        <div class="soc-head">
          <span class="soc-name">Wazuh 엔드포인트 EDR</span>
          <span class="soc-port">TCP 1514 / API 55000</span>
        </div>
        <div class="soc-desc">
          에이전트 ID: <code>001</code> · 호스트 커널 시스템 감사 및 Syscheck 디지털 인장(SHA-256) 검증
        </div>
        <div class="soc-chips">
          <span class="soc-chip">agent_fim_template.xml</span>
          <span class="soc-chip">PCI-DSS / ISMS-P 규제준수</span>
        </div>
      </div>

      <!-- n8n SOAR -->
      <div class="soc-item purple-border">
        <div class="soc-head">
          <span class="soc-name">n8n SOAR 대응 자동화</span>
          <span class="soc-port">PORT 5678 / Webhook</span>
        </div>
        <div class="soc-desc">
          침해 인시던트 발생 시 Discord 경보 전파, Jira 티켓 자동 생성 및 차단 명령 자동 라우팅
        </div>
        <div class="soc-chips">
          <span class="soc-chip">R1~R10 페이로드 템플릿 완비</span>
          <span class="soc-chip">Discord 실시간 웹훅</span>
        </div>
      </div>

      <!-- Kernel Netsh -->
      <div class="soc-item gold-border">
        <div class="soc-head">
          <span class="soc-name">Windows 커널 방화벽</span>
          <span class="soc-port">netsh advfirewall</span>
        </div>
        <div class="soc-desc">
          OS 커널 레벨 인바운드 차단 규칙 즉시 생성 (지연시간: <strong>0.001초 미만</strong>, 즉시 패킷 폐기)
        </div>
        <div class="soc-chips">
          <span class="soc-chip">127.0.0.1 화이트리스트 보호</span>
          <span class="soc-chip">1-Click 비상 호스트 격리</span>
        </div>
      </div>

      <!-- MITRE Matrix Badge -->
      <div style="background:rgba(6,9,17,0.7); border:1px solid var(--border-color); border-radius:10px; padding:14px; margin-top:auto;">
        <div style="font-size:13px; font-weight:800; color:var(--c-cyan); margin-bottom:4px;">
          🌐 MITRE ATT&CK Enterprise v14 &amp; Navigator v4.5
        </div>
        <div style="font-size:11.5px; color:var(--text-sub); line-height:1.4;">
          TA0043(정찰), TA0001(침투), TA0002(실행), TA0005(방어우회), TA0040(파괴) 5대 전술 7대 핵심 기법 실시간 매핑 레이어 완비
        </div>
      </div>

    </div>

  </div>

  <!-- Footer Legend -->
  <div class="footer-legend">
    <div class="legend-items">
      <div class="legend-item"><div class="legend-dot red"></div> 공격 트래픽 / 모의 침투 (Kali 11번)</div>
      <div class="legend-item"><div class="legend-dot blue"></div> 텔레메트리 &amp; 패킷 스트림 (GELF / Syslog)</div>
      <div class="legend-item"><div class="legend-dot green"></div> 디코이 트랩 &amp; FIM 감시 (NEXUS-GUARD 코어)</div>
      <div class="legend-item"><div class="legend-dot purple"></div> AI-XDR 상관분석 (Groq / NVIDIA / Ollama)</div>
      <div class="legend-item"><div class="legend-dot gold"></div> 커널 차단 &amp; pfBlockerNG 격리 조치</div>
    </div>
    <div class="footer-right">
      NEXUS-GUARD v2.5.0-LTS // DEVELOPED BY HONG JUHYEONG (홍주형)
    </div>
  </div>

</body>
</html>"""

def main():
    print("[*] Generating NEXUS-GUARD Integrated Security Architecture Diagram...")
    html_path = Path("temp_guard_arch.html")
    html_path.write_text(HTML_TEMPLATE, encoding="utf-8")

    out_portfolio = Path(r"C:\Users\user\Desktop\NEXUS-GUARD_포트폴리오\assets\images\NEXUS_GUARD_통합관제_아키텍처.png")
    out_portfolio_legacy = Path(r"C:\Users\user\Desktop\NEXUS-GUARD_포트폴리오\assets\images\NEXUS_WORK_시스템_아키텍처_구조도.png")
    out_guide = Path(r"C:\Users\user\Desktop\넥서스가이드\NEXUS_GUARD_통합관제_아키텍처.png")
    out_repo = Path(r"C:\Users\user\Desktop\NEXUS-GUARD\docs\presentation\NEXUS_GUARD_통합관제_아키텍처.png")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        # 2400 x 1350 (Ultra-sharp 16:9 ratio)
        context = browser.new_context(viewport={"width": 2400, "height": 1350}, device_scale_factor=1.0)
        page = context.new_page()
        page.goto(html_path.resolve().as_uri())
        page.wait_for_timeout(1000)

        # Screenshot to all required destinations
        page.screenshot(path=str(out_portfolio), full_page=True)
        page.screenshot(path=str(out_portfolio_legacy), full_page=True) # Overwrite legacy light image!
        page.screenshot(path=str(out_guide), full_page=True)
        page.screenshot(path=str(out_repo), full_page=True)

        browser.close()

    if html_path.exists():
        html_path.unlink()

    print(f"[+] Successfully rendered NEXUS-GUARD Architecture to:")
    print(f"    - {out_portfolio}")
    print(f"    - {out_portfolio_legacy} (Replaced legacy light image)")
    print(f"    - {out_guide}")
    print(f"    - {out_repo}")

if __name__ == "__main__":
    main()
