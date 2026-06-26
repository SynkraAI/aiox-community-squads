#!/usr/bin/env bash
# ==============================================================================
# ETL Env Bootstrap — Diagnose and install ETL-Ops runtime dependencies
# EXEC-W-001 | Worker | Deterministic
# ==============================================================================
set -euo pipefail

# ==============================================================================
# LOGGING (TTY-aware colors)
# ==============================================================================

if [ -t 2 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  CYAN='\033[0;36m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' CYAN='' BOLD='' NC=''
fi

log_info()    { echo -e "${BLUE}[INFO]${NC} $*" >&2; }
log_success() { echo -e "${GREEN}[OK]${NC} $*" >&2; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $*" >&2; }
log_error()   { echo -e "${RED}[FAIL]${NC} $*" >&2; }
log_section() { echo -e "\n${BOLD}${CYAN}── $* ──${NC}" >&2; }

# ==============================================================================
# MODE PARSING
# ==============================================================================

MODE="check"
HELP=false

while [ $# -gt 0 ]; do
  case "$1" in
    --check)          MODE="check"; shift ;;
    --core)           MODE="core"; shift ;;
    --full)           MODE="full"; shift ;;
    --install-media)  MODE="install-media"; shift ;;
    --install-ebook)  MODE="install-ebook"; shift ;;
    --help|-h)        HELP=true; shift ;;
    *)                log_error "Unknown option: $1"; exit 1 ;;
  esac
done

if [ "$HELP" = true ]; then
  cat >&2 <<'USAGE'
ETL Env Bootstrap — Diagnose and install ETL-Ops runtime dependencies

Usage: etl-env-bootstrap.sh [mode]

Modes:
  --check           Diagnose only, no installs (default)
  --core            Install core: npm deps + scrapling + curl + jq
  --full            Install everything (core + media + ebook + web)
  --install-media   Add media tools (ffmpeg, yt-dlp, whisper)
  --install-ebook   Add ebook tools (pandoc, calibre)

Exit codes:
  0 — Everything ready for the requested scope
  1 — Something missing or failed

Output:
  stderr — Human messages (progress, diagnostics)
  stdout — JSON report
USAGE
  exit 0
fi

# ==============================================================================
# OS DETECTION
# ==============================================================================

OS_TYPE="unknown"
PKG_INSTALL=""

case "$(uname -s)" in
  Darwin*)
    OS_TYPE="darwin"
    if command -v brew >/dev/null 2>&1; then
      PKG_INSTALL="brew install"
    else
      log_warning "Homebrew not found. System package installs will be skipped."
    fi
    ;;
  Linux*)
    OS_TYPE="linux"
    if command -v apt-get >/dev/null 2>&1; then
      PKG_INSTALL="sudo apt-get install -y"
    elif command -v dnf >/dev/null 2>&1; then
      PKG_INSTALL="sudo dnf install -y"
    else
      log_warning "No supported package manager found. System package installs will be skipped."
    fi
    ;;
esac

log_info "OS detected: ${OS_TYPE} | Package manager: ${PKG_INSTALL:-none}"

# ==============================================================================
# RESOLVE PATHS
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SQUAD_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Walk up to find repo root (where .aiox-core/ or root package.json lives)
REPO_ROOT="$SQUAD_ROOT"
while [ "$REPO_ROOT" != "/" ]; do
  if [ -d "$REPO_ROOT/.aiox-core" ] || [ -f "$REPO_ROOT/package.json" ]; then
    break
  fi
  REPO_ROOT="$(dirname "$REPO_ROOT")"
done

ETL_SERVICE_DIR=""
for candidate in \
  "${REPO_ROOT}/services/etl" \
  "${REPO_ROOT}/infrastructure/services/etl"
do
  if [ -d "$candidate" ]; then
    ETL_SERVICE_DIR="$candidate"
    break
  fi
done

if [ -z "$ETL_SERVICE_DIR" ]; then
  ETL_SERVICE_DIR="${REPO_ROOT}/services/etl"
fi

