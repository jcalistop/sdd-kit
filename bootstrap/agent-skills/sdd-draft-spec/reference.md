# SDD Draft — Referencia

**Fuentes canónicas (no duplicar aquí):**

- DoR, antipatrones → `.cursor/rules/sdd-workflow-reference.mdc`
- Prompt kit → `python {{KIT_PATH}}/cli/sdd.py prompt show discovery-to-draft --full`

---

## Preguntas útiles

- ¿Qué problema resuelve hoy que no se resuelve?
- ¿Quién usa esto (rol/panel)?
- ¿Qué queda **fuera** de alcance?
- ¿Depende de algún SDD en curso?
- ¿Versión objetivo según campaña abierta en BACKLOG?
- ¿Hace falta «Congelado para implementación» (decisión única, API, tests, lista + N)? Si sí: ¿cuál es N y la lista?

---

## Formato fila BACKLOG (Draft)

```markdown
| SDD-NNN | dominio | Título breve | **vX.Y.Z** | [spec](specs/dominio/SDD-NNN-slug.md) |
```

---

## Validación documental

```bash
python {{KIT_PATH}}/cli/sdd.py validate
```
