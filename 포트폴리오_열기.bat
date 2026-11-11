@echo off
chcp 65001 > nul
title NEXUS-GUARD 엔터프라이즈 능동 방어 보안 관제 포트폴리오
echo ==============================================================================
echo   🛡️ NEXUS-GUARD: AI 기반 엔터프라이즈 능동 방어(Active Defense) 보안 포트폴리오
echo   작성자: 홍주형 (Hong Juhyeong) · 포털 코어 아키텍트 & 보안 최고관리자
echo   버전: v2.5.0-LTS (Commercial Grade)
echo ==============================================================================
echo.
echo [1/1] 기본 웹 브라우저에서 인터랙티브 포트폴리오(index.html)를 자동 실행합니다...
start "" "%~dp0index.html"
exit /b 0
