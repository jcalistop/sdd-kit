# SDD-009 — Posicionar sdd-kit como agent harness en documentacion

---

## Cabecera

| Campo                 | Valor                                    |
| --------------------- | ---------------------------------------- |
| **ID**                | `SDD-009`                                |
| **Dominio**           | `docs`                                   |
| **Tipo**              | `documentation`                          |
| **Fecha**             | 2026-07-15                               |
| **Estado**            | `Released`                               |
| **Version objetivo**  | `v1.3.0`                                 |
| **Owner**             | mantenedor                               |
| **Prioridad**         | `P2`                                     |
| **ADRs relacionados** | `ADR-002`                                |
| **Dependencias**      | SDD-008 (lenguaje guias/sensores — mismo release, sin bloqueo) |

---

## Problema y objetivo

**Problema:**

sdd-kit **ya es un agent harness** — define reglas, skills, verificaciones, orquestacion del ciclo y gates humanos alrededor del agente de coding. Sin embargo, en su documentacion publica (README.md, concepts.md, agent-setup.md) no se posiciona con ese termino. El kit se describe como "metodologia" y "reglas para el agente", lo cual es correcto pero no captura el paradigma emergente que la industria ya reconoce.

En 2026, Harness Engineering es una disciplina con respaldo de Mitchell Hashimoto, Martin Fowler, Thoughtworks, Anthropic y AWS. No usar el termino es perder una oportunidad de posicionamiento y de comunicacion con desarrolladores que ya conocen el concepto.

**Objetivo:**

Incorporar el termino "agent harness" en los documentos publicos clave de sdd-kit, presentando el kit como lo que ya es: un harness metodologico para coding agents. Sin cambiar el producto, solo su presentacion.

---

## Alcance

**Incluye:**

- `README.md`: agregar referencia explicita a "agent harness" en la descripcion del proyecto y en "La idea en 30 segundos"
- `core/concepts.md`: agregar nota "SDD es un agent harness" con enlace al informe de research
- `core/agent-setup.md`: renombrar o agregar seccion que explique que instalar reglas y skills es "configurar el harness SDD"
- `core/healthy-development.md`: nota breve sobre harness engineering como marco conceptual para arquitectura sana
- `docs/releases/README.md`: incluir el termino en contexto de releases del producto

**Excluye explicitamente:**

- Cambios en reglas del agente (eso es SDD-008)
- Cambios en `validate-sdd` (eso es SDD-010)
- Modificar `domain-rules.md` (ya cubierto en SDD-008)
- Modificar perfiles de stack individuales
- Crear nueva documentacion
- Modificar CLI, bootstrap o skills
- Traduccion de paginas completas — solo se agregan terminos donde corresponde

---

## Impacto tecnico

> Perfil: `sdd-kit`. Tabla segun `profiles/sdd-kit/spec-impact.md`.

