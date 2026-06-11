## Resumen

<!-- 2–4 líneas: qué cambia y por qué -->

## Tipo de cambio

- [ ] Documentación
- [ ] Perfil de stack (`profiles/`)
- [ ] Core / workflow (`core/`)
- [ ] Bootstrap / agentes (`bootstrap/`)
- [ ] CLI (`cli/`)
- [ ] Mantenedores (`docs/maintainers/`)
- [ ] Otro: \_

## Checklist

- [ ] El cambio es acotado y documentado donde corresponde
- [ ] No rompe la regla _core agnóstico / perfiles autocontenidos_ (o está justificado)
- [ ] Si es perfil nuevo: sigue [profile-template.md](../core/templates/profile-template.md)
- [ ] `python -m compileall cli/` pasa (si toqué Python)
- [ ] Breaking change para consumidores del submodule: **Sí / No** — si sí, describir migración

## Issue relacionado

Closes #<!-- número o "ninguno" -->
