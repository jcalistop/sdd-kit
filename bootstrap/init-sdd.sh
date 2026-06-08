#!/usr/bin/env bash
# Inicializa SDD en un proyecto. Uso:
#   ./sdd-kit/bootstrap/init-sdd.sh --profile laravel-filament --project "Mi App"

set -euo pipefail

PROFILE="laravel-filament"
PROJECT_NAME="Mi Proyecto"
KIT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_ROOT="$(pwd)"
SDD_PATH=".github/docs/sdd"
BUSINESS_PATH=".github/docs/business"
INSTALL_CURSOR=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --project) PROJECT_NAME="$2"; shift 2 ;;
    --sdd-path) SDD_PATH="$2"; shift 2 ;;
    --cursor) INSTALL_CURSOR=true; shift ;;
    -h|--help)
      echo "Uso: init-sdd.sh [--profile NAME] [--project NAME] [--sdd-path PATH] [--cursor]"
      exit 0
      ;;
    *) echo "Opción desconocida: $1"; exit 1 ;;
  esac
done

PROFILE_DIR="$KIT_DIR/profiles/$PROFILE"
if [[ ! -d "$PROFILE_DIR" ]]; then
  echo "Perfil no encontrado: $PROFILE"
  exit 1
fi

FULL_SDD="$TARGET_ROOT/$SDD_PATH"
mkdir -p "$FULL_SDD"/{specs,archive,adr,releases,templates}
mkdir -p "$TARGET_ROOT/$BUSINESS_PATH"

# Core docs (copia inicial; proyectos pueden enlazar al kit vía submodule)
for f in workflow.md operations.md branching.md checklist-pr.md README.md; do
  cp "$KIT_DIR/core/$f" "$FULL_SDD/$f"
done

cp -r "$KIT_DIR/core/releases/"* "$FULL_SDD/releases/"
cp "$KIT_DIR/core/adr/README.md" "$FULL_SDD/adr/README.md"
cp "$KIT_DIR/core/templates/"* "$FULL_SDD/templates/"

# Perfil stack: checklist y referencias
mkdir -p "$FULL_SDD/profiles"
cp -r "$PROFILE_DIR" "$FULL_SDD/profiles/"

# Config
cp "$KIT_DIR/sdd.config.example.yaml" "$FULL_SDD/sdd.config.yaml"
if command -v sed &>/dev/null; then
  sed -i.bak "s/Mi Proyecto/$PROJECT_NAME/" "$FULL_SDD/sdd.config.yaml" && rm -f "$FULL_SDD/sdd.config.yaml.bak"
  sed -i.bak "s/profile: laravel-filament/profile: $PROFILE/" "$FULL_SDD/sdd.config.yaml" && rm -f "$FULL_SDD/sdd.config.yaml.bak"
fi

# BACKLOG
sed "s/{{PROJECT_NAME}}/$PROJECT_NAME/" "$KIT_DIR/core/templates/BACKLOG-template.md" > "$FULL_SDD/BACKLOG.md"

# PROJECT.md
cat > "$FULL_SDD/PROJECT.md" <<EOF
# SDD — $PROJECT_NAME

Instancia SDD generada con **sdd-kit** (perfil \`$PROFILE\`).

| Capa | Ubicación |
|------|-----------|
| Kit (core + perfiles) | \`sdd-kit/\` en repo o submodule |
| Instancia | Este directorio |

**Config:** [sdd.config.yaml](sdd.config.yaml)

**Checklist PR:** [checklist-pr.md](checklist-pr.md) + [profiles/$PROFILE/checklist-stack.md](profiles/$PROFILE/checklist-stack.md)
EOF

# Business stub
if [[ ! -f "$TARGET_ROOT/$BUSINESS_PATH/README.md" ]]; then
  cat > "$TARGET_ROOT/$BUSINESS_PATH/README.md" <<EOF
# Negocio — $PROJECT_NAME

Contexto de producto (qué hace el sistema). Separado de la metodología SDD en \`$SDD_PATH\`.

Completar: visión, glosario, módulos, roles, flujos, modelo de datos.
EOF
fi

# PR template (opcional)
if [[ ! -f "$TARGET_ROOT/.github/PULL_REQUEST_TEMPLATE.md" ]]; then
  mkdir -p "$TARGET_ROOT/.github"
  cp "$KIT_DIR/core/templates/pr-template.md" "$TARGET_ROOT/.github/PULL_REQUEST_TEMPLATE.md"
fi

# Cursor rules
if $INSTALL_CURSOR; then
  mkdir -p "$TARGET_ROOT/.cursor/rules"
  cp "$KIT_DIR/bootstrap/cursor-rules/sdd-core.mdc" "$TARGET_ROOT/.cursor/rules/sdd-core.mdc"
  if [[ -f "$KIT_DIR/bootstrap/cursor-rules/sdd-stack-${PROFILE}.mdc" ]]; then
    cp "$KIT_DIR/bootstrap/cursor-rules/sdd-stack-${PROFILE}.mdc" "$TARGET_ROOT/.cursor/rules/"
  fi
fi

echo "SDD inicializado en $FULL_SDD (perfil: $PROFILE)"
echo "Siguiente: revisar sdd.config.yaml, dominios y crear SDD-001."
