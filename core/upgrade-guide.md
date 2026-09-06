# Guía de actualización del kit SDD

> Runbook para proyectos **consumidores** cuando publica una nueva versión del kit (SemVer en `docs/releases/` del repositorio sdd-kit).
>
> **Relacionado:** [`adoption-guide.md`](adoption-guide.md) · [`agent-setup.md`](agent-setup.md) · [`prompt-catalog.md`](prompt-catalog.md) (`upgrade-kit`)

---

## Qué actualizas y qué no

| Capa                   | Ubicación en tu proyecto            | ¿Se sobrescribe sola?                        |
| ---------------------- | ----------------------------------- | -------------------------------------------- |
| **Kit (producto)**     | `sdd-kit/` submodule                | Sí — con `git submodule update`              |
| **Instancia SDD**      | `.github/docs/sdd/`                 | **No** — merge manual o con agente           |
| **Negocio**            | `.github/docs/business/`            | **No**                                       |
| **Adaptadores agente** | `.cursor/rules/`, `CLAUDE.md`, etc. | Parcial — `install-agents.py` con marcadores |

**No confundir:**

- `kit.installed_version` en `sdd.config.yaml` = versión del **kit** que usa el proyecto.
- `.github/docs/sdd/releases/` = releases de **iniciativas SDD** de tu producto (independiente).

---

## Antes de empezar