ETL_SERVICE_REF="${ETL_SERVICE_DIR#$REPO_ROOT/}"
if [ "$ETL_SERVICE_REF" = "$ETL_SERVICE_DIR" ]; then
  ETL_SERVICE_REF="$ETL_SERVICE_DIR"
fi

log_info "Repo root: ${REPO_ROOT}"
log_info "ETL service: ${ETL_SERVICE_DIR}"
log_info "ETL service ref: ${ETL_SERVICE_REF}"

# ==============================================================================
# TOOL REGISTRY (parallel arrays — Bash 3.2 compatible, no declare -A)
# ==============================================================================

TOOL_NAMES=()
TOOL_STATUSES=()
TOOL_VERSIONS=()
TOOL_CATEGORIES=()

register_tool() {
  local name="$1" status="$2" version="$3" category="$4"
  TOOL_NAMES+=("$name")
  TOOL_STATUSES+=("$status")
  TOOL_VERSIONS+=("$version")
  TOOL_CATEGORIES+=("$category")
}

ENV_NAMES=()
ENV_STATUSES=()

register_env() {
  local name="$1" status="$2"
  ENV_NAMES+=("$name")
  ENV_STATUSES+=("$status")
}

# ==============================================================================
# CHECK FUNCTIONS
# ==============================================================================

check_command() {
  local name="$1" category="$2"
  local version=""
  if command -v "$name" >/dev/null 2>&1; then
    case "$name" in
      node)        version="$(node --version 2>/dev/null || echo "?")" ;;
      npm)         version="$(npm --version 2>/dev/null || echo "?")" ;;
      python3)     version="$(python3 --version 2>/dev/null | awk '{print $2}' || echo "?")" ;;
      pip3|pip)    version="$(pip3 --version 2>/dev/null | awk '{print $2}' || echo "?")" ;;
      curl)        version="$(curl --version 2>/dev/null | head -1 | awk '{print $2}' || echo "?")" ;;
      jq)          version="$(jq --version 2>/dev/null | sed 's/jq-//' || echo "?")" ;;
      ffmpeg)      version="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}' || echo "?")" ;;
      ffprobe)     version="$(ffprobe -version 2>/dev/null | head -1 | awk '{print $3}' || echo "?")" ;;
      yt-dlp)      version="$(yt-dlp --version 2>/dev/null || echo "?")" ;;
      pandoc)      version="$(pandoc --version 2>/dev/null | head -1 | awk '{print $2}' || echo "?")" ;;
      scenedetect) version="$(scenedetect --version 2>/dev/null | awk '{print $NF}' || echo "?")" ;;
      *)           version="installed" ;;
    esac
    register_tool "$name" "installed" "$version" "$category"
    log_success "$name ($version)"
    return 0
  else
    register_tool "$name" "missing" "-" "$category"
    log_error "$name — not found"
    return 1
  fi
}

check_core() {
  log_section "Core Tools"
  local ok=0
  check_command "node"    "core" || ok=1
  check_command "npm"     "core" || ok=1
  check_command "python3" "core" || ok=1
  check_command "curl"    "core" || ok=1
  check_command "jq"      "core" || ok=1
  return $ok
}

check_node_deps() {
  log_section "Node.js Dependencies"
  if [ ! -d "$ETL_SERVICE_DIR" ]; then
    register_tool "npm-deps" "missing" "-" "node"
    log_error "ETL service directory not found: $ETL_SERVICE_DIR"
    return 1
  fi
  if [ ! -f "$ETL_SERVICE_DIR/package.json" ]; then
    register_tool "npm-deps" "missing" "-" "node"
    log_error "package.json not found in $ETL_SERVICE_DIR"
    return 1
  fi
  if [ -d "$ETL_SERVICE_DIR/node_modules" ]; then
    register_tool "npm-deps" "installed" "present" "node"
    log_success "npm-deps (node_modules present)"
    return 0
  else
    register_tool "npm-deps" "missing" "-" "node"
    log_warning "npm-deps — node_modules not found in $ETL_SERVICE_DIR"
    return 1
  fi
}

