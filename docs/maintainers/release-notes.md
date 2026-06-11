# SDD Kit — versión 0.1.0 (pre-release)

> **Estado:** versión de prueba, no es una release estable. Sirvió para validar la idea y recibir los primeros comentarios.

**Fecha de etiqueta:** primera publicación del repositorio  
**Repositorio:** https://github.com/jcalistop/sdd-kit

---

## ¿Qué es esto?

El **SDD Kit** es una guía y un conjunto de plantillas para trabajar **con un plan antes de programar**.

En lugar de ir directo al código, primero escribes un documento corto (un _spec_) que dice qué quieres hacer, qué no incluye y cómo sabrás que terminó bien. Después construyes — a mano o con ayuda de un agente de IA.

La versión **0.1.0** fue la **primera versión pública de prueba**: suficiente para probar el flujo en proyectos Laravel, pero sin muchas de las herramientas que el kit tiene hoy.

---

## ¿Para quién era?

- Personas o equipos pequeños que usan **Laravel** (con Filament o Voyager).
- Quienes quieren ordenar el trabajo con specs y un backlog visible.
- Quienes usan **Cursor** y quieren que el asistente siga reglas claras del proyecto.

No estaba pensada aún para otros lenguajes ni para informes en PDF.

---

## ¿Qué traía esta pre-release?

### Lo esencial (para cualquier proyecto)

- **Guía del método SDD:** cómo pasar de una idea → spec → código → revisión → publicado.
- **Plantillas listas para copiar:** spec, backlog, notas de release, decisiones de arquitectura (ADR).
- **Scripts de instalación** para Windows y Linux/macOS: crean la carpeta de documentación en tu proyecto con un solo comando.

### Adaptado a Laravel

Dos **perfiles** (configuraciones según tu stack):

| Perfil             | Para proyectos con…          |
| ------------------ | ---------------------------- |
| `laravel-filament` | Laravel + panel Filament     |
| `laravel-voyager`  | Laravel + Voyager + Livewire |

Cada perfil incluía checklist de calidad, guía de despliegue y tabla para completar en cada spec.

### Integración con Cursor (opcional)

Al instalar, podías activar reglas para que el asistente de Cursor respete el flujo SDD en cada conversación.

---

## ¿Qué NO traía aún?

Estas piezas llegaron **después** de la 0.1.0 (en versiones posteriores del repositorio):

- Herramienta de línea de comandos (`sdd validate`, `sdd backlog`, etc.)
- Perfiles Python (Django, FastAPI), React o informes LaTeX/Markdown
- Guías para principiantes (`concepts.md`), adopción en proyectos ya existentes o varios agentes (Claude, Copilot…)
- Documentación para quienes mantienen el kit (`docs/maintainers/`)

Si usas el repo **hoy**, verás mucho más que en la etiqueta `v0.1.0`. Esa etiqueta marca un punto histórico, no el estado actual.

---

## Cómo se probaba (en su momento)

1. Añadir el kit al proyecto como submódulo de Git.
2. Ejecutar el script de instalación con el perfil Laravel que correspondiera.
3. Completar la configuración básica y el backlog.
4. Crear el primer spec y seguir el ciclo.

Instrucciones actualizadas: [README.md](https://github.com/jcalistop/sdd-kit/blob/main/README.md) e [INSTALL.md](https://github.com/jcalistop/sdd-kit/blob/main/INSTALL.md).

---

## Limitaciones conocidas de la pre-release

- Solo dos stacks (Laravel Filament y Voyager).
- Instalación pensada sobre todo para **proyectos nuevos**; en proyectos con mucha documentación previa había que tener cuidado al instalar a mano.
- Sin validador automático unificado (solo scripts básicos).
- API y documentación en evolución: se esperaban cambios sin aviso de versión estable.

---

## ¿Qué sigue?

La 0.1.0 cumplió su rol: **probar que la metodología portable tiene sentido**. Las versiones siguientes ampliaron perfiles, CLI, soporte multi-agente y guías de adopción.

Para el estado actual del kit, consulta el [README.md](https://github.com/jcalistop/sdd-kit/blob/main/README.md) de la rama `main`.