1. Lee las notas de la versión en `sdd-kit/docs/releases/vX.Y.Z.md` (o [GitHub Releases](https://github.com/jcalistop/sdd-kit/releases)).
2. Revisa `sdd.config.yaml` → `kit.installed_version` (versión que tienes registrada).
3. Confirma que `sdd-kit/` es submodule (`git submodule status`).

Sin submodule (copia puntual): sigue los pasos de merge manual; la comparación automática de versión en `validate-sdd` no aplica.

---

## Flujo recomendado (submodule)

Orden fijo — el agente debe seguirlo con prompt `upgrade-kit`:

```
1. Detectar versión actual (config + submodule)
2. Leer changelog de la versión destino
3. Actualizar submodule a tag o commit
4. Diff sdd-kit/core/ vs .github/docs/sdd/
5. Merge con confirmación humana (nunca --force en instancia)
6. Reinstalar adaptadores si cambió bootstrap/agent-prompts/
7. sdd validate / validate-sdd
8. Actualizar kit.installed_version y UPGRADE-LOG.md
9. Commits separados: submodule + instancia
```

### 1. Detectar versión actual

```bash
# Versión registrada en la instancia
grep -A2 '^kit:' .github/docs/sdd/sdd.config.yaml

# Ref Git del submodule
git -C sdd-kit describe --tags --always
```

### 2. Actualizar submodule

```bash
cd sdd-kit
git fetch origin --tags
git checkout vX.Y.Z   # o: git pull origin main
cd ..
git add sdd-kit
```

### 3. Portar cambios a la instancia

Comparar (ejemplo):

```bash
diff -rq sdd-kit/core .github/docs/sdd --exclude=prompts --exclude=profiles
```

**Reglas de merge:**

- Archivos **nuevos** en `core/` → copiar si no existen en instancia.
- Archivos **modificados** en ambos → mostrar diff; **pedir confirmación** antes de sobrescribir.
- `BACKLOG.md`, `specs/`, `archive/` de tu proyecto → **nunca** reemplazar desde el kit.
- `prompts/` y `prompt-catalog.md` → copiar solo entradas o fichas faltantes.

### 4. Reinstalar adaptadores y skills

Si cambió `bootstrap/agent-prompts/` o `bootstrap/agent-skills/`:

```bash
python sdd-kit/bootstrap/install-agents.py install \
  --profile <PERFIL> \
  --agent auto \
  --sdd-path .github/docs/sdd \
  --kit-path sdd-kit
```

Ver [`agent-setup.md`](agent-setup.md).

### 5. Validar

```bash
python sdd-kit/cli/sdd.py validate
```

- **ERROR** → corregir antes de cerrar el upgrade.
- **WARN** por `kit.installed_version` ≠ ref Git → actualizar config y log tras completar el merge.

### 6. Registrar trazabilidad

En `.github/docs/sdd/UPGRADE-LOG.md` añade una fila:

| Fecha | Desde | Hacia | Archivos mergeados | Validación | Notas |
| ----- | ----- | ----- | ------------------ | ---------- | ----- |

Actualiza `sdd.config.yaml`:

```yaml
kit:
    installed_version: "vX.Y.Z"
    installed_at: "YYYY-MM-DD"
```

**Si el humano rechaza un merge:** documenta archivos pendientes en Notas; **no** actualices `installed_version` hasta completar o acordar deuda.

### 7. Commits

```bash
git commit -m "chore: actualiza sdd-kit a vX.Y.Z" -- sdd-kit
git commit -m "chore(sdd): portar cambios kit vX.Y.Z a instancia" -- .github/docs/sdd .cursor
```

---

## Tras v1.3.0+ — checklist de consumo

Tras actualizar a **v1.3.0 o superior**, el bump de submodule **no basta**. Debes completar el flujo de esta guía (pasos 4–8), en especial **reinstalar adaptadores** si cambió `bootstrap/agent-prompts/` o `bootstrap/agent-skills/`.

### Qué debe quedar instalado / verificable

| Entregable | Cómo verificar |
| ---------- | -------------- |
| **Safe-git** (SDD-007) | Existe `.cursor/rules/sdd-safe-git.mdc` con `alwaysApply: true`. Preámbulos Claude/Codex/Copilot mencionan safe-git o `core/safe-git-contract.md`. **No** duplica reglas de migraciones BD de instancia (`safe-migrations`, etc.). |
| **Two-zone / reglas** | Reinstall regenera reglas Cursor en orden stable→volatile (`cacheZone` en manifest). |
| **Plantilla compacta** | Disponible en el kit: `sdd-kit/core/templates/spec-compact-template.md` (no requiere copiar a instancia salvo que uses plantillas locales). |
| **validate-sdd por componente** (SDD-010) | Salida con prefijos `[backlog]`, `[specs]`, `[config]`, etc. |

### Comando de reinstall (Cursor)

```bash
python sdd-kit/bootstrap/install-agents.py install \
  --profile <PERFIL> \
  --agent cursor \
  --sdd-path .github/docs/sdd \
  --kit-path sdd-kit
```

Si solo hiciste checkout del tag y **falta** `sdd-safe-git.mdc`, vuelve a ejecutar el reinstall y el checklist de la skill `sdd-upgrade-kit` (`reference.md`).

### v1.3.1 — Descartado en archive

Si tras el upgrade `validate-sdd` falla por specs en `specs/` con BACKLOG Descartado (o cabecera `Deprecated`/`Descartado`):

1. Renombra cabecera a **`Descartado`** (no uses `Deprecated`).
2. `git mv` el `.md` a `archive/<YYYY>/<dominio>/` — **sin stub** en `specs/`.
3. Asegura la fila en BACKLOG «Descartado / en pausa» con enlace al archive.
4. Vuelve a ejecutar `validate`.

Detalle: `docs/releases/v1.3.1.md`.

### v1.3.2 — Retiro de metering de tokens y cost-governance (SDD-016)

Breaking change menor respecto a v1.3.1 (publicado como patch `v1.3.2`):

- Skill `sdd-cost-governance` **retirada** (ya no se instala). Borra copias huérfanas en `.cursor/skills/sdd-cost-governance/` al reinstalar.
- Subcomando `sdd metrics tokens` **retirado**. `sdd metrics` sigue midiendo salud del proceso (estados, stagnant).
- No se usa `paths.sdd/metrics/token-usage.json`.
- Se conservan two-zone, grafo de dependencias, plantilla compacta y umbral «¿necesita spec?» (A/B/C/F de SDD-012 salvo la skill D).

### v1.4.0 — Suite pytest CLI (SDD-017)

Minor del repo productor: suite `pytest` en `cli/tests/`, step en CI y `requirements-dev.txt`.

- **Consumidores:** sin cambio de API ni de adaptadores. Bump submodule + `kit.installed_version` basta.
- **Mantenedores del kit:** `pip install -r requirements-dev.txt` y `python -m pytest cli/tests -q` (también en CI).

Detalle: `docs/releases/v1.4.0.md`.

### v1.4.1 — Higiene agentica: retirar residual `sdd-core.mdc` (SDD-018)

Patch de higiene: el kit ya no versiona ni documenta `.cursor/rules/sdd-core.mdc` (fusionado en `sdd-agent-workflow` desde v1.2.2 / SDD-006).

- Si tras el upgrade queda `.cursor/rules/sdd-core.mdc` en tu proyecto, **bórralo** a mano; `install-agents` / `sync-cursor-rules` no lo regeneran.
- Actualiza referencias en docs locales que aún listen `sdd-core` como regla vigente.

Detalle: `docs/releases/v1.4.1.md` (al cerrar campaña).

---

## Prompt para el agente

```bash
python sdd-kit/cli/sdd.py prompt show upgrade-kit --full
```

Sustituye `<VERSION>` por la versión destino (ej. `v1.1.0`).

---

## Referencias

| Documento                          | Uso                               |
| ---------------------------------- | --------------------------------- |
| [`INSTALL.md`](../INSTALL.md)      | Instalación y submodule           |
| [`UPGRADE-LOG.md`](UPGRADE-LOG.md) | Log de esta instancia (si existe) |
| `sdd-kit/docs/releases/`           | Changelog del producto kit        |
