/**
 * NEXUS-GUARD Interactive Security Dashboard & Portfolio
 * Core Engine, Visualizers & CISO Zero-Trust Subsystems
 * Author: Hong Juhyeong (홍주형)
 */

(function () {
  "use strict";

  // State Management
  const State = {
    isCleanSlate: true,
    activeScenario: null,
    blockedIpCount: 0,
    radarAngle: 0,
    radarSpeed: 0.025,
    attackBlips: [],
    oscilloscopeData: new Array(120).fill(25),
    oscilloscopeSpike: false,
    spikeIntensity: 0,
    metricsAnimated: false,
    audioEnabled: true
  };

  // Sound Synthesizer (Web Audio API)
  const SoundFX = {
    ctx: null,
    init() {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      } catch (e) {
        console.warn("AudioContext not supported", e);
      }
    },
    playTone(freq, type, duration, gainValue = 0.05) {
      if (!this.ctx || !State.audioEnabled) return;
      if (this.ctx.state === "suspended") {
        this.ctx.resume();
      }
      try {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        gain.gain.setValueAtTime(gainValue, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
      } catch (err) {}
    },
    threatAlert() {
      this.playTone(880, "sawtooth", 0.12, 0.08);
      setTimeout(() => this.playTone(660, "sawtooth", 0.18, 0.08), 120);
    },
    recoveryChime() {
      this.playTone(523.25, "sine", 0.1, 0.05); // C5
      setTimeout(() => this.playTone(659.25, "sine", 0.12, 0.05), 90); // E5
      setTimeout(() => this.playTone(783.99, "sine", 0.25, 0.06), 180); // G5
    },
    clickTick() {
      this.playTone(1200, "sine", 0.03, 0.02);
    }
  };

  // DOM Elements Cache
  let radarCanvas, radarCtx;
  let oscCanvas, oscCtx;
  let terminalBody;
  let statBlockedCount, statThreatScore, statTriageVerdict;
  let ztBadgeThreats, ztBadgeIntegrity, ztBadgeAudit;

  // Initialize on DOM Ready
  document.addEventListener("DOMContentLoaded", () => {
    initDOMElements();
    initCanvases();
    initCounters();
    initTabSystem();
    initParrAccordion();
    initAttackSimulator();
    initImageModal();
    initMitreJsonModal();
    initFallbackModal();
    initPrintHandler();

    // Start Animation Loops
    requestAnimationFrame(renderRadar);
    requestAnimationFrame(renderOscilloscope);

    // Initial Terminal Log
    logToTerminal("INIT", "NEXUS-GUARD v2.5.0-LTS Core Security Kernel started.", "safe");
    logToTerminal("KERNEL_HOOK", "Windows netsh advfirewall hook: ACTIVE (Response: 0.001s).", "prefix");
    logToTerminal("NIST_SP800_207", "Zero-Trust State: Protected [0 Threats] | Baseline Integrity [100%] | Vuln Audit [On-Demand].", "safe");
    logToTerminal("INFO", "360° Rotating Threat Radar & Oscilloscope live telemetry active.", "prefix");
  });

  function initDOMElements() {
    radarCanvas = document.getElementById("radarCanvas");
    oscCanvas = document.getElementById("oscilloscopeCanvas");
    terminalBody = document.getElementById("terminalBody");
    statBlockedCount = document.getElementById("statBlockedCount");
    statThreatScore = document.getElementById("statThreatScore");
    statTriageVerdict = document.getElementById("statTriageVerdict");

    ztBadgeThreats = document.getElementById("ztBadgeThreats");
    ztBadgeIntegrity = document.getElementById("ztBadgeIntegrity");
    ztBadgeAudit = document.getElementById("ztBadgeAudit");
  }

  // --------------------------------------------------------------------------
  // 1. Radar Canvas (360-degree Sweeping Beam & 4 Infrastructure Nodes)
  // --------------------------------------------------------------------------
  const radarNodes = [
    { id: "PORTAL", name: "02.PORTAL (Core)", angle: 0, dist: 0, color: "#00e5ff", status: "ONLINE (5070)" },
    { id: "PFSENSE", name: "01.pfSense (WAF)", angle: Math.PI * 0.25, dist: 0.65, color: "#00e676", status: "SECURE DROP" },
    { id: "KALI", name: "00.KALI (Sim Engine)", angle: Math.PI * 0.75, dist: 0.78, color: "#ff3864", status: "STANDBY" },
    { id: "SIEM", name: "03.SIEM (Graylog/Wazuh)", angle: Math.PI * 1.25, dist: 0.62, color: "#c084fc", status: "INGESTING 12201" }
  ];

  function initCanvases() {
    if (radarCanvas) {
      radarCtx = radarCanvas.getContext("2d");
      resizeCanvas(radarCanvas);
    }
    if (oscCanvas) {
      oscCtx = oscCanvas.getContext("2d");
      resizeCanvas(oscCanvas);
    }

    window.addEventListener("resize", () => {
      if (radarCanvas) resizeCanvas(radarCanvas);
      if (oscCanvas) resizeCanvas(oscCanvas);
    });
  }

  function resizeCanvas(canvas) {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
  }

  function renderRadar() {
    if (!radarCtx || !radarCanvas) return;
    const rect = radarCanvas.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const cx = width / 2;
    const cy = height / 2;
    const radius = Math.min(cx, cy) - 20;

    radarCtx.clearRect(0, 0, width, height);

    // 1. Static Concentric Circles & Crosshairs
    radarCtx.strokeStyle = "rgba(30, 41, 59, 0.7)";
    radarCtx.lineWidth = 1;
    [0.25, 0.5, 0.75, 1.0].forEach((ratio) => {
      radarCtx.beginPath();
      radarCtx.arc(cx, cy, radius * ratio, 0, Math.PI * 2);
      radarCtx.stroke();
    });

    // Crosshairs
    radarCtx.beginPath();
    radarCtx.moveTo(cx - radius, cy);
    radarCtx.lineTo(cx + radius, cy);
    radarCtx.moveTo(cx, cy - radius);
    radarCtx.lineTo(cx, cy + radius);
    radarCtx.stroke();

    // 2. Degree Markers
    radarCtx.fillStyle = "rgba(100, 116, 139, 0.5)";
    radarCtx.font = "9px 'JetBrains Mono', monospace";
    radarCtx.textAlign = "center";
    radarCtx.fillText("000°", cx, cy - radius + 12);
    radarCtx.fillText("090°", cx + radius - 15, cy + 3);
    radarCtx.fillText("180°", cx, cy + radius - 5);
    radarCtx.fillText("270°", cx - radius + 15, cy + 3);

    // 3. Rotating Sweep Beam with Gradient Trail
    State.radarAngle = (State.radarAngle + State.radarSpeed) % (Math.PI * 2);

    const sweepGradient = radarCtx.createRadialGradient(cx, cy, 0, cx, cy, radius);
    sweepGradient.addColorStop(0, "rgba(0, 229, 255, 0.2)");
    sweepGradient.addColorStop(1, "rgba(0, 229, 255, 0.01)");

    radarCtx.save();
    radarCtx.beginPath();
    radarCtx.moveTo(cx, cy);
    radarCtx.arc(cx, cy, radius, State.radarAngle - 0.5, State.radarAngle);
    radarCtx.closePath();
    radarCtx.fillStyle = sweepGradient;
    radarCtx.fill();

    // Leading Beam Line
    radarCtx.beginPath();
    radarCtx.moveTo(cx, cy);
    radarCtx.lineTo(cx + Math.cos(State.radarAngle) * radius, cy + Math.sin(State.radarAngle) * radius);
    radarCtx.strokeStyle = State.isCleanSlate ? "rgba(0, 230, 118, 0.9)" : "rgba(255, 56, 100, 0.9)";
    radarCtx.lineWidth = 2;
    radarCtx.stroke();
    radarCtx.restore();

    // 4. Infrastructure Nodes
    radarNodes.forEach((node) => {
      const nx = cx + Math.cos(node.angle) * (radius * node.dist);
      const ny = cy + Math.sin(node.angle) * (radius * node.dist);

      // Node Glow Aura
      radarCtx.beginPath();
      radarCtx.arc(nx, ny, 8, 0, Math.PI * 2);
      radarCtx.fillStyle = node.color + "33";
      radarCtx.fill();

      // Node Center Dot
      radarCtx.beginPath();
      radarCtx.arc(nx, ny, 3.5, 0, Math.PI * 2);
      radarCtx.fillStyle = node.color;
      radarCtx.fill();

      // Node Label
      radarCtx.fillStyle = "#e2e8f0";
      radarCtx.font = "10px 'JetBrains Mono', monospace";
      radarCtx.textAlign = "center";
      radarCtx.fillText(node.name, nx, ny + 15);
    });

    // 5. Active Attack Blips & Particle Vectors
    if (State.attackBlips.length > 0) {
      const now = Date.now();
      State.attackBlips = State.attackBlips.filter((b) => now - b.time < 3000);

      State.attackBlips.forEach((blip) => {
        const age = now - blip.time;
        const alpha = Math.max(0, 1 - age / 3000);
        const radiusScale = (age / 40) % 25;

        // Expanding shockwave from KALI to PORTAL
        radarCtx.beginPath();
        radarCtx.arc(blip.x, blip.y, radiusScale, 0, Math.PI * 2);
        radarCtx.strokeStyle = `rgba(255, 56, 100, ${alpha * 0.8})`;
        radarCtx.lineWidth = 1.5;
        radarCtx.stroke();

        // Vector line to Center
        radarCtx.beginPath();
        radarCtx.setLineDash([4, 4]);
        radarCtx.moveTo(blip.x, blip.y);
        radarCtx.lineTo(cx, cy);
        radarCtx.strokeStyle = `rgba(255, 56, 100, ${alpha * 0.5})`;
        radarCtx.stroke();
        radarCtx.setLineDash([]);
      });
    }

    requestAnimationFrame(renderRadar);
  }

  // --------------------------------------------------------------------------
  // 2. Traffic Oscilloscope (Real-time Packet Throughput Waveform)
  // --------------------------------------------------------------------------
  function renderOscilloscope() {
    if (!oscCtx || !oscCanvas) return;
    const rect = oscCanvas.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const cy = height / 2;

    oscCtx.clearRect(0, 0, width, height);

    // Grid lines
    oscCtx.strokeStyle = "rgba(30, 41, 59, 0.4)";
    oscCtx.lineWidth = 1;
    for (let x = 0; x < width; x += 30) {
      oscCtx.beginPath();
      oscCtx.moveTo(x, 0);
      oscCtx.lineTo(x, height);
      oscCtx.stroke();
    }
    for (let y = 0; y < height; y += 20) {
      oscCtx.beginPath();
      oscCtx.moveTo(0, y);
      oscCtx.lineTo(width, y);
      oscCtx.stroke();
    }

    // Update Waveform Data
    let newSample;
    if (State.oscilloscopeSpike) {
      // Big threat spike
      newSample = (Math.random() * 0.8 + 0.2) * (height * 0.85);
      State.spikeIntensity = Math.max(0, State.spikeIntensity - 0.02);
      if (State.spikeIntensity <= 0) {
        State.oscilloscopeSpike = false;
      }
    } else {
      // Normal baseline traffic
      const t = Date.now() * 0.003;
      newSample = 20 + Math.sin(t) * 8 + Math.random() * 6;
    }

    State.oscilloscopeData.push(newSample);
    if (State.oscilloscopeData.length > 120) {
      State.oscilloscopeData.shift();
    }

    // Draw Smooth Waveform
    const step = width / (State.oscilloscopeData.length - 1);

    oscCtx.beginPath();
    oscCtx.moveTo(0, cy);

    for (let i = 0; i < State.oscilloscopeData.length; i++) {
      const x = i * step;
      const amp = State.oscilloscopeData[i];
      const y = cy + (i % 2 === 0 ? amp * 0.5 : -amp * 0.5);
      if (i === 0) oscCtx.moveTo(x, y);
      else {
        const prevX = (i - 1) * step;
        const prevAmp = State.oscilloscopeData[i - 1];
        const prevY = cy + ((i - 1) % 2 === 0 ? prevAmp * 0.5 : -prevAmp * 0.5);
        const xc = (prevX + x) / 2;
        const yc = (prevY + y) / 2;
        oscCtx.quadraticCurveTo(prevX, prevY, xc, yc);
      }
    }

    const strokeColor = State.isCleanSlate ? "#00e5ff" : "#ff3864";
    oscCtx.strokeStyle = strokeColor;
    oscCtx.lineWidth = 2;
    oscCtx.shadowColor = strokeColor;
    oscCtx.shadowBlur = 10;
    oscCtx.stroke();
    oscCtx.shadowBlur = 0;

    // Update Throughput Text on HUD
    const oscThroughputEl = document.getElementById("oscThroughput");
    if (oscThroughputEl) {
      if (State.oscilloscopeSpike) {
        oscThroughputEl.innerHTML = `<strong>12,480</strong> KB/s <span style="color:var(--color-threat)">(THREAT SURGE)</span>`;
      } else {
        const val = (Math.sin(Date.now() * 0.002) * 5 + 48).toFixed(1);
        oscThroughputEl.innerHTML = `<strong>${val}</strong> KB/s (Normal Baseline)`;
      }
    }

    requestAnimationFrame(renderOscilloscope);
  }

  // --------------------------------------------------------------------------
  // 3. Animated Number Counters
  // --------------------------------------------------------------------------
  function initCounters() {
    const counterElements = document.querySelectorAll(".metric-counter");

    function runCounters() {
      if (State.metricsAnimated) return;
      State.metricsAnimated = true;

      counterElements.forEach((el) => {
        const target = parseFloat(el.getAttribute("data-target"));
        const decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
        const duration = 1400; // ms
        const startTime = performance.now();

        function updateCount(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
          const currentVal = easeProgress * target;

          el.textContent = currentVal.toFixed(decimals);

          if (progress < 1) {
            requestAnimationFrame(updateCount);
          } else {
            el.textContent = target.toFixed(decimals);
          }
        }

        requestAnimationFrame(updateCount);
      });
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          runCounters();
        }
      });
    }, { threshold: 0.2 });

    const metricsSection = document.querySelector(".metrics-strip-section");
    if (metricsSection) {
      observer.observe(metricsSection);
    } else {
      setTimeout(runCounters, 300);
    }
  }

  // --------------------------------------------------------------------------
  // 4. Attack Scenario Simulator Engine
  // --------------------------------------------------------------------------
  const Scenarios = {
    brute_force: {
      name: "무차별 대입 공격 (Brute Force)",
      mitre: "T1110.001",
      threatIp: "192.168.7.77",
      targetPath: "/login (50 req/sec)",
      action: "호스트 레벨 속도 제한 초과 ➔ 5회 오류 즉시 IP 임시 잠금 및 429 반환",
      triage: "HIGH (75/100) - Credential Stuffing Attempt Intercepted"
    },
    decoy_probe: {
      name: "디코이 트랩 침투 탐침 (Decoy Probing)",
      mitre: "T1083",
      threatIp: "192.168.7.104",
      targetPath: "/.env, /.git/config, /admin.php",
      action: "미끼 엔드포인트 1-바이트 터치 즉시 0.1초 403 Forbidden 및 netsh OS 방화벽 영구 격리",
      triage: "CRITICAL (92/100) - Decoy Honeypot Triggered & Dropped"
    },
    fim_tamper: {
      name: "소스코드/설정 무단 변조 (FIM Tamper)",
      mitre: "T1562.001",
      threatIp: "INTERNAL_HOST",
      targetPath: "app/auth.py (SHA-256 Mismatch)",
      action: "자체 FIM 해시 불일치 0.1초 감지 ➔ 백업 원본 자동 롤백 및 CISO 알림 발송",
      triage: "HIGH (85/100) - Core Source Code Tampering Detected"
    },
    complex_chain: {
      name: "복합 다중 공격 체인 (Multi-Vector Chain)",
      mitre: "T1190 & T1083 & T1005",
      threatIp: "192.168.7.200",
      targetPath: "Decoy Probing ➔ AST SQLi ➔ BOLA Approval Bypass",
      action: "pfSense 경계 방화벽 Drop + Windows netsh 격리 + Graylog GELF + n8n SOAR 긴급 티켓 발행",
      triage: "CRITICAL (100/100) - Enterprise Active Defense Containment Triggered"
    }
  };

  function initAttackSimulator() {
    const simButtons = document.querySelectorAll(".sim-btn");
    const resetBtn = document.getElementById("btnSimReset");

    simButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        SoundFX.clickTick();
        const scenarioKey = btn.getAttribute("data-scenario");
        triggerAttackScenario(scenarioKey, btn);
      });
    });

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        executeCleanSlateRecovery();
      });
    }
  }

  function triggerAttackScenario(key, activeBtn) {
    const data = Scenarios[key];
    if (!data) return;

    State.isCleanSlate = false;
    State.activeScenario = key;
    State.blockedIpCount += 1;
    State.oscilloscopeSpike = true;
    State.spikeIntensity = 1.0;

    SoundFX.threatAlert();

    // Active button UI highlight
    document.querySelectorAll(".sim-btn").forEach((b) => b.classList.remove("active"));
    if (activeBtn) activeBtn.classList.add("active");

    // Add Blip on Radar (originates from KALI node)
    if (radarCanvas) {
      const rect = radarCanvas.getBoundingClientRect();
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const radius = Math.min(cx, cy) - 20;
      const kaliNode = radarNodes.find((n) => n.id === "KALI");
      const kx = cx + Math.cos(kaliNode.angle) * (radius * kaliNode.dist);
      const ky = cy + Math.sin(kaliNode.angle) * (radius * kaliNode.dist);

      State.attackBlips.push({ x: kx, y: ky, time: Date.now() });
    }

    // Update Zero-Trust Status Badges
    if (ztBadgeThreats) {
      ztBadgeThreats.className = "zt-badge threat";
      ztBadgeThreats.innerHTML = `<span class="beacon-dot" style="background:var(--color-threat);"></span> [ACTIVE INTERCEPTED: 403 BLOCKED]`;
    }
    if (ztBadgeIntegrity) {
      ztBadgeIntegrity.className = "zt-badge threat";
      ztBadgeIntegrity.innerHTML = `<span>🛡️</span> [ATTACK SURFACE: 1 THREAT IP CONFINED]`;
    }
    if (ztBadgeAudit) {
      ztBadgeAudit.className = "zt-badge threat";
      ztBadgeAudit.innerHTML = `<span>⚡</span> [KERNEL HOOK: ISOLATED 0.001s]`;
    }

    // Update HUD Stats
    if (statBlockedCount) {
      statBlockedCount.textContent = `${State.blockedIpCount} 건`;
      statBlockedCount.className = "hud-stat-value threat";
    }
    if (statThreatScore) {
      statThreatScore.textContent = "78 / 100";
      statThreatScore.className = "hud-stat-value threat";
    }
    if (statTriageVerdict) {
      statTriageVerdict.textContent = data.triage;
      statTriageVerdict.style.color = "var(--color-threat)";
    }

    // Highlight MITRE technique badges
    highlightMitreTechnique(data.mitre);

    // Terminal Logging
    logToTerminal("ALERT", `[SIMULATION] ${data.name} initiated from IP: ${data.threatIp}`, "threat");
    logToTerminal("MITRE", `ATT&CK Technique identified: ${data.mitre} targeting ${data.targetPath}`, "warn");
    logToTerminal("KERNEL", `Active Defense: ${data.action}`, "safe");
    logToTerminal("SIEM", `GELF UDP 12201 dispatched to Graylog & n8n webhook alert emitted.`, "prefix");
  }

  function executeCleanSlateRecovery() {
    SoundFX.recoveryChime();

    State.isCleanSlate = true;
    State.activeScenario = null;
    State.blockedIpCount = 0;
    State.oscilloscopeSpike = false;
    State.spikeIntensity = 0;
    State.attackBlips = [];

    // Reset button states
    document.querySelectorAll(".sim-btn").forEach((b) => b.classList.remove("active"));

    // Reset Zero-Trust Status Badges
    if (ztBadgeThreats) {
      ztBadgeThreats.className = "zt-badge protected";
      ztBadgeThreats.innerHTML = `<span class="beacon-dot"></span> [ACTIVE PROTECTED: 0 ACTIVE THREATS]`;
    }
    if (ztBadgeIntegrity) {
      ztBadgeIntegrity.className = "zt-badge integrity";
      ztBadgeIntegrity.innerHTML = `<span>🛡️</span> [BASELINE INTEGRITY: 100% (SHA-256 Verified)]`;
    }
    if (ztBadgeAudit) {
      ztBadgeAudit.className = "zt-badge standby";
      ztBadgeAudit.innerHTML = `<span>🔍</span> [VULN AUDIT: ON-DEMAND STANDBY (NIST SP 800-207)]`;
    }

    // Reset HUD Stats
    if (statBlockedCount) {
      statBlockedCount.textContent = "0 건";
      statBlockedCount.className = "hud-stat-value safe";
    }
    if (statThreatScore) {
      statThreatScore.textContent = "100 / 100";
      statThreatScore.className = "hud-stat-value safe";
    }
    if (statTriageVerdict) {
      statTriageVerdict.textContent = "A+ 최고 안전 상태 (CLEAN NETWORK)";
      statTriageVerdict.style.color = "var(--color-safe)";
    }

    // Clear MITRE technique highlights
    document.querySelectorAll(".technique-chip").forEach((chip) => {
      chip.classList.remove("triggered");
    });

    // Terminal Reset Notification
    logToTerminal("RECOVERY", "=======================================================", "safe");
    logToTerminal("CLEAN_SLATE", "1-Second Clean Slate Recovery (--cleanup) executed successfully.", "safe");
    logToTerminal("AUDIT", "Firewall rules reset. Blacklist 0. Active threats 0. Integrity 100% verified.", "safe");
    logToTerminal("RECOVERY", "=======================================================", "safe");
  }

  function highlightMitreTechnique(mitreStr) {
    document.querySelectorAll(".technique-chip").forEach((chip) => {
      chip.classList.remove("triggered");
      const techId = chip.getAttribute("data-tech");
      if (mitreStr.includes(techId)) {
        chip.classList.add("triggered");
        chip.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
      }
    });
  }

  function logToTerminal(prefix, message, type = "normal") {
    if (!terminalBody) return;
    const now = new Date();
    const timeStr = now.toTimeString().split(" ")[0] + "." + String(now.getMilliseconds()).padStart(3, "0");

    const line = document.createElement("div");
    line.className = "log-line";

    let typeClass = "";
    if (type === "threat") typeClass = "log-threat";
    else if (type === "warn") typeClass = "log-warn";
    else if (type === "safe") typeClass = "log-safe";
    else if (type === "prefix") typeClass = "log-prefix";

    line.innerHTML = `<span class="log-ts">[${timeStr}]</span> <span class="log-prefix">[${prefix}]</span> <span class="${typeClass}">${escapeHtml(message)}</span>`;

    terminalBody.appendChild(line);
    terminalBody.scrollTop = terminalBody.scrollHeight;
  }

  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, (m) => {
      switch (m) {
        case "&": return "&amp;";
        case "<": return "&lt;";
        case ">": return "&gt;";
        case '"': return "&quot;";
        case "'": return "&#039;";
        default: return m;
      }
    });
  }

  // --------------------------------------------------------------------------
  // 5. Tabbed System (5 Core Panels)
  // --------------------------------------------------------------------------
  function initTabSystem() {
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanels = document.querySelectorAll(".tab-panel");

    tabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        SoundFX.clickTick();
        const targetId = btn.getAttribute("data-tab");

        tabButtons.forEach((b) => b.classList.remove("active"));
        tabPanels.forEach((p) => p.classList.remove("active"));

        btn.classList.add("active");
        const activePanel = document.getElementById(targetId);
        if (activePanel) {
          activePanel.classList.add("active");
        }
      });
    });
  }

  // --------------------------------------------------------------------------
  // 6. PARR Troubleshooting Accordion
  // --------------------------------------------------------------------------
  function initParrAccordion() {
    const caseCards = document.querySelectorAll(".parr-case-card");

    caseCards.forEach((card) => {
      const header = card.querySelector(".parr-header");
      if (header) {
        header.addEventListener("click", () => {
          SoundFX.clickTick();
          card.classList.toggle("open");
        });
      }
    });
  }

  // --------------------------------------------------------------------------
  // 7. Architecture Image Zoom Modal
  // --------------------------------------------------------------------------
  function initImageModal() {
    const triggers = document.querySelectorAll("[data-modal-img]");
    const modal = document.getElementById("archModal");
    const modalImg = document.getElementById("modalImgTarget");
    const modalTitle = document.getElementById("modalTitleTarget");
    const closeBtn = document.getElementById("modalCloseBtn");

    if (!modal) return;

    triggers.forEach((trigger) => {
      trigger.addEventListener("click", () => {
        SoundFX.clickTick();
        const src = trigger.getAttribute("data-modal-img");
        const title = trigger.getAttribute("data-modal-title") || "시스템 아키텍처 상세도";
        if (modalImg) modalImg.src = src;
        if (modalTitle) modalTitle.textContent = title;
        modal.classList.add("active");
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        modal.classList.remove("active");
      });
    }

    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("active");
      }
    });
  }

  // --------------------------------------------------------------------------
  // 8. MITRE ATT&CK Navigator v4.5 Layer JSON Viewer Modal
  // --------------------------------------------------------------------------
  const mitreLayerData = {
    "name": "NEXUS-GUARD ATT&CK Enterprise Matrix (Active Defense)",
    "versions": {
      "attack": "14",
      "navigator": "4.5",
      "layer": "4.3"
    },
    "domain": "enterprise-attack",
    "description": "NEXUS-GUARD 엔터프라이즈 AI-XDR 능동 방어 실시간 탐지 레이어 (Hong Juhyeong)",
    "techniques": [
      {
        "techniqueID": "T1190",
        "tactic": "initial-access",
        "score": 10,
        "color": "#ff3864",
        "comment": "T1190: AST 정적 쿼리 점검 및 WAF 실시간 403 차단",
        "enabled": true
      },
      {
        "techniqueID": "T1083",
        "tactic": "discovery",
        "score": 8,
        "color": "#ff3864",
        "comment": "T1083: 디코이(/.env, /.git) 탐침 즉시 0.1초 OS netsh 방화벽 격리",
        "enabled": true
      },
      {
        "techniqueID": "T1110",
        "tactic": "credential-access",
        "score": 7,
        "color": "#ffb300",
        "comment": "T1110: 무차별 대입 공격(Brute Force) 5회 오류 시 429 및 계정 임시 잠금",
        "enabled": true
      },
      {
        "techniqueID": "T1005",
        "tactic": "collection",
        "score": 6,
        "color": "#00e5ff",
        "comment": "T1005: 전자결재 순차 승인 무결성(BOLA) 및 지출결의서 위조 원천 방어",
        "enabled": true
      },
      {
        "techniqueID": "T1562.001",
        "tactic": "defense-evasion",
        "score": 9,
        "color": "#ff3864",
        "comment": "T1562.001: SHA-256 FIM 무결성 감시 - 핵심 코드 변조 0.1초 감지 및 자동 롤백",
        "enabled": true
      }
    ],
    "gradient": {
      "colors": ["#0f172a", "#00e5ff", "#ffb300", "#ff3864"],
      "minValue": 0,
      "maxValue": 10
    },
    "legendItems": [
      { "label": "정상 대기 (Clean Baseline)", "color": "#00e676" },
      { "label": "능동 격리 완료 (Active Defense)", "color": "#00e5ff" },
      { "label": "고위험 침해 시도 (High Threat)", "color": "#ffb300" },
      { "label": "크리티컬 커널 차단 (Critical Block)", "color": "#ff3864" }
    ]
  };

  function initMitreJsonModal() {
    const btnOpen = document.getElementById("btnOpenMitreJson");
    const modal = document.getElementById("mitreJsonModal");
    const closeBtn = document.getElementById("mitreJsonCloseBtn");
    const copyBtn = document.getElementById("btnCopyMitreJson");
    const downloadBtn = document.getElementById("btnDownloadMitreJson");
    const codeTarget = document.getElementById("mitreJsonTarget");

    if (codeTarget) {
      codeTarget.textContent = JSON.stringify(mitreLayerData, null, 2);
    }

    if (btnOpen && modal) {
      btnOpen.addEventListener("click", () => {
        SoundFX.clickTick();
        modal.classList.add("active");
      });
    }

    if (closeBtn && modal) {
      closeBtn.addEventListener("click", () => {
        modal.classList.remove("active");
      });
    }

    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.remove("active");
      });
    }

    if (copyBtn) {
      copyBtn.addEventListener("click", () => {
        SoundFX.clickTick();
        navigator.clipboard.writeText(JSON.stringify(mitreLayerData, null, 2)).then(() => {
          const orig = copyBtn.textContent;
          copyBtn.textContent = "복사 완료! ✓";
          setTimeout(() => (copyBtn.textContent = orig), 2000);
        });
      });
    }

    if (downloadBtn) {
      downloadBtn.addEventListener("click", () => {
        SoundFX.clickTick();
        const blob = new Blob([JSON.stringify(mitreLayerData, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "nexus_guard_mitre_layer_v4.5.json";
        a.click();
        URL.revokeObjectURL(url);
      });
    }
  }

  // --------------------------------------------------------------------------
  // 9. Standalone Fallback Modal
  // --------------------------------------------------------------------------
  function initFallbackModal() {
    const trigger = document.getElementById("btnStandaloneFallbackInfo");
    const modal = document.getElementById("fallbackModal");
    const closeBtn = document.getElementById("fallbackCloseBtn");

    if (trigger && modal) {
      trigger.addEventListener("click", () => {
        SoundFX.clickTick();
        modal.classList.add("active");
      });
    }

    if (closeBtn && modal) {
      closeBtn.addEventListener("click", () => {
        modal.classList.remove("active");
      });
    }

    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.remove("active");
      });
    }
  }

  // --------------------------------------------------------------------------
  // 10. Print Handler (PDF Export)
  // --------------------------------------------------------------------------
  function initPrintHandler() {
    const printButtons = document.querySelectorAll(".btn-print");
    printButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        SoundFX.clickTick();
        window.print();
      });
    });
  }

  // Global Architecture View Switcher
  window.switchArchView = function (type) {
    const teamView = document.getElementById("archViewTeam");
    const guardView = document.getElementById("archViewGuard");
    const btnTeam = document.getElementById("btnShowTeamArch");
    const btnGuard = document.getElementById("btnShowGuardArch");

    if (!teamView || !guardView) return;

    if (type === "team") {
      teamView.style.display = "block";
      guardView.style.display = "none";
      if (btnTeam) {
        btnTeam.className = "btn btn-primary btn-sm";
      }
      if (btnGuard) {
        btnGuard.className = "btn btn-outline btn-sm";
      }
    } else {
      teamView.style.display = "none";
      guardView.style.display = "block";
      if (btnTeam) {
        btnTeam.className = "btn btn-outline btn-sm";
      }
      if (btnGuard) {
        btnGuard.className = "btn btn-primary btn-sm";
      }
    }
  };

  // Video Demonstration Time Jump Controller
  window.jumpVideo = function (seconds) {
    const video = document.getElementById("demoVideoPlayer");
    if (!video) return;
    video.currentTime = seconds;
    video.play().catch(() => {});
    SoundFX.clickTick();
  };

  // Initialize sound on first user gesture

  document.addEventListener("click", () => {
    if (!SoundFX.ctx) SoundFX.init();
  }, { once: true });

})();
