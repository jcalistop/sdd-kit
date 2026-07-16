# SDD-010 — Observabilidad por componente en validate-sdd

---

## Cabecera

| Campo                 | Valor                           |
| --------------------- | ------------------------------- |
| **ID**                | `SDD-010`                       |
| **Dominio**           | `cli`                           |
| **Tipo**              | `feature`                       |
| **Fecha**             | 2026-07-15                      |
| **Estado**            | `Draft`                         |
| **Version objetivo**  | `v1.3.0`                        |
| **Owner**             | mantenedor                      |
| **Prioridad**         | `P2`                             |
| **ADRs relacionados** | —                               |
| **Dependencias**      | — (independiente de SDD-008 y SDD-009) |

---

## Problema y objetivo

**Problema:**

`validate-sdd` (v1.2.2) emite mensajes genericos de aprobacion/error:

```
OK:    Spec activo SDD-008 coherente con BACKLOG (Draft)
ERROR: Spec SDD-005 en specs/ pero BACKLOG dice Released
```

El mantenedor ve que algo fallo, pero no sabe **que componente** esta roto. Si falla una regla de dominio, un archivo de perfil, o un spec activo, el mensaje no lo distingue. Esto impide diagnosticar rapidamente donde intervenir.

La disciplina harness engineering (AHE, NexAU 2026) propone **observabilidad por componente**: descomponer el sistema en partes ortogonales, cada una trackeable y auditable. `validate-sdd` ya valida varios componentes (BACKLOG, specs, config, archivos de perfil, manifest), pero los reporta como lista plana sin agruparlos ni nombrar el componente.

**Objetivo:**

Refactorizar la salida de `validate-sdd` para agrupar resultados por **componente**. Cada linea de salida incluye el componente al que pertenece. El resumen final desglosa errores y advertencias por componente.

---

## Alcance

**Incluye:**

- `bootstrap/validate-sdd.ps1`: prefijar cada linea de salida con `[componente]`, agrupar visualmente por componente, resumen final con desglose `componente: E errores, W advertencias`
- `bootstrap/validate-sdd.sh`: mismos cambios para bash (si existe; verificar)
- Componentes a identificar:
  - `[backlog]` — coherencia del BACKLOG (IDs duplicados, secciones, proximo ID)
  - `[specs]` — coherencia specs activos vs BACKLOG y archive
  - `[config]` — sdd.config.yaml presente y valido
  - `[agent]` — manifest de skills, targets de agente
  - `[kit-version]` — version del kit en disco vs config
  - `[docs]` — coherencia de documentacion cross-capa
- Agregar separador visual entre componentes (linea de guiones o cabecera de seccion)
- Preservar codigos de salida existentes (0=OK, 1=FATAL, 2=ERROR)
- Preservar salida compatible con consumo programatico (no cambiar formato de linea para grep/CI)

**Excluye explicitamente:**

- Agregar nuevos checks de validacion — solo se reorganiza la salida existente
- Cambiar `cli/sdd.py` (el wrapper Python delega en validate-sdd.ps1/.sh)
- Modificar `cli/lib/` (backlog parser, paths, etc.)
- Agregar metricas de trayectoria o historial de fallos (SDD futuro)
- Formato JSON/YAML estructurado de salida (SDD futuro si hay demanda)
- Validacion de enlaces rotos en documentacion

---

## Impacto tecnico

> Perfil: `sdd-kit`.

| Pregunta | Respuesta |
| -------- | --------- |
| Afecta `core/`? | No aplica — cambio en bootstrap |
| Afecta `profiles/<stack>/`? | No aplica |
| Afecta `bootstrap/`? | Si — validate-sdd.ps1 y validate-sdd.sh |
| Afecta `cli/`? | No — el wrapper Python delega sin cambios |
| Afecta `.github/workflows/` o reglas Cursor? | No — CI usa `cli/sdd.py validate` que delega sin cambios |
| Requiere actualizar `README.md` o `INSTALL.md`? | No aplica — cambio interno de herramienta |
| Afecta instancia SDD? | Si — el output de `validate-sdd` cambia para consumidores |
| Afecta reglas en `domain-rules.md`? | No aplica |
| Introduce decision arquitectonica transversal? | No |

---

## Reglas de negocio

> Aplica `domain-rules.md` principios #1 (core agnostico al stack — validate-sdd es bootstrap, no core), #4 (agente ejecuta; humano aprueba — validate es sensor computacional).

Particularidad de este spec: la observabilidad por componente no modifica la logica de validacion, solo como se presenta el resultado. Es un cambio de **output format** con beneficio diagnostico directo para el mantenedor.

---

## Criterios de aceptacion

**Happy path:**

