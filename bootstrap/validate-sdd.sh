#!/usr/bin/env bash
# Valida coherencia documental de una instancia SDD.
# Uso: ./sdd-kit/bootstrap/validate-sdd.sh [.github/docs/sdd]
# Codigos de salida: 0=OK, 1=fallo del script/entorno (FATAL), 2=incoherencias documentales (ERROR)
# Salida por componente (SDD-010): [backlog] [specs] [config] [agent] [kit-version] [docs] [metrics]

set -euo pipefail

SDD_PATH="${1:-.github/docs/sdd}"
ERRORS=0
WARNINGS=0
LAST_COMPONENT=""
# component stats as parallel arrays via associative: name -> "errors:warnings:messages"
declare -A COMP_STATS
declare -a COMP_ORDER=()

ensure_component() {
  local c="$1"
  if [[ -z "${COMP_STATS[$c]:-}" ]]; then
    COMP_STATS[$c]="0:0:0"
    COMP_ORDER+=("$c")
  fi
  if [[ "$LAST_COMPONENT" != "$c" ]]; then
    echo ""
    echo "--- [$c] ---"
    LAST_COMPONENT="$c"
  fi
}

bump_stat() {
  local c="$1" field="$2"
  local e w m
  IFS=':' read -r e w m <<< "${COMP_STATS[$c]}"
  case "$field" in
    e) e=$((e + 1)); m=$((m + 1)) ;;
    w) w=$((w + 1)); m=$((m + 1)) ;;
    m) m=$((m + 1)) ;;
  esac
  COMP_STATS[$c]="$e:$w:$m"
}

fatal() {
  echo "FATAL: $1"
  echo ""
  echo "La validacion no pudo ejecutarse (exit 1)."
  exit 1
}

err() { ensure_component "$1"; echo "[$1] ERROR: $2"; ERRORS=$((ERRORS + 1)); bump_stat "$1" e; }
warn() { ensure_component "$1"; echo "[$1] WARN:  $2"; WARNINGS=$((WARNINGS + 1)); bump_stat "$1" w; }
ok() { ensure_component "$1"; echo "[$1] OK:    $2"; bump_stat "$1" m; }

echo ""
echo "=== Validacion SDD ($SDD_PATH) ==="

if [[ ! -d "$SDD_PATH" ]]; then
  fatal "No existe el directorio SDD: $SDD_PATH"
fi

BACKLOG="$SDD_PATH/BACKLOG.md"
if [[ ! -f "$BACKLOG" ]]; then
  fatal "Falta BACKLOG.md en $SDD_PATH"
fi

# --- Extraer IDs del BACKLOG por seccion ---
declare -A BACKLOG_IDS
declare -A BACKLOG_SECTION

