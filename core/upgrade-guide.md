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

### 4. Reinstalar adaptadores

Si cambió `bootstrap/agent-prompts/`:

```bash
python sdd-kit/bootstrap/install-agents.py install \
  --profile <PERFIL> \
  --agent auto \
  --sdd-path .github/docs/sdd
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