check_python_deps() {
  log_section "Python Dependencies"
  if ! command -v python3 >/dev/null 2>&1; then
    register_tool "scrapling" "missing" "-" "python"
    log_warning "scrapling — python3 not available"
    return 1
  fi
  if python3 -c "import scrapling" >/dev/null 2>&1; then
    local ver
    ver="$(python3 -c "import scrapling; print(getattr(scrapling, '__version__', 'installed'))" 2>/dev/null || echo "installed")"
    register_tool "scrapling" "installed" "$ver" "python"
    log_success "scrapling ($ver)"
    return 0
  else
    register_tool "scrapling" "missing" "-" "python"
    log_warning "scrapling — not importable by python3"
    return 1
  fi
}

check_media() {
  log_section "Media Tools"
  local ok=0
  check_command "ffmpeg"   "media" || ok=1
  check_command "ffprobe"  "media" || ok=1
  check_command "yt-dlp"   "media" || ok=1

  # Whisper CLI — check both 'whisper' and 'whisper-cli' binaries
  if command -v whisper >/dev/null 2>&1; then
    local ver
    ver="$(whisper --version 2>/dev/null || echo "?")"
    register_tool "whisper-cli" "installed" "$ver" "media"
    log_success "whisper-cli ($ver)"
  elif command -v whisper-cli >/dev/null 2>&1; then
    register_tool "whisper-cli" "installed" "present" "media"
    log_success "whisper-cli (present)"
  else
    register_tool "whisper-cli" "missing" "-" "media"
    log_warning "whisper-cli — not found"
    ok=1
  fi

  check_command "scenedetect" "media" || ok=1

  return $ok
}

check_ebook() {
  log_section "Ebook Tools"
  local ok=0
  check_command "pandoc" "ebook" || ok=1

  # Calibre: also check macOS app bundle path
  if command -v ebook-convert >/dev/null 2>&1; then
    local ver
    ver="$(ebook-convert --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "?")"
    register_tool "ebook-convert" "installed" "$ver" "ebook"
    log_success "ebook-convert ($ver)"
  elif [ "$OS_TYPE" = "darwin" ] && [ -x "/Applications/calibre.app/Contents/MacOS/ebook-convert" ]; then
    local ver
    ver="$(/Applications/calibre.app/Contents/MacOS/ebook-convert --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "?")"
    register_tool "ebook-convert" "installed" "$ver (app bundle)" "ebook"
    log_success "ebook-convert ($ver via calibre.app)"
  else
    register_tool "ebook-convert" "missing" "-" "ebook"
    log_warning "ebook-convert (calibre) — not found"
    ok=1
  fi

  return $ok
}

check_web_extended() {
  log_section "Web Extended Tools"
  if command -v firecrawl >/dev/null 2>&1; then
    register_tool "firecrawl-cli" "installed" "present" "web"
    log_success "firecrawl-cli"
    return 0
  else
    register_tool "firecrawl-cli" "missing" "-" "web"
    log_warning "firecrawl-cli — not found"
    return 1
  fi
}

check_env_vars() {
  log_section "Environment Variables"
  local vars=("CLOUDFLARE_API_TOKEN" "CLOUDFLARE_ACCOUNT_ID" "FIRECRAWL_API_KEY" "OPENROUTER_API_KEY" "WHISPER_MODEL_PATH")
  for var in "${vars[@]}"; do
    if [ -n "${!var:-}" ]; then
      register_env "$var" "set"
      log_success "$var — set"
    else
      register_env "$var" "unset"
      log_warning "$var — not set"
    fi
  done
}

# ==============================================================================
# INSTALL FUNCTIONS
# Wrapped in set +e to prevent individual failures from killing the script.
# Every install is idempotent — skips if already present.
# ==============================================================================

