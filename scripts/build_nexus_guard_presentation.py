# -*- coding: utf-8 -*-
"""Generate NEXUS-GUARD Master Presentation Deck (PPTX) and convert to PDF.

- 12 High-Impact Presentation Slides
- 16:9 Widescreen (13.333 x 7.5 inches)
- Deep Slate / Cyberpunk Enterprise Dark Theme
- High-Resolution Architecture Diagrams Embedded
- Automated PDF Conversion via PowerPoint COM
"""
import os
import sys
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Paths
PORTFOLIO_DIR = Path(r"C:\Users\user\Desktop\NEXUS-GUARD_포트폴리오")
IMG_GUARD_ARCH = PORTFOLIO_DIR / "assets" / "images" / "NEXUS_GUARD_통합관제_아키텍처.png"
IMG_TEAM_ARCH = PORTFOLIO_DIR / "assets" / "images" / "team_architecture_original.png"

# Color Palette (CrowdStrike / SentinelOne Dark SOC Style)
C_BG = RGBColor(8, 12, 22)           # #080c16 Deep Navy
C_CARD_BG = RGBColor(15, 23, 42)      # #0f172a Slate 900
C_CARD_INNER = RGBColor(22, 33, 56)   # #162138
C_BORDER = RGBColor(38, 56, 92)       # Slate Border
C_CYAN = RGBColor(0, 229, 255)        # #00e5ff Cyber Cyan
C_GREEN = RGBColor(0, 230, 118)       # #00e676 Neon Green
C_RED = RGBColor(255, 56, 100)        # #ff3864 Crimson Alert
C_PURPLE = RGBColor(179, 136, 255)    # #b388ff AI Purple
C_GOLD = RGBColor(255, 214, 0)        # #ffd600 Warning Gold
C_TEXT_WHITE = RGBColor(248, 250, 252)
C_TEXT_SUB = RGBColor(148, 163, 184)
C_TEXT_DIM = RGBColor(100, 116, 139)


def set_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    return bg


def add_header(slide, badge_text, title_text, subtitle_text, badge_color=C_CYAN):
    # Badge Box
    b_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf = b_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"●  {badge_text.upper()}"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = badge_color

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    # Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.35))
    tf = s_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = subtitle_text
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEXT_SUB


