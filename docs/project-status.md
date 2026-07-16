# Project status

Snapshot for TCG#21 from `main@0fd8b51783b4ca21c1f28c54abada3834d621eaf`.

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
| P0 | Publish annotated tag `v2.1.0`, public GitHub Release, ZIP and checksum assets, verify the downloaded ZIP SHA-256, install and verify Social preview | [TCG#12](https://github.com/sevranty/tech-card-generator/issues/12) | Open - publication/settings write operations are required | Release target `168d8342e3d1bbe724a8a06c7823f1e6e22e16ad`; expected SHA-256 `5159ff71763fed5cbfac44d24ea57c500fbfcccde8ff674abe299fccbc5282d2` |
| P1 | Register TCG in the WebFactoryOS project registry and add the task relation to TCG#20 | [WFO#64](https://github.com/sevranty/web-factory-os/issues/64) | Open external orchestration task | The relation must keep `grants_write_access=false`; WFO is not a TCG runtime, build, validation or release dependency |
| P2 | Run a native installed-skill smoke with real image generation | Deferred | Requires an environment with native installed-skill invocation and image generation | Deterministic runtime evidence remains valid in [TCG#10](https://github.com/sevranty/tech-card-generator/issues/10) |

TCG#12 is the only open work item owned by this repository. WFO#64 is tracked in WebFactoryOS and does not block local use, validation or packaging.

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
| Numberless primary-project chat naming contract | [WFO#65 / PR#77](https://github.com/sevranty/web-factory-os/issues/65) |

Closed duplicate Issues #13, #14 and #15 are not backlog.

PR#23, PR#24 and PR#25 were overlapping TCG#21 status implementations. TCG#21 normalizes them into this single ledger.

## Boundaries

TCG owns skill implementation, references, examples, validators, tests, assets, packages, versioning and releases.

WebFactoryOS owns routing, registry placement, naming rules, task relations and orchestration status. A relation does not grant cross-repository write access.

Protected from project-status maintenance:

- `machinery-card-generator/**`
- `dist/**`
- `assets/**`
- `docs/webfactoryos-orchestration.md`
- existing tags and release history
- production, deployment, DNS and secrets

See [`webfactoryos-orchestration.md`](webfactoryos-orchestration.md) for the local orchestration contract.

## Verification

- source base - `0fd8b51783b4ca21c1f28c54abada3834d621eaf`
- canonical release target - `168d8342e3d1bbe724a8a06c7823f1e6e22e16ad`
- canonical archive SHA-256 - `5159ff71763fed5cbfac44d24ea57c500fbfcccde8ff674abe299fccbc5282d2`
- GitHub Checks - not configured as a mandatory gate and not reported as passed
- TCG#21 write scope - `README.md` and `docs/project-status.md`
