#!/usr/bin/env bash
# Valida coherencia documental de una instancia SDD.
# Uso: ./sdd-kit/bootstrap/validate-sdd.sh [.github/docs/sdd]
# Codigos de salida: 0=OK, 1=fallo del script/entorno (FATAL), 2=incoherencias documentales (ERROR)
# Salida por componente (SDD-010): [backlog] [specs] [config] [agent] [kit-version] [docs]

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

# IDs en archivos specs/ y archive/
declare -A FILE_IDS
declare -A FILE_PATHS
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
    FILE_PATHS["$id"]="$f"
    if [[ -n "${FILE_DUP[$id]:-}" ]]; then
      err specs "ID $id aparece en mas de un archivo"
    fi
    FILE_DUP[$id]=1
  fi
done < <(find "$SDD_PATH/specs" "$SDD_PATH/archive" -name 'SDD-*.md' -print0 2>/dev/null || true)

header_estado() {
  local f="$1"
  local line
  while IFS= read -r line; do
    if [[ "$line" == *"**Estado**"* ]]; then
      echo "$line" | cut -d'|' -f3 | sed 's/`//g;s/^[[:space:]]*//;s/[[:space:]]*$//'
      return 0
    fi
  done < <(head -n 40 "$f" 2>/dev/null || true)
  return 0
}

# Specs activos deben estar en BACKLOG
for id in "${!FILE_IDS[@]}"; do
  loc="${FILE_IDS[$id]}"
  estado=""
  if [[ -n "${FILE_PATHS[$id]:-}" ]]; then
    estado=$(header_estado "${FILE_PATHS[$id]}")
  fi
  if [[ "$loc" == "specs" ]]; then
    if [[ -z "${BACKLOG_IDS[$id]:-}" ]]; then
      err specs "Spec $id en specs/ sin entrada en BACKLOG.md"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Released" ]]; then
      err specs "Spec $id en specs/ pero BACKLOG dice Released (debe estar en archive/)"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Descartado" ]]; then
      err specs "Spec $id en specs/ pero BACKLOG dice Descartado (debe estar en archive/)"
    elif [[ "$estado" =~ ^(Released|Descartado) ]]; then
      err specs "Spec $id en specs/ con cabecera Estado=$estado (terminales solo en archive/)"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Discovery" ]]; then
      warn specs "Spec $id en specs/ pero BACKLOG aun en Discovery (esperado Draft+)"
    else
      ok specs "Spec activo $id coherente con BACKLOG (${BACKLOG_SECTION[$id]})"
    fi
  fi
  if [[ "$loc" == "archive" ]]; then
    if [[ -z "${BACKLOG_IDS[$id]:-}" ]]; then
      err specs "Spec archivado $id sin entrada en BACKLOG.md"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Released" || "${BACKLOG_SECTION[$id]}" == "Descartado" ]]; then
      ok specs "Spec archivado $id coherente con BACKLOG (${BACKLOG_SECTION[$id]})"
    else
      err specs "Spec $id en archive/ pero BACKLOG no esta en Released ni Descartado (esta en ${BACKLOG_SECTION[$id]})"
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