install_core() {
  log_section "Installing Core Dependencies"

  # Node/npm: advisory only (protected paths like ~/.nvm)
  if ! command -v node >/dev/null 2>&1; then
    log_warning "Node.js not found. Install it manually (nvm, brew, or official installer)."
    log_info "  Recommended: nvm install --lts"
  fi

  # curl
  if ! command -v curl >/dev/null 2>&1 && [ -n "$PKG_INSTALL" ]; then
    log_info "Installing curl..."
    $PKG_INSTALL curl || log_warning "Failed to install curl"
  fi

  # jq
  if ! command -v jq >/dev/null 2>&1 && [ -n "$PKG_INSTALL" ]; then
    log_info "Installing jq..."
    $PKG_INSTALL jq || log_warning "Failed to install jq"
  fi

  # npm dependencies in ETL service directory
  if [ -d "$ETL_SERVICE_DIR" ] && [ -f "$ETL_SERVICE_DIR/package.json" ]; then
    if [ ! -d "$ETL_SERVICE_DIR/node_modules" ] && command -v npm >/dev/null 2>&1; then
      log_info "Installing npm dependencies in $ETL_SERVICE_DIR..."
      (cd "$ETL_SERVICE_DIR" && npm install) || log_warning "npm install failed"
    fi
  fi

  # scrapling (Python) — requires python3
  if command -v python3 >/dev/null 2>&1; then
    if ! python3 -c "import scrapling" >/dev/null 2>&1; then
      log_info "Installing scrapling..."
      if [ -f "$ETL_SERVICE_DIR/requirements.txt" ]; then
        if [ -n "${VIRTUAL_ENV:-}" ]; then
          pip install -r "$ETL_SERVICE_DIR/requirements.txt" || log_warning "pip install from requirements.txt failed"
        else
          pip3 install --user -r "$ETL_SERVICE_DIR/requirements.txt" || log_warning "pip3 install from requirements.txt failed"
        fi
      else
        if [ -n "${VIRTUAL_ENV:-}" ]; then
          pip install "scrapling>=0.2" || log_warning "pip install scrapling failed"
        else
          pip3 install --user "scrapling>=0.2" || log_warning "pip3 install scrapling failed"
        fi
      fi
    fi
  else
    log_warning "python3 not found — cannot install scrapling"
  fi
}

install_media() {
  log_section "Installing Media Tools"

  if [ -z "$PKG_INSTALL" ]; then
    log_warning "No package manager available. Install media tools manually."
    return 0
  fi

  # ffmpeg (includes ffprobe)
  if ! command -v ffmpeg >/dev/null 2>&1; then
    log_info "Installing ffmpeg..."
    $PKG_INSTALL ffmpeg || log_warning "Failed to install ffmpeg"
  fi

  # yt-dlp
  if ! command -v yt-dlp >/dev/null 2>&1; then
    log_info "Installing yt-dlp..."
    if [ "$OS_TYPE" = "darwin" ]; then
      brew install yt-dlp || log_warning "Failed to install yt-dlp"
    else
      $PKG_INSTALL yt-dlp 2>/dev/null || pip3 install --user yt-dlp || log_warning "Failed to install yt-dlp"
    fi
  fi

  # whisper
  if ! command -v whisper >/dev/null 2>&1 && ! command -v whisper-cli >/dev/null 2>&1; then
    if command -v pip3 >/dev/null 2>&1; then
      log_info "Installing openai-whisper..."
      if [ -n "${VIRTUAL_ENV:-}" ]; then
        pip install openai-whisper || log_warning "Failed to install openai-whisper"
      else
        pip3 install --user openai-whisper || log_warning "Failed to install openai-whisper"
      fi
    else
      log_warning "pip3 not found — cannot install whisper"
    fi
  fi

  # scenedetect
  if ! command -v scenedetect >/dev/null 2>&1; then
    if command -v pip3 >/dev/null 2>&1; then
      log_info "Installing scenedetect..."
      if [ -n "${VIRTUAL_ENV:-}" ]; then
        pip install "scenedetect[opencv]" || log_warning "Failed to install scenedetect"
      else
        pip3 install --user "scenedetect[opencv]" || log_warning "Failed to install scenedetect"
      fi
    else
      log_warning "pip3 not found — cannot install scenedetect"
    fi
  fi
}