def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    return card


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Cover
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Ambient Card
    add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=C_CARD_BG, border_color=C_CYAN)

    tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(10.7), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "●  COMMERCIAL GRADE v2.5.0-LTS  //  NIST SP 800-207 ZERO TRUST"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    tb2 = s1.shapes.add_textbox(Inches(1.3), Inches(1.8), Inches(10.7), Inches(1.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "NEXUS-GUARD"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    p2 = tf2.add_paragraph()
    p2.text = "AI 기반 엔터프라이즈 능동 방어 보안 관제 콘솔"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN

    tb3 = s1.shapes.add_textbox(Inches(1.3), Inches(3.4), Inches(10.7), Inches(0.8))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "단일 독립형 관제 시스템(Standalone)과 엔터프라이즈 분산 SOC의 텔레메트리 융합 및 0.1초 능동 격리 체계"
    p.font.size = Pt(14)
    p.font.color.rgb = C_TEXT_SUB

    # Author & Info Grid
    add_card(s1, Inches(1.3), Inches(4.5), Inches(10.733), Inches(1.6), bg_color=C_CARD_INNER, border_color=C_BORDER)

    tb_auth = s1.shapes.add_textbox(Inches(1.6), Inches(4.65), Inches(5.0), Inches(1.3))
    tf_auth = tb_auth.text_frame
    tf_auth.word_wrap = True
    p = tf_auth.paragraphs[0]
    p.text = "발표자 / 설계자: 홍주형 (Hong Juhyeong)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    p = tf_auth.add_paragraph()
    p.text = "포털 코어 아키텍트 & 보안 최고관리자 (단독 100% 설계 및 풀스택 개발)"
    p.font.size = Pt(12)
    p.font.color.rgb = C_GREEN

    p = tf_auth.add_paragraph()
    p.text = "GitHub: https://github.com/stulss/nexus-guard"
    p.font.size = Pt(11)
    p.font.color.rgb = C_CYAN

    tb_metrics = s1.shapes.add_textbox(Inches(7.0), Inches(4.65), Inches(4.7), Inches(1.3))
    tf_m = tb_metrics.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "핵심 실측 지표"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    p = tf_m.add_paragraph()
    p.text = "• 자동화 테스트 70/70 PASS (결함률 0.0%) | 클린 슬레이트 100점"
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_SUB

    p = tf_m.add_paragraph()
    p.text = "• 0.1초 커널 방화벽 격리 | 0.8초(804ms) 원상복구 | 17.5MB 단일 실행 파일"
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 2: Background & Problems
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "PROJECT BACKGROUND & PROBLEM STATEMENT", "기존 보안 관제의 3대 한계와 패러다임 전환", "사후 로그 분석 중심의 수동 관제에서 0.1초 즉시 격리 및 자율 복구 체계로의 도약")

    cards_data = [
        ("한계 1. 파편화된 다중 관제 화면", C_RED, "5~6개 도구 분산으로 인한 골든타임 상실", [
            "• pfSense, Graylog, Wazuh, n8n, 웹 콘솔이 각각 분리 운영됨",
            "• 위협 발생 시 관제사가 여러 도구를 오가며 수동 상관분석 수행",
            "• 복합 킬체인 공격에 대한 평균 대응 시간(MTTR) 지연"
        ]),
        ("한계 2. 사후 탐지 중심의 수동 방어", C_GOLD, "패킷이 이미 침투한 뒤에야 로그 분석", [
            "• 디코이/카나리 트랩 부재로 웹쉘 및 환경변수 탈취 사전 방어 불가",
            "• BOLA/IDOR 등 비즈니스 로직 결함은 상용 WAF를 100% 정상 통과",
            "• 공격자 IP 차단을 수동 승인에 의존하여 확산 저지 실패"
        ]),
        ("한계 3. 무거운 설치 종속성과 오탐 잔류", C_CYAN, "새 환경 배포 불가 및 '눈속임 감점' 문제", [
            "• 복잡한 파이썬 환경 및 그래픽 라이브러리 없이는 타 PC 구동 불가",
            "• 첫 실행 시 과거 더미 공격자 데이터가 잔류하여 오탐(False-Positive) 유발",
            "• NIST 제로 트러스트 기준을 충족하는 클린 기준선 부재"
        ])
    ]

    for i, (title, col, sub, items) in enumerate(cards_data):
        left = Inches(0.8 + i * 3.98)
        add_card(s2, left, Inches(1.9), Inches(3.78), Inches(4.9), border_color=col)
        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(3.38), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_WHITE
        p2.space_before = Pt(6)
        p2.space_after = Pt(14)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = it
            p_it.font.size = Pt(11)
            p_it.font.color.rgb = C_TEXT_SUB
            p_it.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: Team Architecture vs NEXUS-GUARD Solo Evolution
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "ARCHITECTURE COMPARISON // R&R BREAKDOWN", "팀 원본 아키텍처(03/38) ➔ NEXUS-GUARD 단독 고도화", "4인 팀 협업 인프라에서 도출된 한계를 극복하고 단일 완성형 SOC 콘솔로 집대성")

    # Left: Team Arch
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), border_color=C_BORDER)
    tb_t = s3.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.35), Inches(0.6))
    p = tb_t.text_frame.paragraphs[0]
    p.text = "🏢 팀 프로젝트 원본: NEXUS WORK (발표 03/38)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    if IMG_TEAM_ARCH.exists():
        s3.shapes.add_picture(str(IMG_TEAM_ARCH), Inches(1.0), Inches(2.6), width=Inches(5.35))

    tb_t_desc = s3.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(5.35), Inches(0.9))
    tf = tb_t_desc.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• 5대 분산 구간: 00 Kali(11번) ➔ 01 pfSense(10번) ➔ 02 포털(14번) ➔ 03 Graylog(15번) ➔ 04 SOAR"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_SUB
    p = tf.add_paragraph()
    p.text = "• 홍주형 담당: 02 포털 서버 코어 하드닝 (웹/DB, BOLA, 디코이, FIM 100% 전담)"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_GREEN
    p.font.bold = True

    # Right: Solo Guard
    add_card(s3, Inches(6.78), Inches(1.8), Inches(5.75), Inches(5.1), border_color=C_GREEN)
    tb_g = s3.shapes.add_textbox(Inches(6.98), Inches(1.95), Inches(5.35), Inches(0.6))
    p = tb_g.text_frame.paragraphs[0]
    p.text = "🛡️ 단독 고도화 산출물: NEXUS-GUARD (100% 소유권)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    tb_g_body = s3.shapes.add_textbox(Inches(6.98), Inches(2.6), Inches(5.35), Inches(4.1))
    tf = tb_g_body.text_frame
    tf.word_wrap = True
    points = [
        ("1. 파편화 관제의 단일 통합", "pfSense 룰 제어, 포털 디코이, Graylog R1~R12 스트림, n8n SOAR를 단 하나의 60FPS 네이티브 데스크톱 관제 콘솔로 통합"),
        ("2. Standalone 무중단 페일세이프 듀얼 모드", "외부 SOC 장비 부재 시에도 Windows 커널 netsh advfirewall(0.001s) 및 자체 FIM으로 100% 자립 방어"),
        ("3. NIST SP 800-207 클린 슬레이트 확립", "부팅 시 무오탐(0% False-Positive) 100/100 점 기준선 보장 및 70개 전수 자동화 테스트 검증"),
        ("4. 0.1초 차단 및 0.8초(804ms) 원상복구", "디코이 침투 즉시 인그레스 403 차단, demo_runner.py --cleanup 롤백 엔진 완성"),
        ("5. Windows 무설치 단일 .exe 패키징", "PyInstaller 17.5MB 단일 바이너리 및 GitHub Actions CI/CD 자동 릴리즈 파이프라인 구축")
    ]
    for h, d in points:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = f"★ {h}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p_sub = tf.add_paragraph()
        p_sub.text = d
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = C_TEXT_SUB
        p_sub.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: Full Topology (Master Architecture)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "MASTER TOPOLOGY // ENTERPRISE ACTIVE DEFENSE", "NEXUS-GUARD 통합 관제 아키텍처 다이어그램", "실시간 텔레메트리 감시부터 AI-XDR 4중 분석, 0.1초 커널 방어 및 이중 격리(Dual Containment)까지")

    if IMG_GUARD_ARCH.exists():
        # Large centered high-res image
        s4.shapes.add_picture(str(IMG_GUARD_ARCH), Inches(0.8), Inches(1.8), width=Inches(11.733))
    else:
        add_card(s4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1), border_color=C_CYAN)

    # =========================================================================
    # SLIDE 5: 6-Zone HUD & Visualizer
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "SENTINELONE & GLASSWIRE BENCHMARK HUD", "엔터프라이즈 데스크톱 네이티브 6대 관제 HUD", "CustomTkinter 60FPS 가속 & WCAG 2.x AA 고대비 시각화 (비전문가도 1초 만에 판독 가능)")

    hud_items = [
        ("24틱 헥사 게이지 (100점)", C_GREEN, "NIST SP 800-207 클린 베이스라인", "수신 텔레메트리 이상 징후 0건 기준선(0% FP) 시각화. 정밀 취약점 진단은 호스트 CPU 보호를 위해 사용자 승인 시 가동 분리."),
        ("360° 위협 레이더 캔버스", C_CYAN, "4대 핵심 인프라 노드 회전 빔", "PORTAL(코어), KALI(침투원), pfSense(경계 방화벽), SIEM(감사로그) 4대 노드 실시간 400ms 스윕 빔 및 침투 충격파 블립 점등."),
        ("트래픽 오실로스코프 파형", C_PURPLE, "초당 KB/s 전송량 실시간 렌더링", "정상 시 48~52 KB/s 에메랄드 파형 유지, 악성 침해 패킷 유입 시 12,480 KB/s 네온 크림슨 스파이크 즉각 점등."),
        ("MITRE ATT&CK Matrix v14", C_GOLD, "5대 핵심 전술 스트립 실시간 점등", "정찰(TA0043), 침투(TA0001), 실행(TA0002), 방어우회(TA0005), 파괴(TA0040) 실시간 점등 및 공식 Navigator v4.5 호환."),
        ("쉬운 한글 종합 판정 배너", C_GREEN, "비전문가 / CISO 즉시 인지 UI", "CrowdStrike 스타일의 1초 요약 배너: '🛡️ [안전] 실시간 위협 없음 (위험도 0점 / 정상 트래픽)' 초보자 안내 레이블 전면 배치."),
        ("1-Click 비상 호스트 격리", C_RED, "커널 레벨 즉각 네트워크 단절", "관리 콘솔(127.0.0.1)만 제외하고 외부 패킷을 0.001초 만에 드롭하는 비상 차단 버튼 및 CISO 감사 보고서 발행.")
    ]

    for idx, (title, col, sub, desc) in enumerate(hud_items):
        r = idx // 3
        c = idx % 3
        left = Inches(0.8 + c * 3.98)
        top = Inches(1.85 + r * 2.6)
        add_card(s5, left, top, Inches(3.78), Inches(2.4), border_color=col)
        tb = s5.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(3.38), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_WHITE
        p2.space_before = Pt(3)
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 6: 4 Active Defense Engines
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "ACTIVE DEFENSE & ZERO-TRUST SUBSYSTEMS", "4대 핵심 능동 방어(Active Defense) 엔진", "단순 탐지를 넘어 0.1초 즉시 격리 및 0.8초 완전 롤백을 실현한 능동형 방어 체계")

    eng_data = [
        ("1. 디코이(허니팟) 카나리 트랩", C_RED, "T1083 / T1595.002", "0.1초 차단", "인터넷 자동화 스캐너(전체 위협 99.7%)를 무오탐(0% FP)으로 유인 차단", [
            "• 미끼 경로: /.env, /.git, /admin.php, /wp-login, /config.json 등 10종",
            "• 단 1바이트라도 프로빙 즉시 인그레스 403 차단 및 OS 커널 방화벽 동기화",
            "• 침투자의 정찰 행위 단계에서 선제적 무력화"
        ]),
        ("2. 자체 SHA-256 FIM 무결성 감시", C_CYAN, "T1562.001 / CWE-732", "0.1초 감지", "핵심 소스코드 및 환경설정 무단 변조 실시간 탐지", [
            "• app/, nexus_guard/, db/, .env 핵심 파일 해시 기준선 10초 주기 폴링",
            "• 웹쉘 업로드 또는 백도어 삽입 발생 시 0.1초 만에 알람 발생",
            "• 엔터프라이즈 환경 시 Wazuh Syscheck(agent_fim_template.xml) 연동"
        ]),
        ("3. AST Guard & BOLA Shield", C_PURPLE, "OWASP API1:2023 / CWE-89", "원천 차단", "상용 WAF를 100% 우회하는 비즈니스 로직 결함 방어", [
            "• 파이썬 AST 정적 분석으로 동적 SQL 쿼리 구조 검증 (SQLi 방어)",
            "• @permission_required('users.manage') 데코레이터로 권한 승격 차단",
            "• PoLP(최소권한) 기반 DB 3종(nexus_app, conf, n8n) 물리적 분리"
        ]),
        ("4. 1초 원상복구(Clean-up) 롤백", C_GOLD, "NIST SP 800-61 / MTTD", "804.7 ms", "시연 및 사고 대응 후 즉각 정상 베이스라인 복원", [
            "• demo_runner.py --cleanup 실행 시 0.80초 만에 전체 롤백",
            "• 모의 침투 고정 IP 8개 방화벽 차단 해제 및 잠금 계정 4개 정상화",
            "• 인메모리 블랙리스트 클린 리셋으로 100점 만점 베이스라인 복구"
        ])
    ]

    for i, (title, col, tech, speed, desc, items) in enumerate(eng_data):
        r = i // 2
        c = i % 2
        left = Inches(0.8 + c * 5.98)
        top = Inches(1.85 + r * 2.6)
        add_card(s6, left, top, Inches(5.75), Inches(2.45), border_color=col)
        tb = s6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(2.15))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{title}   [{speed}]"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = f"{desc} ({tech})"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_WHITE
        p2.space_before = Pt(3)
        p2.space_after = Pt(6)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = it
            p_it.font.size = Pt(10)
            p_it.font.color.rgb = C_TEXT_SUB
            p_it.space_after = Pt(2)

    # =========================================================================
    # SLIDE 7: 4-Tier AI Cascade Router
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "MULTI-TIER AI ROUTING ENGINE // 100% AVAILABILITY", "4중 AI-XDR 하이브리드 추론 캐스케이드", "클라우드 LPU의 0.48초 초고속 추론부터 폐쇄망 로컬 LLM 및 인라인 규칙까지 무장애 폴백")

    ai_tiers = [
        ("TIER 1 (PRIMARY)", "Groq Cloud LPU", "openai/gpt-oss-120b", "⚡ 0.48s 초고속", C_CYAN, [
            "• 초당 500+ 토큰의 초고속 LPU 전용 하드웨어 연동",
            "• 실시간 침해 로그 시맨틱 트리아지 및 위험도 평가",
            "• 네트워크 지연을 포함해도 0.5초 이내에 분석 완료"
        ]),
        ("TIER 2 (ENTERPRISE)", "NVIDIA NIM", "Llama-3.1-Nemotron-70B", "🧠 0.52s 심층", C_GREEN, [
            "• 엔터프라이즈 최고 사양 70B 파라미터 추론 엔진",
            "• 단일 룰이 아닌 다단계 복합 공격 체인(Kill-Chain) 분석",
            "• 클라우드 호스팅으로 로컬 GPU 부하 0% 달성"
        ]),
        ("TIER 3 (ON-PREMISE)", "Ollama 로컬 LLM", "qwen2.5:7b (11434)", "🔒 폐쇄망 독립", C_GOLD, [
            "• 외부 인터넷 단절 또는 정부/금융 폐쇄망 완벽 대응",
            "• 호스트 로컬 머신에서 완전 독립형 오프라인 추론 수행",
            "• 기밀 유출 위험 없는 On-Premise 데이터 거버넌스"
        ]),
        ("TIER 4 (FALLBACK)", "내장 정규식 룰셋", "siem_rules.json (R1~R12)", "⚙️ 0.001s 인라인", C_PURPLE, [
            "• 외부 AI 인프라 전체 단절 시 가동되는 100% 안전망",
            "• O(1) 해시 테이블 및 정규식 기반 침해 즉각 판정",
            "• 시스템 중단 없는 절대 무장애 가용성 보장"
        ])
    ]

    for i, (t_num, name, model, speed, col, items) in enumerate(ai_tiers):
        left = Inches(0.8 + i * 2.98)
        add_card(s7, left, Inches(1.9), Inches(2.8), Inches(4.9), border_color=col)
        tb = s7.shapes.add_textbox(left + Inches(0.18), Inches(2.1), Inches(2.44), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = t_num
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DIM

        p = tf.add_paragraph()
        p.text = name
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = model
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_SUB

        p = tf.add_paragraph()
        p.text = speed
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.space_before = Pt(8)
        p.space_after = Pt(14)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = it
            p_it.font.size = Pt(10.5)
            p_it.font.color.rgb = C_TEXT_SUB
            p_it.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: Dual Containment & SOC Integrations
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "DUAL-MODE RESILIENCE // 7 ENTERPRISE INTEGRATIONS", "이중 격리(Dual Containment) 및 엔터프라이즈 SOC 연동", "단독 PC에서의 로컬 커널 제어부터 대형 전사 SOC(pfSense, Graylog, Wazuh, n8n) 연동까지")

    # Mode A
    add_card(s8, Inches(0.8), Inches(1.85), Inches(5.75), Inches(5.1), border_color=C_GOLD)
    tb_a = s8.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(5.35), Inches(4.7))
    tf = tb_a.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚡ [MODE A] Standalone 무중단 페일세이프 (단독 PC)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    mode_a_items = [
        ("Windows netsh advfirewall 커널 제어", "외부 장비 없이 OS 커널 레벨에서 0.001초 미만으로 공격자 IP 패킷 즉각 폐기 (Drop)"),
        ("로컬 루프백 화이트리스트 보호", "127.0.0.1 및 관리자 콘솔 IP를 안전 보호하여 비상 격리 시에도 관제 콘솔 무중단 유지"),
        ("자체 FIM & 내장 룰 엔진 자율 구동", "외부 Wazuh/Graylog 서버가 없어도 로컬 파일 해시 감시 및 침해 탐지 100% 정상 작동"),
        ("완전한 독립 배포 보장", "타 PC나 VM에 단일 파일만 복사해도 즉각 완전한 능동 방어 시스템 기동 가능")
    ]
    for h, d in mode_a_items:
        p = tf.add_paragraph()
        p.text = f"• {h}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.space_before = Pt(8)
        p_d = tf.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_SUB

    # Mode B
    add_card(s8, Inches(6.78), Inches(1.85), Inches(5.75), Inches(5.1), border_color=C_GREEN)
    tb_b = s8.shapes.add_textbox(Inches(6.98), Inches(2.05), Inches(5.35), Inches(4.7))
    tf = tb_b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🌐 [MODE B] 엔터프라이즈 SOC 풀 연동 (분산 인프라)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    mode_b_items = [
        ("pfSense 경계 방화벽 (192.168.3.10:443)", "pfBlockerNG 커스텀 피드 연동으로 탐지된 공격자를 경계망 단계에서 원격 자동 차단"),
        ("Graylog 중앙 SIEM (192.168.3.15:9000)", "GELF UDP 12201 포트로 R1~R12 보안 이벤트를 표준 JSONL 스트리밍 브로드캐스트"),
        ("Wazuh 엔드포인트 EDR (192.168.3.15:1514)", "Syscheck 커널 무결성 감사(agent_fim_template.xml) 및 규제 준수(ISMS-P) 증적 자동 적재"),
        ("n8n SOAR 대응 자동화 (PORT 5678)", "침해 사고 발생 시 Discord/Slack 알림 및 Jira 장애 티켓 자동 발행 파이프라인")
    ]
    for h, d in mode_b_items:
        p = tf.add_paragraph()
        p.text = f"• {h}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.space_before = Pt(8)
        p_d = tf.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 9: Live Verification & Testing (150MB Video & Pytest)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "LIVE VERIFICATION // EMPIRICAL EVIDENCE", "실전 시연 검증 및 70개 전수 자동화 테스트", "150MB 무편집 Full-HD 실측 시연 동영상 및 10.67초 만에 100% 통과된 자동화 테스트 스위트")

    # Left: Video Card
    add_card(s9, Inches(0.8), Inches(1.85), Inches(5.75), Inches(5.1), border_color=C_CYAN)
    tb_v = s9.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(5.35), Inches(4.7))
    tf = tb_v.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎬 무편집 100% 실측 시연 영상 (150.3 MB Full-HD)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    v_steps = [
        ("[00:00] 보안설정 OFF: 취약 모드 재현", "공격자가 /.env, /.git에 무제한 접근하여 DB 패스워드와 기밀 API Key를 탈취하는 침해 성공 확인"),
        ("[01:15] 보안설정 ON: 디코이 가동", "공격자가 미끼 파일 접근 즉시 0.1초 만에 인그레스 403 차단 및 커널 방화벽 격리 집행"),
        ("[02:30] 실시간 전파: pfSense & SIEM", "차단 IP가 pfBlockerNG 및 Graylog(GELF), n8n SOAR Webhook으로 즉각 브로드캐스트"),
        ("[03:10] 1초 원상복구 (--cleanup)", "demo_runner.py --cleanup 실행 단 0.80초 (804ms) 만에 클린 베이스라인 완전 복구")
    ]
    for s_title, s_desc in v_steps:
        p = tf.add_paragraph()
        p.text = s_title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.space_before = Pt(6)
        p_d = tf.add_paragraph()
        p_d.text = s_desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_SUB

    # Right: Test Suite Card
    add_card(s9, Inches(6.78), Inches(1.85), Inches(5.75), Inches(5.1), border_color=C_GREEN)
    tb_tst = s9.shapes.add_textbox(Inches(6.98), Inches(2.05), Inches(5.35), Inches(4.7))
    tf = tb_tst.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧪 자동화 단위/통합 테스트: 70 / 70 PASS (100%)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    t_items = [
        ("7개 테스트 슈트 전수 통과 (10.67s 실측)", "test_clean_slate.py, test_gui_contrast.py, test_mitre_mapping.py, test_report_exporter.py, test_commercial_enterprise.py 등 전수 검증"),
        ("결함률 0.0% (Zero Regression)", "적대적 퍼징 및 극한의 경계값 입력에도 시스템 크래시 또는 미처리 예외 0건 입증"),
        ("NIST 제로 트러스트 클린 베이스라인 검증", "verify_clean_state.py 단독 검증 100% 통과 (초기 차단 목록 0건, 점수 100/100 보장)"),
        ("WCAG 2.x AA 색대비 전수 통과", "모든 HUD 텍스트 및 레이더 캔버스가 대비율 4.5:1 이상을 충족하여 가독성 보장")
    ]
    for h, d in t_items:
        p = tf.add_paragraph()
        p.text = f"✔ {h}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.space_before = Pt(8)
        p_d = tf.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 10: DevOps & Standalone Packaging
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "COMMERCIAL PACKAGING & CI/CD PIPELINE", "엔터프라이즈 무설치 배포 및 자동화 파이프라인", "Python 미설치 환경에서도 1-클릭 실행되는 단일 바이너리 및 GitHub Actions 자동 Releases")

    p_cards = [
        ("1. Windows 단일 실행 파일 (.exe)", C_CYAN, "PyInstaller 17.5 MB", [
            "• Python 인터프리터 및 CustomTkinter 에셋 완전 내장",
            "• 별도 가상환경 설치 없이 더블클릭 1초 만에 네이티브 관제 창 구동",
            "• 백그라운드 검은 터미널 창 없는 클린 실행 (--windowed)"
        ]),
        ("2. GitHub Actions 자동 CI/CD", C_GREEN, "release.yml / ci.yml", [
            "• Git Tag(v2.5.0) 푸시 시 Windows 러너에서 70개 테스트 전수 검증",
            "• 테스트 100% 통과 시에만 NexusGuard-Windows-x64.zip 자동 빌드",
            "• GitHub Releases에 SHA-256 체크섬과 함께 자동 배포"
        ]),
        ("3. 24/7 헤드리스 서버 데몬", C_GOLD, "Docker & docker-compose", [
            "• 리눅스 서버 및 보안 어플라이언스를 위한 헤드리스 모드 지원",
            "• docker compose up -d 한 줄로 백그라운드 상시 위협 감시 가동",
            "• 볼륨 마운트로 logs/ 및 config.json 호스트 실시간 영구 보존"
        ])
    ]

    for i, (title, col, sub, items) in enumerate(p_cards):
        left = Inches(0.8 + i * 3.98)
        add_card(s10, left, Inches(1.9), Inches(3.78), Inches(4.9), border_color=col)
        tb = s10.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(3.38), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_WHITE
        p.space_before = Pt(4)
        p.space_after = Pt(12)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = it
            p_it.font.size = Pt(11)
            p_it.font.color.rgb = C_TEXT_SUB
            p_it.space_after = Pt(8)

    # =========================================================================
    # SLIDE 11: PARR Troubleshooting & CISO Defense Logic
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "ENGINEERING RETROSPECTIVE & CISO DEFENSE", "실전 트러블슈팅(PARR) 및 CISO 철통 방어 논리", "피드백을 통한 3대 핵심 구조 혁신 및 적대적 심사관 압박 질문에 대한 완벽한 방어")

    parr_items = [
        ("Case 1. 초기 임의 공격자 잔류 오탐 ➔ 클린 슬레이트 100점 확립", C_GREEN, [
            "• 문제: 첫 실행 시 더미 공격자가 잔류하여 65점으로 시작, 사용자 불신 초래",
            "• 해결: 코어 상태 머신을 0건으로 격리하고, 부팅 시 100점 만점을 보장하는 상태 머신과 'test_clean_slate.py' 테스트 구축",
            "• 결과: 신규 설치 시 0건 위협, 100/100 점 제로 트러스트 기준선 100% 확립"
        ]),
        ("Case 2. 난해한 레이더 및 전문 용어 ➔ 비전문가 친화적 고대비 UX", C_CYAN, [
            "• 문제: 360도 레이더의 점/선 및 XDR 판정 문구가 비전문 관리자 시각에서 판독 난해",
            "• 해결: SentinelOne 스타일 쉬운 한글 종합 판정 배너, 4대 인프라 범례 점등, WCAG AA 고대비 적용",
            "• 결과: 관제사 및 임원도 1초 만에 시스템 안전 여부를 직관적으로 식별 가능"
        ]),
        ("Case 3. 새 환경 설치 종속성 ➔ 17.5MB 단일 실행 파일 및 CI/CD", C_PURPLE, [
            "• 문제: 파이썬 미설치 환경에서 의존성 충돌로 인한 구동 실패 위험",
            "• 해결: PyInstaller 단일 실행 파일 패키징 스크립트(build_exe.py) 및 GitHub Actions 릴리즈 자동화",
            "• 결과: 새 PC/VM 어디서든 더블클릭 1초 만에 네이티브 관제 콘솔 가동 완성"
        ])
    ]

    for i, (title, col, items) in enumerate(parr_items):
        top = Inches(1.85 + i * 1.7)
        add_card(s11, Inches(0.8), top, Inches(11.733), Inches(1.55), border_color=col)
        tb = s11.shapes.add_textbox(Inches(1.0), top + Inches(0.12), Inches(11.333), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = it
            p_it.font.size = Pt(10.5)
            p_it.font.color.rgb = C_TEXT_SUB
            p_it.space_after = Pt(2)

    # =========================================================================
    # SLIDE 12: Conclusion & Q&A
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "CONCLUSION & EVALUATION SUMMARY", "최종 결론 및 공식 심사 결과 요약", "비즈니스를 지키는 실전형 능동 방어 솔루션으로 공학적 완결성을 증명했습니다")

    # Left Summary Table
    add_card(s12, Inches(0.8), Inches(1.85), Inches(6.75), Inches(5.1), border_color=C_GREEN)
    tb_sum = s12.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(6.35), Inches(4.7))
    tf = tb_sum.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🏆 공식 6대 심사 평가 결과: 100 / 100 만점 (Grade: S+)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_GREEN

    metrics_table = [
        ("■ 1. 새 PC 단독 설치 및 실행", "20 / 20", "17.5MB 단일 바이너리, 1초 무설치 실행, 클린 베이스라인"),
        ("■ 2. GitHub 저장소 구성 및 보안", "15 / 15", "팀 원본 및 홍주형 100% 분리, 민감정보 0건, 연동설정 동봉"),
        ("■ 3. 실제 동작 확인 (4단계)", "20 / 20", "0.1초 차단, 0.48초 AI 트리아지, 804ms 복구, 150MB 시연영상"),
        ("■ 4. 개인 기여도 분리 (단독 100%)", "15 / 15", "GUI 관제센터, 360° 레이더, FIM, 디코이, CI/CD 단독 소유"),
        ("■ 5. 개선점과 느낀 점 (PARR)", "15 / 15", "클린 슬레이트, 초보자 고대비 UX, 무설치 .exe 3대 혁신"),
        ("■ 6. 이력서 및 자소서 완성도", "15 / 15", "STAR 기법 4대 에세이, CISO 기술 압박 면접 질문 4선 완비")
    ]
    for num_t, score, desc in metrics_table:
        p = tf.add_paragraph()
        p.text = f"{num_t} : {score}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p.space_before = Pt(4)
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_SUB

    # Right Thank You & Q&A
    add_card(s12, Inches(7.78), Inches(1.85), Inches(4.75), Inches(5.1), border_color=C_CYAN)
    tb_qa = s12.shapes.add_textbox(Inches(8.0), Inches(2.3), Inches(4.3), Inches(4.2))
    tf = tb_qa.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "THANK YOU"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "NEXUS-GUARD"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "경청해 주셔서 감사합니다."
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "질의응답 (Q & A)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(20)

    p = tf.add_paragraph()
    p.text = "발표자: 홍주형 (포털 코어 아키텍트 & 보안 최고관리자)\nEmail: doffl9737@gmail.com\nGitHub: https://github.com/stulss/nexus-guard"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_SUB
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(25)

    # Save PPTX
    out_pptx = Path(r"C:\Users\user\Desktop\NEXUS_GUARD_발표자료.pptx")
    prs.save(str(out_pptx))
    print(f"[+] Master PPTX successfully created at: {out_pptx}")
    return out_pptx


