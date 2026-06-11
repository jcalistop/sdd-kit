#!/usr/bin/env bash
# Valida coherencia documental de una instancia SDD.
# Uso: ./sdd-kit/bootstrap/validate-sdd.sh [.github/docs/sdd]

set -euo pipefail

SDD_PATH="${1:-.github/docs/sdd}"
ERRORS=0
WARNINGS=0

err() { echo "ERROR: $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "WARN:  $1"; WARNINGS=$((WARNINGS + 1)); }
ok() { echo "OK:    $1"; }

if [[ ! -d "$SDD_PATH" ]]; then
  err "No existe el directorio SDD: $SDD_PATH"
  echo "Ejecuta init-sdd o indica la ruta correcta."
  exit 1
fi

BACKLOG="$SDD_PATH/BACKLOG.md"
if [[ ! -f "$BACKLOG" ]]; then
  err "Falta BACKLOG.md en $SDD_PATH"
  exit 1
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
    err "ID $id duplicado en BACKLOG (secciones: ${BACKLOG_IDS[$id]} y $current_section)"
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
      err "ID $id aparece en mas de un archivo"
    fi
    FILE_DUP[$id]=1
  fi
done < <(find "$SDD_PATH/specs" "$SDD_PATH/archive" -name 'SDD-*.md' -print0 2>/dev/null || true)

# Specs activos deben estar en BACKLOG (no Discovery sin ID es ok)
for id in "${!FILE_IDS[@]}"; do
  loc="${FILE_IDS[$id]}"
  if [[ "$loc" == "specs" ]]; then
    if [[ -z "${BACKLOG_IDS[$id]:-}" ]]; then
      err "Spec $id en specs/ sin entrada en BACKLOG.md"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Released" ]]; then
      err "Spec $id en specs/ pero BACKLOG dice Released (debe estar en archive/)"
    elif [[ "${BACKLOG_SECTION[$id]}" == "Discovery" ]]; then
      warn "Spec $id en specs/ pero BACKLOG aun en Discovery (esperado Draft+)"
    else
      ok "Spec activo $id coherente con BACKLOG (${BACKLOG_SECTION[$id]})"
    fi
  fi
  if [[ "$loc" == "archive" ]]; then
    if [[ -z "${BACKLOG_IDS[$id]:-}" ]]; then
      err "Spec archivado $id sin entrada en BACKLOG.md"
    elif [[ "${BACKLOG_SECTION[$id]}" != "Released" ]]; then
      err "Spec $id en archive/ pero BACKLOG no esta en Released (esta en ${BACKLOG_SECTION[$id]})"
    else
      ok "Spec archivado $id coherente con BACKLOG"
    fi
  fi
done

# IDs en BACKLOG Draft..Validating deben tener archivo en specs/
for id in "${!BACKLOG_IDS[@]}"; do
  sec="${BACKLOG_SECTION[$id]}"
  if [[ "$sec" =~ ^(Draft|Ready|In[[:space:]]Build|Validating)$ ]]; then
    if [[ "${FILE_IDS[$id]:-}" != "specs" ]]; then
      err "BACKLOG: $id en $sec pero no hay archivo en specs/"
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
      warn "Proximo ID SDD-$(printf '%03d' $next_num) parece bajo (max usado: SDD-$(printf '%03d' $max_num))"
    else
      ok "Proximo ID disponible coherente (max usado: SDD-$(printf '%03d' $max_num))"
    fi
  fi
fi

# sdd.config.yaml
if [[ ! -f "$SDD_PATH/sdd.config.yaml" ]]; then
  warn "Falta sdd.config.yaml"
else
  ok "sdd.config.yaml presente"
fi

echo ""
echo "Resumen: $ERRORS error(es), $WARNINGS advertencia(s)"
if [[ $ERRORS -gt 0 ]]; then
  exit 1
fi
exit 0