- [ ] Cada linea de salida de `validate-sdd` incluye prefijo `[componente]` (ej. `[backlog]`, `[specs]`, `[config]`)
- [ ] Los resultados se agrupan por componente con separador visual (ej. `--- [backlog] ---`)
- [ ] Resumen final desglosa: `[backlog] 0E/1W | [specs] 1E/0W | [config] OK | ...`
- [ ] Codigos de salida preservados: 0 cuando 0 errores (advertencias no cambian exit code)
- [ ] `python cli/sdd.py validate` produce el nuevo formato (el wrapper Python delega sin cambios)
- [ ] El script bash (`validate-sdd.sh`) recibe los mismos cambios si existe; si no, se documenta como deuda
- [ ] CI existente no se rompe (`.github/workflows/ci.yml`)
- [ ] Salida existente de `validate-sdd` en consumidores sigue siendo parseable para grep simple

**Error path:**

- [ ] Si un componente no tiene checks (vacio), no se muestra separador — no genera ruido
- [ ] Si el script falla en inicializacion (FATAL), el formato por componente no se aplica (no hay nada que agrupar)

---

## Diseno tecnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `bootstrap/validate-sdd.ps1` | Refactorizar salida: prefijos `[componente]`, agrupacion, resumen desglosado |
| `bootstrap/validate-sdd.sh` | Mismos cambios si existe; si no existe, nota en deuda tecnica |

**Formato propuesto (ejemplo):**

```
=== Validacion SDD (.github/docs/sdd) ===

--- [backlog] ---
[backlog] OK:    Proximo ID disponible coherente (max usado: SDD-009)

--- [specs] ---
[specs] OK:    Spec activo SDD-008 coherente con BACKLOG (Draft)
[specs] OK:    Spec activo SDD-009 coherente con BACKLOG (Draft)
[specs] OK:    Spec activo SDD-007 coherente con BACKLOG (Draft)
[specs] OK:    Spec archivado SDD-001 coherente con BACKLOG

--- [config] ---
[config] OK:    sdd.config.yaml presente

--- [agent] ---
[agent] WARN:  agent.targets incluye cursor pero falta .cursor/skills/.sdd-kit-manifest.json

--- [kit-version] ---
[kit-version] OK:    kit.installed_version coherente con kit en disco (v1.2.2)

--- [docs] ---

--- Resumen ---
[backlog]     OK   (0 errores, 0 warnings)
[specs]       OK   (0 errores, 0 warnings)
[config]      OK   (0 errores, 0 warnings)
[agent]       WARN (0 errores, 1 warning)
[kit-version] OK   (0 errores, 0 warnings)
[docs]        OK   (0 errores, 0 warnings)

Total: 0 error(es), 1 advertencia(s)
Validacion documental SDD OK.
```

**Logica de implementacion (validate-sdd.ps1):**

1. Al inicio del script, inicializar un array/hashtable para acumular resultados por componente
2. Cada llamada a `Write-Ok`/`Write-Err`/`Write-Warn` incluye el parametro `-Component`
3. Al imprimir, prefijar `[$component]` y acumular contadores en `$componentResults`
4. Entre componentes distintos, insertar separador `--- [$component] ---`
5. Al final, iterar `$componentResults` para imprimir resumen desglosado

**Compatibilidad con grep/CI:**

El prefijo `[componente]` se agrega al inicio de cada linea, despues del nivel (OK/ERROR/WARN). El formato es:

```
[componente] NIVEL: mensaje
```

Un grep simple como `grep ERROR` o `grep WARN` sigue funcionando sin cambios. La agrupacion visual (separadores) no interfiere con el parseo linea a linea.

---

## Verificacion tecnica

```bash
# Validacion del propio kit
python cli/sdd.py validate

# Verificar que el script PowerShell no tiene errores de sintaxis
powershell -NoProfile -Command "Get-Command .\bootstrap\validate-sdd.ps1"

# Verificar salida con componentes
.\bootstrap\validate-sdd.ps1 -SddPath ".github/docs/sdd"
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigacion |
| ------ | ------------ | ------- | ---------- |
| Cambio de formato rompe CI que parsea la salida | Baja | Medio | El prefijo `[componente]` es aditivo; grep por `ERROR` o `WARN` no se rompe |
| Script bash no existe o difiere del ps1 | Media | Bajo | Verificar existencia primero; si falta, documentar como deuda |
| Salida mas verbosa dificulta lectura rapida | Baja | Bajo | La agrupacion reduce ruido visual; leer por componente es mas rapido que lista plana |
| Componentes vacios generan ruido | Baja | Bajo | Si un componente no tiene checks, no se imprime separador |

Rollback: revertir `validate-sdd.ps1` y `validate-sdd.sh` a version anterior. Sin dependencias con otros archivos.

---

## Notas post-implementacion

- Este spec es el tercero de la serie harness engineering (SDD-008, SDD-009, SDD-010).
- Inspirado en AHE (NexAU): "component observability — harness decomposed into seven orthogonal, file-level components, each git-tracked so every edit is auditable and revertible".
- Paso siguiente natural: capturar historial de fallos por componente para mejora continua (evaluate -> analyze -> improve). Evaluar en spec futuro si hay demanda.