install_ebook() {
  log_section "Installing Ebook Tools"

  if [ -z "$PKG_INSTALL" ]; then
    log_warning "No package manager available. Install ebook tools manually."
    return 0
  fi

  # pandoc
  if ! command -v pandoc >/dev/null 2>&1; then
    log_info "Installing pandoc..."
    $PKG_INSTALL pandoc || log_warning "Failed to install pandoc"
  fi

  # calibre
  if ! command -v ebook-convert >/dev/null 2>&1; then
    if [ "$OS_TYPE" = "darwin" ]; then
      if [ ! -x "/Applications/calibre.app/Contents/MacOS/ebook-convert" ]; then
        log_info "Installing calibre via brew..."
        brew install --cask calibre || log_warning "Failed to install calibre"
      fi
    else
      log_info "Installing calibre..."
      $PKG_INSTALL calibre || log_warning "Failed to install calibre"
    fi
  fi
}

install_web_extended() {
  log_section "Installing Web Extended Tools"

  if ! command -v firecrawl >/dev/null 2>&1; then
    if command -v npx >/dev/null 2>&1; then
      log_info "Installing firecrawl-cli..."
      npx -y firecrawl-cli@latest init --all --browser || log_warning "Failed to install firecrawl-cli"
    else
      log_warning "npx not found — cannot install firecrawl-cli"
    fi
  fi
}

# ==============================================================================
# DO INSTALL (by scope)
# ==============================================================================

do_install() {
  case "$MODE" in
    core)
      install_core
      ;;
    full)
      install_core
      install_media
      install_ebook
      install_web_extended
      ;;
    install-media)
      install_media
      ;;
    install-ebook)
      install_ebook
      ;;
  esac
}

# ==============================================================================
# PROFILE READINESS ASSESSMENT
# ==============================================================================