| Item                        | Impacto                                                                 |
| --------------------------- | ----------------------------------------------------------------------- |
| **core/**                   | Bajo — cambios puntuales en concepts.md, agent-setup.md, healthy-development.md |
| **profiles/**               | No aplica                                                               |
| **bootstrap/**              | No aplica                                                               |
| **cli/**                    | No aplica                                                               |
| **docs/**                   | Bajo — README.md, releases/README.md con terminos adicionales           |
| **BD o schema**             | No aplica                                                               |
| **CI**                      | No aplica — sin cambios en quality gates                                |
| **Seguridad**               | No aplica                                                               |
| **Compatibilidad**          | Alta — solo se agregan terminos; nada se elimina ni se redefine         |
| **Instancias consumidoras** | Transparente — no afecta reglas ni skills del agente                    |

---

## Reglas de negocio

> Aplica `domain-rules.md` principios #1 (core agnostico al stack), #6 (documentacion solo en paths.sdd), #7 (separacion producto/proceso/versiones).

Particularidad de este spec: el termino "agent harness" se aplica al producto (el kit completo), no a un cambio en el proceso SDD ni en las reglas de negocio. Es un cambio de framing, no de sustancia.

---

## Criterios de aceptacion

**Happy path:**

- [x] `README.md` menciona "agent harness" en la descripcion del proyecto (primer parrafo o badges) y en "La idea en 30 segundos"
- [x] `core/concepts.md` incluye nota breve: "SDD es un agent harness" con enlace a `research/2026-07-15-harness-engineering.md`
- [x] `core/agent-setup.md` nombra el proceso de instalacion de reglas/skills como "configurar el harness SDD"
- [x] `core/healthy-development.md` incluye referencia a harness engineering en la introduccion o seccion de arquitectura
- [x] `docs/releases/README.md` referencia "product harness" en el contexto de versionado SemVer
- [x] `python cli/sdd.py validate` sin errores
- [x] Ningun enlace se rompe; todos los cambios son incrementales (no reescriben secciones completas)
- [x] El tono es natural, no forzado — no se repite "harness" en cada parrafo

**Error path:**

- [x] Si el termino genera confusion en feedback de consumidores, se puede revertir por archivo — rollback por archivo documentado
- [x] Si validate-sdd detecta inconsistencia, se corrige antes de merge — correr validate en verify

---

## Diseno tecnico

**Archivos principales:**

| Archivo | Cambio |
| ------- | ------ |
| `README.md` | Agregar "agent harness" en tagline, descripcion y seccion "La idea en 30 segundos" |
| `core/concepts.md` | Agregar nota al final de "Como funciona (resumen)" o seccion nueva breve |
| `core/agent-setup.md` | Agregar nota "esto es configurar el harness del agente" en la introduccion |
| `core/healthy-development.md` | Referencia a harness engineering en la seccion de arquitectura sana |
| `docs/releases/README.md` | Nota sobre releases del producto harness |

**Texto propuesto (orientativo; el agente redacta la version final en implementacion):**

README.md — agregar al primer parrafo o debajo del titulo:

> SDD Kit es un **agent harness** para desarrollo spec-first. Define las reglas, verificaciones y ciclo de trabajo alrededor del agente de IA — el modelo es commodity, el harness es la ventaja competitiva.

core/concepts.md — agregar al final de "Como funciona (resumen)":

> SDD Kit es un **agent harness**: la capa de infraestructura que guia al agente antes de actuar y verifica su trabajo despues. Mas contexto en el [informe de harness engineering](research/2026-07-15-harness-engineering.md).

core/agent-setup.md — modificar introduccion:

> La capa agentica instala el **harness SDD** en el formato de cada IDE. No es un plugin: es la configuracion del entorno de ejecucion del agente (guias, sensores, skills y reglas). La fuente unica de contenido esta en...

---

## Verificacion tecnica

```bash
python cli/sdd.py validate
python -m compileall -q cli/
```

---

## Riesgos y rollback

| Riesgo | Probabilidad | Impacto | Mitigacion |
| ------ | ------------ | ------- | ---------- |
| Termino "harness" confunde a nuevos usuarios que no conocen el concepto | Media | Bajo | El informe de research queda enlazado; el termino es complementario, no reemplaza "metodologia" |
| Sobre-uso del termino en cada parrafo | Baja | Medio | Limitar a 1-2 menciones por documento; priorizar naturalidad sobre densidad |
| Enlace roto al informe de research | Baja | Bajo | `validate-sdd` no cubre enlaces docs; verificacion manual en revision |

Rollback: revertir cada archivo individualmente. Sin dependencias entre cambios.

---

## Notas post-implementacion

- Este spec es el segundo de la serie harness engineering (SDD-008, SDD-009, SDD-010).
- Si el feedback de consumidores es positivo, considerar expandir el framing en el adoption guide.
- El informe de research en `research/2026-07-15-harness-engineering.md` es la referencia tecnica para quien quiera profundizar.
- **Smoke manual (2026-07-15):** exitoso — tono natural en README, concepts, agent-setup, healthy-development y docs/releases.
