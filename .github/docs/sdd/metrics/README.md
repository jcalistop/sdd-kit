# Métricas de tokens (SDD)

> Estimaciones **heurísticas** — no son facturación exacta ni counts del IDE.
> Comando: `python cli/sdd.py metrics tokens [--summary|--all|SDD-NNN] [--format json|table]`

## Archivo `token-usage.json`

Schema (versión 1):

```json
{
  "version": 1,
  "entries": [
    {
      "spec_id": "SDD-006",
      "domain": "bootstrap",
      "date": "2026-07-14",
      "phases": {
        "draft": { "turns": 5, "tool_calls": 10, "estimated_tokens": 8000 },
        "build": { "turns": 20, "tool_calls": 40, "estimated_tokens": 35000 },
        "verify": { "turns": 3, "tool_calls": 5, "estimated_tokens": 5000 }
      },
      "total_estimated_tokens": 48000,
      "estimated_input_tokens": 25872,
      "estimated_output_tokens": 11712,
      "verify_passed_first_attempt": true,
      "domain_rules_violations": 0,
      "confidence": "medium"
    }
  ]
}
```

| Campo | Descripción |
|-------|-------------|
| `confidence` | `low` (solo heurística de tamaño) · `medium` (registro manual/sesión) · `high` (log rico; raro sin telemetría IDE) |
| `phases.*.estimated_tokens` | Tokens estimados por fase SDD |
| `verify_passed_first_attempt` | Sensor: verify al primer intento |

## Heurística sin registro

Si no hay entrada para un `SDD-NNN`, la CLI estima: `(chars del spec / 4) × 15` con `confidence: low`.

## validate-sdd

- **WARN** (no ERROR) si specs en Released no tienen entrada en `token-usage.json`
- **WARN** si un spec registrado supera **2×** el promedio de su dominio (mínimo **N=3** muestras en ese dominio)
- Si falta el directorio `metrics/` → WARN, no ERROR

## Relación con governance

Skill `sdd-cost-governance` pide registrar costo al cerrar specs. Esta carpeta es el almacén; la CLI lee y reporta.