tool_status() {
  local name="$1"
  local i=0
  while [ $i -lt ${#TOOL_NAMES[@]} ]; do
    if [ "${TOOL_NAMES[$i]}" = "$name" ]; then
      echo "${TOOL_STATUSES[$i]}"
      return
    fi
    i=$((i + 1))
  done
  echo "unchecked"
}

env_status() {
  local name="$1"
  local i=0
  while [ $i -lt ${#ENV_NAMES[@]} ]; do
    if [ "${ENV_NAMES[$i]}" = "$name" ]; then
      echo "${ENV_STATUSES[$i]}"
      return
    fi
    i=$((i + 1))
  done
  echo "unchecked"
}

has_tool() { [ "$(tool_status "$1")" = "installed" ]; }
has_env()  { [ "$(env_status "$1")" = "set" ]; }

PROFILE_NAMES=()
PROFILE_STATUSES=()
PROFILE_NOTES=()

assess_profile() {
  local name="$1" status="$2" note="$3"
  PROFILE_NAMES+=("$name")
  PROFILE_STATUSES+=("$status")
  PROFILE_NOTES+=("$note")
}

assess_profiles() {
  log_section "Profile Readiness"

  # youtube_video, youtube_channel, youtube_podcast, youtube_metadata
  # No fallback — node + npm-deps are both required for any YouTube extractor
  for p in youtube_video youtube_channel youtube_podcast youtube_metadata; do
    if has_tool "node" && has_tool "npm-deps"; then
      assess_profile "$p" "READY" ""
      log_success "$p — READY"
    else
      local missing=""
      has_tool "node" || missing="node"
      has_tool "npm-deps" || missing="${missing:+$missing, }npm-deps"
      assess_profile "$p" "UNAVAILABLE" "missing: $missing"
      log_error "$p — UNAVAILABLE ($missing)"
    fi
  done

  # web_page — primary: fetch-page.js (node+npm-deps), fallback: scrapling
  if has_tool "node" && has_tool "npm-deps"; then
    assess_profile "web_page" "READY" ""
    log_success "web_page — READY"
  elif has_tool "scrapling"; then
    assess_profile "web_page" "DEGRADED" "scrapling fallback (fetch-page.js unavailable)"
    log_warning "web_page — DEGRADED (scrapling fallback)"
  else
    local missing=""
    has_tool "node" || missing="node"
    has_tool "npm-deps" || missing="${missing:+$missing, }npm-deps"
    has_tool "scrapling" || missing="${missing:+$missing, }scrapling"
    assess_profile "web_page" "UNAVAILABLE" "missing: $missing"
    log_error "web_page — UNAVAILABLE ($missing)"
  fi

  # web_page_protected — requires scrapling (no alternative)
  if has_tool "scrapling"; then
    assess_profile "web_page_protected" "READY" ""
    log_success "web_page_protected — READY"
  else
    assess_profile "web_page_protected" "UNAVAILABLE" "missing: scrapling"
    log_error "web_page_protected — UNAVAILABLE (scrapling)"
  fi

  # web_page_js_heavy — primary: cloudflare-crawl.sh, fallback chain: scrapling → firecrawl
  if has_tool "curl" && has_tool "jq" && has_env "CLOUDFLARE_API_TOKEN" && has_env "CLOUDFLARE_ACCOUNT_ID"; then
    assess_profile "web_page_js_heavy" "READY" ""
    log_success "web_page_js_heavy — READY"
  elif has_tool "scrapling"; then
    assess_profile "web_page_js_heavy" "DEGRADED" "scrapling fallback (Cloudflare env vars not set)"
    log_warning "web_page_js_heavy — DEGRADED (scrapling fallback)"
  elif has_env "FIRECRAWL_API_KEY"; then
    assess_profile "web_page_js_heavy" "DEGRADED" "firecrawl fallback (Cloudflare + scrapling unavailable)"
    log_warning "web_page_js_heavy — DEGRADED (firecrawl fallback)"
  else
    assess_profile "web_page_js_heavy" "UNAVAILABLE" "no Cloudflare env, no scrapling, no Firecrawl"
    log_error "web_page_js_heavy — UNAVAILABLE"
  fi

  # site_crawl — primary: cloudflare-crawl.sh, fallback: firecrawl crawl
  if has_tool "curl" && has_tool "jq" && has_env "CLOUDFLARE_API_TOKEN" && has_env "CLOUDFLARE_ACCOUNT_ID"; then
    assess_profile "site_crawl" "READY" ""
    log_success "site_crawl — READY"
  elif has_env "FIRECRAWL_API_KEY"; then
    assess_profile "site_crawl" "DEGRADED" "firecrawl fallback (Cloudflare env vars not set)"
    log_warning "site_crawl — DEGRADED (firecrawl fallback)"
  else
    assess_profile "site_crawl" "UNAVAILABLE" "no Cloudflare env, no FIRECRAWL_API_KEY"
    log_error "site_crawl — UNAVAILABLE"
  fi

  # search_and_scrape — requires FIRECRAWL_API_KEY (no alternative)
  if has_env "FIRECRAWL_API_KEY"; then
    assess_profile "search_and_scrape" "READY" ""
    log_success "search_and_scrape — READY"
  else
    assess_profile "search_and_scrape" "UNAVAILABLE" "missing: FIRECRAWL_API_KEY"
    log_error "search_and_scrape — UNAVAILABLE"
  fi

  # ebook_epub — primary: ebook-to-markdown.js (node+npm-deps), enhanced with pandoc
  if has_tool "node" && has_tool "npm-deps"; then
    if has_tool "pandoc"; then
      assess_profile "ebook_epub" "READY" ""
      log_success "ebook_epub — READY"
    else
      assess_profile "ebook_epub" "DEGRADED" "pandoc missing (basic conversion only)"
      log_warning "ebook_epub — DEGRADED (no pandoc)"
    fi
  else
    assess_profile "ebook_epub" "UNAVAILABLE" "missing: node/npm-deps"
    log_error "ebook_epub — UNAVAILABLE"
  fi

  # pdf_document — requires node + npm-deps (pdf-collector.js)
  if has_tool "node" && has_tool "npm-deps"; then
    assess_profile "pdf_document" "READY" ""
    log_success "pdf_document — READY"
  else
    assess_profile "pdf_document" "UNAVAILABLE" "missing: node/npm-deps"
    log_error "pdf_document — UNAVAILABLE"
  fi

  # audio_transcription — requires ffmpeg + whisper
  if has_tool "ffmpeg" && has_tool "whisper-cli"; then
    if has_env "WHISPER_MODEL_PATH"; then
      assess_profile "audio_transcription" "READY" ""
      log_success "audio_transcription — READY"
    else
      assess_profile "audio_transcription" "DEGRADED" "WHISPER_MODEL_PATH not set (will use default model)"
      log_warning "audio_transcription — DEGRADED (no WHISPER_MODEL_PATH)"
    fi
  else
    local missing=""
    has_tool "ffmpeg" || missing="ffmpeg"
    has_tool "whisper-cli" || missing="${missing:+$missing, }whisper"
    assess_profile "audio_transcription" "UNAVAILABLE" "missing: $missing"
    log_error "audio_transcription — UNAVAILABLE ($missing)"
  fi

  # video_transcription — requires ffmpeg + whisper
  if has_tool "ffmpeg" && has_tool "whisper-cli"; then
    assess_profile "video_transcription" "READY" ""
    log_success "video_transcription — READY"
  else
    local missing=""
    has_tool "ffmpeg" || missing="ffmpeg"
    has_tool "whisper-cli" || missing="${missing:+$missing, }whisper"
    assess_profile "video_transcription" "UNAVAILABLE" "missing: $missing"
    log_error "video_transcription — UNAVAILABLE ($missing)"
  fi

  # video_multimodal — requires ffmpeg + whisper, enhanced with scenedetect
  if has_tool "ffmpeg" && has_tool "whisper-cli"; then
    if has_tool "scenedetect"; then
      assess_profile "video_multimodal" "READY" ""
      log_success "video_multimodal — READY"
    else
      assess_profile "video_multimodal" "DEGRADED" "scenedetect missing (ffmpeg scene filter fallback)"
      log_warning "video_multimodal — DEGRADED (no scenedetect)"
    fi
  else
    local missing=""
    has_tool "ffmpeg" || missing="ffmpeg"
    has_tool "whisper-cli" || missing="${missing:+$missing, }whisper"
    assess_profile "video_multimodal" "UNAVAILABLE" "missing: $missing"
    log_error "video_multimodal — UNAVAILABLE ($missing)"
  fi

  # direct_video_url — requires ffmpeg + whisper
  if has_tool "ffmpeg" && has_tool "whisper-cli"; then
    assess_profile "direct_video_url" "READY" ""
    log_success "direct_video_url — READY"
  else
    local missing=""
    has_tool "ffmpeg" || missing="ffmpeg"
    has_tool "whisper-cli" || missing="${missing:+$missing, }whisper"
    assess_profile "direct_video_url" "UNAVAILABLE" "missing: $missing"
    log_error "direct_video_url — UNAVAILABLE ($missing)"
  fi

  # generic_document — requires node + npm-deps (document-collector.js)
  if has_tool "node" && has_tool "npm-deps"; then
    assess_profile "generic_document" "READY" ""
    log_success "generic_document — READY"
  else
    assess_profile "generic_document" "UNAVAILABLE" "missing: node/npm-deps"
    log_error "generic_document — UNAVAILABLE"
  fi
}

# ==============================================================================
# JSON REPORT
# ==============================================================================

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\t'/\\t}"
  s="${s//$'\r'/}"
  s="${s//$'\n'/\\n}"
  printf '%s' "$s"
}

# Count profiles by status — sets PROF_READY, PROF_DEGRADED, PROF_UNAVAILABLE
count_profiles() {
  PROF_READY=0
  PROF_DEGRADED=0
  PROF_UNAVAILABLE=0
  local i=0
  while [ $i -lt ${#PROFILE_STATUSES[@]} ]; do
    case "${PROFILE_STATUSES[$i]}" in
      READY)       PROF_READY=$((PROF_READY + 1)) ;;
      DEGRADED)    PROF_DEGRADED=$((PROF_DEGRADED + 1)) ;;
      UNAVAILABLE) PROF_UNAVAILABLE=$((PROF_UNAVAILABLE + 1)) ;;
    esac
    i=$((i + 1))
  done
}

emit_json() {
  local has_jq=false
  command -v jq >/dev/null 2>&1 && has_jq=true

  count_profiles

  local json=""
  json+='{'
  json+="\"mode\":\"$MODE\","
  json+="\"os\":\"$OS_TYPE\","
  json+="\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","

  # Tools
  json+='"tools":['
  local i=0
  while [ $i -lt ${#TOOL_NAMES[@]} ]; do
    [ $i -gt 0 ] && json+=','
    json+="{\"name\":\"${TOOL_NAMES[$i]}\",\"status\":\"${TOOL_STATUSES[$i]}\",\"version\":\"$(json_escape "${TOOL_VERSIONS[$i]}")\",\"category\":\"${TOOL_CATEGORIES[$i]}\"}"
    i=$((i + 1))
  done
  json+='],'

  # Env vars
  json+='"env_vars":['
  i=0
  while [ $i -lt ${#ENV_NAMES[@]} ]; do
    [ $i -gt 0 ] && json+=','
    json+="{\"name\":\"${ENV_NAMES[$i]}\",\"status\":\"${ENV_STATUSES[$i]}\"}"
    i=$((i + 1))
  done
  json+='],'

  # Profiles
  json+='"profiles":['
  i=0
  while [ $i -lt ${#PROFILE_NAMES[@]} ]; do
    [ $i -gt 0 ] && json+=','
    json+="{\"name\":\"${PROFILE_NAMES[$i]}\",\"status\":\"${PROFILE_STATUSES[$i]}\",\"note\":\"$(json_escape "${PROFILE_NOTES[$i]}")\"}"
    i=$((i + 1))
  done
  json+='],'

  # Summary
  json+="\"summary\":{\"profiles_ready\":$PROF_READY,\"profiles_degraded\":$PROF_DEGRADED,\"profiles_unavailable\":$PROF_UNAVAILABLE,\"profiles_total\":${#PROFILE_NAMES[@]}}"

  json+='}'

  if [ "$has_jq" = true ]; then
    echo "$json" | jq .
  else
    echo "$json"
  fi
}

# ==============================================================================
# SUMMARY TABLE
# ==============================================================================

print_summary() {
  log_section "Summary"

  # count_profiles already called by emit_json
  local total=${#PROFILE_NAMES[@]}
  echo -e "${GREEN}READY:${NC}       $PROF_READY / $total" >&2
  echo -e "${YELLOW}DEGRADED:${NC}    $PROF_DEGRADED / $total" >&2
  echo -e "${RED}UNAVAILABLE:${NC} $PROF_UNAVAILABLE / $total" >&2

  if [ "$PROF_UNAVAILABLE" -eq 0 ] && [ "$PROF_DEGRADED" -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}All profiles fully operational.${NC}" >&2
  elif [ "$PROF_UNAVAILABLE" -eq 0 ]; then
    echo -e "\n${YELLOW}${BOLD}All profiles functional (some degraded).${NC}" >&2
  else
    echo -e "\n${RED}${BOLD}Some profiles unavailable. Run with --core or --full to install dependencies.${NC}" >&2
  fi
}

# ==============================================================================
# MAIN
# ==============================================================================

main() {
  log_section "ETL Env Bootstrap (mode: $MODE)"

  # Phase 1: Install (if requested)
  # Temporarily disable set -e so install failures don't kill diagnosis
  if [ "$MODE" != "check" ]; then
    set +e
    do_install
    set -e
    log_info "Install phase complete — running full diagnosis..."
  fi

  # Phase 2: Full diagnosis (always runs, re-checks after install)
  TOOL_NAMES=()
  TOOL_STATUSES=()
  TOOL_VERSIONS=()
  TOOL_CATEGORIES=()
  ENV_NAMES=()
  ENV_STATUSES=()
  PROFILE_NAMES=()
  PROFILE_STATUSES=()
  PROFILE_NOTES=()

  check_core          || true
  check_node_deps     || true
  check_python_deps   || true
  check_media         || true
  check_ebook         || true
  check_web_extended  || true
  check_env_vars

  # Phase 3: Assess profiles
  assess_profiles

  # Phase 4: Report
  emit_json
  print_summary

  # Exit code: 0 if no UNAVAILABLE, 1 otherwise
  [ "$PROF_UNAVAILABLE" -eq 0 ]
}

main