def convert_pptx_to_pdf(pptx_path: Path):
    print(f"[*] Converting PPTX to PDF via PowerPoint COM: {pptx_path} ...")
    import win32com.client
    ppt = None
    deck = None
    try:
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        # Do not make it visible to prevent focus theft
        deck = ppt.Presentations.Open(str(pptx_path.resolve()), WithWindow=False)
        out_pdf = pptx_path.with_suffix(".pdf")
        # 32 = ppSaveAsPDF
        deck.SaveAs(str(out_pdf.resolve()), 32)
        deck.Close()
        deck = None
        ppt.Quit()
        ppt = None
        print(f"[+] Successfully converted to PDF at: {out_pdf}")
        return out_pdf
    except Exception as e:
        print(f"[!] PowerPoint COM conversion error: {e}")
        if deck:
            deck.Close()
        if ppt:
            ppt.Quit()
        return None


def main():
    pptx_path = build_deck()
    pdf_path = convert_pptx_to_pdf(pptx_path)

    # Sync to all required directories
    targets = [
        Path(r"C:\Users\user\Desktop\NEXUS-GUARD_포트폴리오\presentation"),
        Path(r"C:\Users\user\Desktop\NEXUS-GUARD\docs\presentation"),
        Path(r"C:\Users\user\Desktop\넥서스가이드\presentation"),
    ]

    for t in targets:
        t.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pptx_path, t / "NEXUS_GUARD_발표자료.pptx")
        if pdf_path and pdf_path.exists():
            shutil.copy2(pdf_path, t / "NEXUS_GUARD_발표자료.pdf")
        print(f"[+] Synced presentation files to: {t}")


if __name__ == "__main__":
    main()
