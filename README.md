<div align="center">

# SDD Kit — Spec-Driven Development

Metodología para desarrollar **con un plan antes de codear**. Pensada para equipos pequeños y desarrollo asistido por agente de IA (Cursor, Claude Code, Codex, Copilot): el agente redacta specs y código; tú apruebas en puntos clave.

[![Repositorio](https://img.shields.io/badge/repo-jcalistop%2Fsdd--kit-24292f?style=flat-square&logo=github)](https://github.com/jcalistop/sdd-kit)
[![Spec-first](https://img.shields.io/badge/enfoque-spec--first-2563eb?style=flat-square)](core/workflow.md)
[![Multi-stack](https://img.shields.io/badge/stacks-Laravel%20%7C%20Django%20%7C%20FastAPI%20%7C%20React-059669?style=flat-square)](profiles/)
[![Agent-ready](https://img.shields.io/badge/agente-Cursor%20%7C%20Claude%20%7C%20Codex%20%7C%20Copilot-7c3aed?style=flat-square)](core/agent-setup.md)

**Repositorio:** https://github.com/jcalistop/sdd-kit

</div>

---

## Navegación rápida

|     | Documento                                       | Para qué                                    |
| --- | ----------------------------------------------- | ------------------------------------------- |
| 🚀  | [Instalación](INSTALL.md)                       | Submodule, copia puntual o solo docs        |
| 📖  | [Conceptos en 5 min](core/concepts.md)          | Primera vez con SDD + glosario              |
| 🗺️  | [Adopción incremental](core/adoption-guide.md)  | Etapas 1–3 en proyectos nuevos o existentes |
| 🤖  | [Configuración del agente](core/agent-setup.md) | Cursor, Claude, Codex, Copilot              |
| 🧭  | [Ciclo SDD](core/workflow.md)                   | Estados, DoR/DoD, releases                  |
| 🛠️  | [CLI](cli/README.md)                            | `validate`, `backlog`, `spec new`           |

---

## ¿Para quién es esto?

| Si eres…                                 | Este kit te ayuda a…                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------- |
| 👤 **Desarrollador principiante en SDD** | Entender el flujo, instalarlo en tu proyecto y no perderte entre archivos |
| ⚙️ **Desarrollador con experiencia**     | Estandarizar specs, backlog, releases y calidad por stack                 |
| 🤝 **Solo dev + agente IA**              | Que el agente siga reglas claras (spec antes de código, checklist en PR)  |

> 💡 No necesitas conocer SDD de antemano. Empieza por **[`core/concepts.md`](core/concepts.md)** (5 minutos, glosario incluido).

---

## La idea en 30 segundos

1. Tienes una **idea o tarea** → la anotas en `BACKLOG.md`.
2. Antes de codear, escribes un **spec** (documento corto): qué quieres, qué no incluye, cómo sabrás que está listo.
3. Cuando el spec está **aprobado**, implementas (o el agente implementa).
4. Al terminar, archivas el spec y registras la **release**.

```mermaid
flowchart LR
    A["💡 Idea"] --> B["📄 Spec"]
    B --> C["💻 Código"]
    C --> D["🔍 Revisión"]
    D --> E["🚀 Publicado"]
```

Más detalle: [`core/concepts.md`](core/concepts.md) · ciclo completo: [`core/workflow.md`](core/workflow.md).

---

## Empieza aquí (desarrollador principiante)

### Paso 1 — Elige tu perfil

El **perfil** adapta tests, deploy y checklist a tu tecnología (o a informes, si no es una app).

| Perfil                                                    | Cuándo usarlo                          |
| --------------------------------------------------------- | -------------------------------------- |
| [`laravel-filament`](profiles/laravel-filament/README.md) | Laravel + panel Filament               |
| [`laravel-voyager`](profiles/laravel-voyager/README.md)   | Laravel + Voyager + Livewire           |
| [`python-fastapi`](profiles/python-fastapi/README.md)     | API con FastAPI                        |
| [`python-django`](profiles/python-django/README.md)       | Django web, admin, DRF/Celery opcional |
| [`react-vite`](profiles/react-vite/README.md)             | Frontend React + Vite                  |
| [`reports-latex-md`](profiles/reports-latex-md/README.md) | Informes Markdown/LaTeX → PDF/DOCX     |

### Paso 2 — Instala en tu proyecto

Desde la raíz de tu repo (con Git):

```powershell
git submodule add https://github.com/jcalistop/sdd-kit.git sdd-kit
.\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App"
```

En Linux/macOS, cambia el perfil y usa `init-sdd.sh`. Guía completa: **[INSTALL.md](INSTALL.md)**.

Por defecto detecta tu agente/IDE e instala las instrucciones correspondientes (`-Agent auto`). Ver **[`core/agent-setup.md`](core/agent-setup.md)**.

### Paso 3 — Completa lo mínimo (día 1)

| Archivo                            | Qué poner                                                      |
| ---------------------------------- | -------------------------------------------------------------- |
| `.github/docs/sdd/sdd.config.yaml` | Nombre del proyecto, ramas, dominios (ej. `auth`, `api`, `ux`) |
| `.github/docs/business/README.md`  | Qué hace el sistema y quién lo usa                             |
| `.github/docs/sdd/BACKLOG.md`      | 3–5 tareas reales en **Discovery** (lo que viene ahora)        |

Checklist detallado: **[`core/adoption-guide.md`](core/adoption-guide.md)** — Etapa 1.

### Paso 4 — Valida que todo esté bien

```powershell
.\sdd-kit\bootstrap\validate-sdd.ps1
```

Si pasa sin errores críticos, la estructura está lista.

### Paso 5 — Tu primer spec con el agente

Con adaptadores instalados, el agente ya tiene las reglas SDD. Si no, pide explícitamente:

> "Sigue sdd-agent-workflow: crea un spec Draft para [tu idea] en el dominio [ux/api/…]."

El agente usa la plantilla del perfil. Revisa el spec; si está bien, aprueba → pasa a **Ready** → implementación.

Ejemplos de calidad por perfil: `profiles/<perfil>/examples/SDD-001-*.md`.

---

## Cómo trabajar con el agente

| Momento           | Tú (humano)                     | Agente                          |
| ----------------- | ------------------------------- | ------------------------------- |
| 💡 Nueva idea     | Describes el problema           | Anota en BACKLOG, propone spec  |
| 📝 Spec en Draft  | **Apruebas o corriges** el spec | Redacta spec, verifica DoR      |
| 🔨 Implementación | Autorizas empezar               | Codea según spec y perfil stack |
| ✅ PR             | **Revisas y mergeas**           | Checklist, tests, evidencia     |

Adaptadores instalados según tu herramienta (ver `sdd.config.yaml` → `agent.targets`). En Cursor: `sdd-core`, `sdd-agent-workflow`, `sdd-stack-<perfil>`.

> 🌱 **Desarrollo sano:** el agente también aplica [`core/healthy-development.md`](core/healthy-development.md) (evitar sobre-ingeniería y antipatrones).

---

## Archivos que usarás seguido

| Archivo                                                    | Para qué                                         |
| ---------------------------------------------------------- | ------------------------------------------------ |
| `BACKLOG.md`                                               | Lista única de tareas y su estado                |
| `specs/<dominio>/SDD-NNN-*.md`                             | Specs activos (una tarea = un spec)              |
| `business/domain-rules.md`                                 | Reglas de negocio que el agente no debe inventar |
| `templates/spec-template.md`                               | Plantilla completa (features técnicas)           |
| `templates/spec-simple-template.md`                        | Plantilla reducida (inicio o tareas simples)     |
| `checklist-pr.md` + `profiles/<perfil>/checklist-stack.md` | Qué revisar antes del merge                      |

---

## CLI (opcional, Python 3.10+)

```powershell
.\sdd-kit\bootstrap\sdd.ps1 validate
.\sdd-kit\bootstrap\sdd.ps1 backlog
.\sdd-kit\bootstrap\sdd.ps1 spec new --domain ux --type feature --title "Mi feature"
```

Detalle: **[cli/README.md](cli/README.md)**.

---

## Cómo está organizado el kit

Tres capas — no hace falta memorizarlas el día 1:

| Capa             | Dónde                                  | Qué es                                          |
| ---------------- | -------------------------------------- | ----------------------------------------------- |
| 🧩 **Core**      | `core/`                                | Ciclo SDD, plantillas, guías (igual para todos) |
| 📦 **Perfil**    | `profiles/<stack>/`                    | Tests, deploy y checklist de tu stack           |
| 📁 **Instancia** | `.github/docs/sdd/` en **tu** proyecto | Tu BACKLOG, specs y releases                    |

```
tu-proyecto/
├── sdd-kit/                    # submodule (el kit)
└── .github/docs/
    ├── sdd/                    # tu instancia SDD
    │   ├── BACKLOG.md
    │   ├── specs/
    │   └── sdd.config.yaml
    └── business/               # contexto de negocio
```

---

## Siguiente lectura (cuando avances)

| Documento                                                    | Cuándo leerlo                               |
| ------------------------------------------------------------ | ------------------------------------------- |
| [`core/concepts.md`](core/concepts.md)                       | Primera vez con SDD                         |
| [`core/adoption-guide.md`](core/adoption-guide.md)           | Proyecto nuevo o existente, etapas 1–3      |
| [`core/workflow.md`](core/workflow.md)                       | Estados, tipos de spec, DoR/DoD             |
| [`core/healthy-development.md`](core/healthy-development.md) | Buenas prácticas y antipatrones             |
| [`core/agent-setup.md`](core/agent-setup.md)                 | Cursor, Claude, Codex, Copilot              |
| [`INSTALL.md`](INSTALL.md)                                   | Otras formas de instalar (copia, solo docs) |

---

## Mantenedores del kit

Planificación y evolución del repositorio (no se copia a proyectos): **[docs/maintainers/](docs/maintainers/)**.

Crear perfiles nuevos: **[`core/templates/profile-template.md`](core/templates/profile-template.md)**.
