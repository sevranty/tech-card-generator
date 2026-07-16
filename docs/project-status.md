# Project status

Snapshot for TCG#21 from `main@9931a210f5cbd695473203116dcaffbe135c43cd`.

Ledger change: [TCG#21](https://github.com/sevranty/tech-card-generator/issues/21) via [PR#23](https://github.com/sevranty/tech-card-generator/pull/23).

## Identity

| Field | Value |
|---|---|
| PROJECT_ID | `TECH_CARD_GENERATOR` |
| SHORT_ID | `TCG` |
| Project | `tech-card-generator` |
| Skill | `machinery-card-generator` |
| Repository | https://github.com/sevranty/tech-card-generator |
| Tasks | https://github.com/sevranty/tech-card-generator/issues |

## Open and deferred work

| Priority | Work | Owner | Status | Evidence |
|---|---|---|---|---|
| P0 | Publish annotated tag `v2.1.0`, public GitHub Release, ZIP and checksum assets, verify downloaded ZIP SHA-256, install and verify Social preview | [TCG#12](https://github.com/sevranty/tech-card-generator/issues/12) | Blocked by unavailable publication/settings write operations in the connected tool | Release target `168d8342e3d1bbe724a8a06c7823f1e6e22e16ad`; expected SHA-256 `5159ff71763fed5cbfac44d24ea57c500fbfcccde8ff674abe299fccbc5282d2` |
| P1 | Register TCG in the WebFactoryOS project registry and task relations | [WFO#64](https://github.com/sevranty/web-factory-os/issues/64) | Open external task | TCG remains autonomous; relation must not grant cross-repository write access |
| P1 | Add the generic numberless primary-project chat contract for atomic skills | [WFO#65](https://github.com/sevranty/web-factory-os/issues/65) | Open external task | Issues, PRs, `TASK_ID` and relation IDs remain numbered |
| P2 | Run a native installed-skill smoke with real image generation | Deferred | No native installed-skill invocation API in the current execution environment | Deterministic runtime evidence remains in [TCG#10](https://github.com/sevranty/tech-card-generator/issues/10) |

WFO#64 and WFO#65 are orchestration dependencies, not runtime, build, validation or release dependencies of this repository.

## Completed work

| Work | Evidence |
|---|---|
| Canonical skill publication and regression contract | [PR#4](https://github.com/sevranty/tech-card-generator/pull/4) |
| MIT License | [PR#6](https://github.com/sevranty/tech-card-generator/pull/6) |
| Root product README | [PR#9](https://github.com/sevranty/tech-card-generator/pull/9) |
| End-to-end deterministic runtime evidence | [PR#16](https://github.com/sevranty/tech-card-generator/pull/16) |
| Local validation gate | [PR#17](https://github.com/sevranty/tech-card-generator/pull/17) |
| Reproducible v2.1.0 package | [PR#18](https://github.com/sevranty/tech-card-generator/pull/18) |
| Project image and social preview source assets | [PR#19](https://github.com/sevranty/tech-card-generator/pull/19) |
| Local WebFactoryOS ownership and dependency boundary | [PR#22](https://github.com/sevranty/tech-card-generator/pull/22) |

Closed duplicate Issues #13, #14 and #15 are not backlog.

## Boundaries

TCG owns skill implementation, references, examples, validators, tests, assets, packages, versioning and releases. WebFactoryOS owns routing, registry placement, naming rules, task relations and orchestration status.

The following remain protected from project-status maintenance:

- `machinery-card-generator/**`
- `dist/**`
- `assets/**`
- existing tags and release history
- production, deployment, DNS and secrets

See [`webfactoryos-orchestration.md`](webfactoryos-orchestration.md) for the local orchestration contract.
