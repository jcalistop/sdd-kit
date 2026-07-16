---
name: sdd-cost-governance
description: Define límites de gasto de tokens, patrones de stop y logging de costo por spec. El agente DEBE leer esta skill al inicio de cada sesión SDD. Es el circuit breaker del harness.
---

# SDD Cost Governance

> **Circuit breaker del harness.** No es opcional. Leer al inicio de cada sesión SDD.

---

## Límites de sesión

| Límite | Valor por defecto | Acción al alcanzar |
|--------|------------------|-------------------|
| Turnos máximos por fase | 15 | Pausar y pedir aprobación humana |
| Turnos máximos totales | 50 | Terminar sesión; reportar estado |
| Iteraciones de verify fallidas consecutivas | 3 | **STOP.** No seguir. Reportar criterios fallidos al humano. |
| Tool calls idénticas consecutivas | 3 | Circuit breaker: cambiar approach o pedir ayuda |
| Tiempo máximo de sesión | 45 min | Pausar y resumir progreso |

---

## Anti-patrones de gasto — STOP inmediato

Si detectas alguno de estos patrones, **detente y pide instrucciones al humano.** No sigas iterando:

1. **Loop de "generar → test falla → mismo error → regenerar"** sin cambiar approach. Si el test falla 3 veces con el mismo error, el approach está mal.
2. **Leer el mismo archivo 5+ veces** sin modificarlo entre lecturas. Carga el archivo una vez; confía en el contexto.
3. **Re-escribir specs ya aprobadas en Ready.** Un spec en Ready está congelado. Solo se modifica con aprobación humana explícita.
4. **Ejecutar tests sin cambiar código** entre ejecuciones. Si nada cambió, el resultado no cambiará.
5. **Cargar specs de otras features no relacionadas.** Usa el [grafo de dependencias]({{SDD_PATH}}/workflow.md) para saber qué leer.
6. **Debug por fuerza bruta** — probar cambios aleatorios hasta que "funcione". Si no entiendes la causa raíz, pide ayuda.

---

## Registro de costo por spec

Al finalizar cada spec (transición a Released), estimar y registrar:

```
SDD-NNN | Fase más cara | Turns est. | Verify 1er intento | Notas
```

El objetivo es construir una base de datos de costo por spec para detectar outliers y patrones de mejora.

**Métrica clave:** si un spec consume >2× el promedio de specs del mismo dominio, requiere análisis post-mortem.

---

## Fundamento

- El spec es ~2.4% de los tokens. La revisión iterativa es ~59.4%. Fuente: Tokenomics paper (arXiv:2601.14470, 2026).
- Un harness con governance reduce tokens 38%, costo 41%, tiempo 44%. Fuente: Harness Effect paper (arXiv:2607.06906, 2026).
- KV-cache hit rate < 90% implica pagar hasta 10× más por input tokens. Fuente: Manus data (Sah, 2026).
- Todos los desastres de costo documentados fueron fallos de governance, no de metodología. Fuente: [research/2026-07-15-token-economics-sdd-harness.md]({{SDD_PATH}}/research/2026-07-15-token-economics-sdd-harness.md).

---

## Recursos

- [Grafo de dependencias SDD]({{SDD_PATH}}/workflow.md) — contexto mínimo por skill
- [Investigación: Token economics]({{SDD_PATH}}/research/2026-07-15-token-economics-sdd-harness.md)
- [Workflow SDD]({{SDD_PATH}}/workflow.md) — thresholds de decisión SDD vs no-SDD