current_section=""
while IFS= read -r line; do
  if [[ "$line" =~ ^##[[:space:]]+(Discovery|Draft|Ready|In[[:space:]]Build|Validating|Released|Descartado) ]]; then
    current_section="${BASH_REMATCH[1]}"
    continue
  fi
  [[ "$line" =~ ^\| ]] || continue
  [[ "$line" =~ ^\|[[:space:]]*[-:] ]] && continue
  id=$(echo "$line" | cut -d'|' -f2 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  [[ "$id" =~ ^SDD-[0-9]+[a-z]?$ ]] || continue
  if [[ -n "${BACKLOG_IDS[$id]:-}" && "${BACKLOG_IDS[$id]}" != "$current_section" ]]; then
    err backlog "ID $id duplicado en BACKLOG (secciones: ${BACKLOG_IDS[$id]} y $current_section)"
  else
    BACKLOG_IDS[$id]="$current_section"
    BACKLOG_SECTION[$id]="$current_section"
  fi
done < "$BACKLOG"

# IDs en archivos specs/
declare -A FILE_IDS
declare -A FILE_DUP
while IFS= read -r -d '' f; do
  base=$(basename "$f")
  if [[ "$base" =~ ^(SDD-[0-9]+[a-z]?) ]]; then
    id="${BASH_REMATCH[1]}"
    if [[ "$f" == *"/specs/"* ]]; then
      FILE_IDS["$id"]="specs"
    elif [[ "$f" == *"/archive/"* ]]; then
      FILE_IDS["$id"]="archive"
    fi
    if [[ -n "${FILE_DUP[$id]:-}" ]]; then
      err specs "ID $id aparece en mas de un archivo"
    fi
    FILE_DUP[$id]=1
  fi
done < <(find "$SDD_PATH/specs" "$SDD_PATH/archive" -name 'SDD-*.md' -print0 2>/dev/null || true)

# Specs activos deben estar en BACKLOG
for id in "${!FILE_IDS[@]}"; do
  loc="${FILE_IDS[$id]}"
  if [[ "$loc" == "specs" ]]; then
    if [[ -z "${BACKLOG_IDS[$id]:-}" ]]; then
      err specs "Spec $id en specs/ sin entrada en BACKLOG.md"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Released" ]]; then
      err specs "Spec $id en specs/ pero BACKLOG dice Released (debe estar en archive/)"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Discovery" ]]; then
      warn specs "Spec $id en specs/ pero BACKLOG aun en Discovery (esperado Draft+)"
    else
      ok specs "Spec activo $id coherente con BACKLOG (${BACKLOG_SECTION[$id]})"
    fi
  fi
  if [[ "$loc" == "archive" ]]; then
    if [[ -z "${BACKLOG_IDS[$id]:-}" ]]; then
      err specs "Spec archivado $id sin entrada en BACKLOG.md"
    elif [[ "${BACKLOG_SECTION[$id]}" != "Released" ]]; then
      err specs "Spec $id en archive/ pero BACKLOG no esta en Released (esta en ${BACKLOG_SECTION[$id]})"
    else
      ok specs "Spec archivado $id coherente con BACKLOG"
    fi
  fi
done

# IDs en BACKLOG Draft..Validating deben tener archivo en specs/
for id in "${!BACKLOG_IDS[@]}"; do
  sec="${BACKLOG_SECTION[$id]}"
  if [[ "$sec" =~ ^(Draft|Ready|In[[:space:]]Build|Validating)$ ]]; then
    if [[ "${FILE_IDS[$id]:-}" != "specs" ]]; then
      err specs "BACKLOG: $id en $sec pero no hay archivo en specs/"
    fi
  fi
done

# Proximo ID vs max usado
if grep -q 'Próximo ID disponible\|Proximo ID disponible' "$BACKLOG"; then
  next_line=$(grep -E 'Próximo ID disponible|Proximo ID disponible' "$BACKLOG" | head -1)
  if [[ "$next_line" =~ SDD-([0-9]+) ]]; then
    next_num="${BASH_REMATCH[1]}"
    max_num=0
    for id in "${!BACKLOG_IDS[@]}"; do
      if [[ "$id" =~ SDD-([0-9]+) ]]; then
        n="${BASH_REMATCH[1]}"
        n=$((10#$n))
        (( n > max_num )) && max_num=$n
      fi
    done
    for id in "${!FILE_IDS[@]}"; do
      if [[ "$id" =~ SDD-([0-9]+) ]]; then
        n="${BASH_REMATCH[1]}"
        n=$((10#$n))
        (( n > max_num )) && max_num=$n
      fi
    done
    next_num=$((10#$next_num))
    expected=$((max_num + 1))
    if [[ $next_num -lt $expected ]]; then
      warn backlog "Proximo ID SDD-$(printf '%03d' $next_num) parece bajo (max usado: SDD-$(printf '%03d' $max_num))"
    else
      ok backlog "Proximo ID disponible coherente (max usado: SDD-$(printf '%03d' $max_num))"
    fi
  fi
fi

# sdd.config.yaml + agent (cursor manifest)
if [[ ! -f "$SDD_PATH/sdd.config.yaml" ]]; then
  warn config "Falta sdd.config.yaml"
else
  ok config "sdd.config.yaml presente"
  if grep -qE 'targets:[[:space:]]*\[[^]]*cursor' "$SDD_PATH/sdd.config.yaml"; then
    PROJECT_ROOT="$(cd "$SDD_PATH/../../.." && pwd)"
    MANIFEST="$PROJECT_ROOT/.cursor/skills/.sdd-kit-manifest.json"
    if [[ ! -f "$MANIFEST" ]]; then
      warn agent "agent.targets incluye cursor pero falta .cursor/skills/.sdd-kit-manifest.json (reinstalar con install-agents.py)"
    else
      ok agent "Manifest de skills SDD presente (.sdd-kit-manifest.json)"
    fi
  fi
fi

KIT_VERSION_SCRIPT="$(cd "$(dirname "$0")" && pwd)/kit-version.py"
if [[ -f "$KIT_VERSION_SCRIPT" ]]; then
  PROJECT_ROOT="$(cd "$SDD_PATH/../../.." && pwd)"
  if command -v python3 &>/dev/null; then
    PY=python3
  elif command -v python &>/dev/null; then
    PY=python
  else
    PY=""
  fi
  if [[ -n "$PY" ]]; then
    while IFS= read -r line; do
      if [[ "$line" == WARN:* ]]; then
        warn kit-version "${line#WARN: }"
      elif [[ "$line" == OK:* ]]; then
        ok kit-version "${line#OK: }"
      fi
    done < <("$PY" "$KIT_VERSION_SCRIPT" check "$SDD_PATH" "$PROJECT_ROOT" 2>/dev/null || true)
  fi
fi

# Dual-release (producto kit): acta campaña => nota SemVer en docs/releases/
PROJECT_ROOT_DOCS="$(cd "$SDD_PATH/../../.." && pwd)"
PRODUCT_RELEASES="$PROJECT_ROOT_DOCS/docs/releases"
CAMPAIGN_RELEASES="$SDD_PATH/releases"
if [[ -d "$PRODUCT_RELEASES" && -d "$CAMPAIGN_RELEASES" ]]; then
  dual_warns=0
  campaign_count=0
  for dir in "$CAMPAIGN_RELEASES"/v*/; do
    [[ -d "$dir" ]] || continue
    ver="$(basename "$dir")"
    [[ "$ver" =~ ^v[0-9]+\.[0-9]+\.[0-9]+ ]] || continue
    campaign_count=$((campaign_count + 1))
    if compgen -G "$dir/release_*.md" > /dev/null; then
      if [[ ! -f "$PRODUCT_RELEASES/$ver.md" ]]; then
        warn docs "dual-release: existe acta $ver/ pero falta docs/releases/$ver.md"
        dual_warns=$((dual_warns + 1))
      fi
    fi
  done
  if [[ $campaign_count -gt 0 && $dual_warns -eq 0 ]]; then
    ok docs "dual-release: actas de campana con nota producto en docs/releases/"
  fi
fi

# Token usage (SDD-013): WARN only — nunca ERROR
METRICS_DIR="$SDD_PATH/metrics"
TOKEN_USAGE="$METRICS_DIR/token-usage.json"
if [[ ! -d "$METRICS_DIR" ]]; then
  warn metrics "Falta directorio metrics/ (opcional; crear con metrics/README.md). No es ERROR."
elif [[ ! -f "$TOKEN_USAGE" ]]; then
  warn metrics "Falta metrics/token-usage.json — registrar consumo al cerrar specs (sdd-cost-governance)"
else
  if command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; then
    PY_METRICS="$(command -v python 2>/dev/null || command -v python3)"
    METRICS_OUT="$("$PY_METRICS" - "$SDD_PATH" <<'PY'
import json, sys
from pathlib import Path
sdd = Path(sys.argv[1])
path = sdd / "metrics" / "token-usage.json"
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception as e:
    print(f"WARN_JSON:{e}")
    sys.exit(0)
entries = data.get("entries") or []
print(f"OK_COUNT:{len(entries)}")
usage = {}
by_dom = {}
for e in entries:
    sid = e.get("spec_id")
    if not sid:
        continue
    tok = int(e.get("total_estimated_tokens") or 0)
    dom = e.get("domain") or "—"
    usage[sid] = tok
    by_dom.setdefault(dom, []).append((sid, tok))
# Released IDs from BACKLOG
released = set()
section = ""
for line in (sdd / "BACKLOG.md").read_text(encoding="utf-8", errors="replace").splitlines():
    if line.startswith("## "):
        section = line[3:].strip()
        continue
    if not line.startswith("|"):
        continue
    cols = [c.strip() for c in line.strip("|").split("|")]
    if cols and cols[0].startswith("SDD-") and section == "Released":
        released.add(cols[0])
for sid in sorted(released):
    if sid not in usage:
        print(f"WARN_RELEASED:{sid}")
min_n, factor = 3, 2.0
for dom, items in by_dom.items():
    if len(items) < min_n:
        continue
    avg = sum(t for _, t in items) / len(items)
    if avg <= 0:
        continue
    for sid, tok in items:
        if tok > factor * avg:
            print(f"WARN_OUTLIER:{sid}:{dom}:{tok}:{avg:.0f}")
PY
)" || true)
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      if [[ "$line" == OK_COUNT:* ]]; then
        ok metrics "token-usage.json presente (${line#OK_COUNT:} entradas)"
      elif [[ "$line" == WARN_JSON:* ]]; then
        warn metrics "token-usage.json no es JSON valido"
      elif [[ "$line" == WARN_RELEASED:* ]]; then
        warn metrics "Spec Released ${line#WARN_RELEASED:} sin entrada en token-usage.json"
      elif [[ "$line" == WARN_OUTLIER:* ]]; then
        rest="${line#WARN_OUTLIER:}"
        IFS=':' read -r oid odom otok oavg <<< "$rest"
        warn metrics "Outlier tokens: $oid en dominio $odom ($otok > 2x promedio $oavg; N>=3)"
      fi
    done <<< "$METRICS_OUT"
  else
    warn metrics "Python no disponible para validar token-usage.json"
  fi
fi

echo ""
echo "--- Resumen ---"
for c in "${COMP_ORDER[@]}"; do
  IFS=':' read -r e w m <<< "${COMP_STATS[$c]}"
  [[ "$m" -eq 0 ]] && continue
  if [[ "$e" -gt 0 ]]; then
    status="FAIL"
  elif [[ "$w" -gt 0 ]]; then
    status="WARN"
  else
    status="OK  "
  fi
  printf '[%-12s] %s (%s errores, %s warnings)\n' "$c" "$status" "$e" "$w"
done

echo ""
echo "Total: $ERRORS error(es), $WARNINGS advertencia(s)"
if [[ $ERRORS -gt 0 ]]; then
  echo ""
  echo "Validacion documental SDD FALLIDA. Corrige los ERROR listados arriba (exit 2)."
  exit 2
fi
echo ""
echo "Validacion documental SDD OK."
exit 0
