# Project status

Post-merge audit baseline: `main@6f99ecc1e5892b377dc611a23c7f07879d340cab` after TCG#21 and PR#23-PR#26.

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
| P0 | Publish annotated tag `v2.1.0`, public GitHub Release, ZIP and checksum assets, verify the downloaded ZIP SHA-256, install and verify Social preview | [TCG#12](https://github.com/sevranty/tech-card-generator/issues/12) | Open - publication and repository-setting writes are required | Release target `168d8342e3d1bbe724a8a06c7823f1e6e22e16ad`; expected SHA-256 `5159ff71763fed5cbfac44d24ea57c500fbfcccde8ff674abe299fccbc5282d2` |
| P1 | Register TCG in the WebFactoryOS project registry and add the task relation to TCG#20 | [WFO#64](https://github.com/sevranty/web-factory-os/issues/64) | Open external orchestration task | The relation must keep `grants_write_access=false`; WFO is not a TCG runtime, build, validation or release dependency |
| P2 | Run a native installed-skill smoke with real image generation | Deferred | Requires an environment with native installed-skill invocation and image generation | Deterministic runtime evidence remains valid in [TCG#10](https://github.com/sevranty/tech-card-generator/issues/10) |

TCG#12 is the only open product and publication gate owned by this repository. WFO#64 is tracked in WebFactoryOS and does not block local use, validation or packaging.

## Completed work

| Work | Evidence |
|---|---|
| Canonical skill publication and regression contract | [TCG#1](https://github.com/sevranty/tech-card-generator/issues/1), [TCG#2](https://github.com/sevranty/tech-card-generator/issues/2), [TCG#3](https://github.com/sevranty/tech-card-generator/issues/3), [PR#4](https://github.com/sevranty/tech-card-generator/pull/4) |
| MIT License | [TCG#5](https://github.com/sevranty/tech-card-generator/issues/5), [PR#6](https://github.com/sevranty/tech-card-generator/pull/6) |
| Root product README | [TCG#7](https://github.com/sevranty/tech-card-generator/issues/7), [PR#9](https://github.com/sevranty/tech-card-generator/pull/9) |
| End-to-end deterministic runtime evidence | [TCG#10](https://github.com/sevranty/tech-card-generator/issues/10), [PR#16](https://github.com/sevranty/tech-card-generator/pull/16) |
| Local validation gate | [TCG#11](https://github.com/sevranty/tech-card-generator/issues/11), [PR#17](https://github.com/sevranty/tech-card-generator/pull/17) |
| Reproducible v2.1.0 package | [TCG#12](https://github.com/sevranty/tech-card-generator/issues/12), [PR#18](https://github.com/sevranty/tech-card-generator/pull/18) |
| Project image and social preview source assets | [TCG#8](https://github.com/sevranty/tech-card-generator/issues/8), [PR#19](https://github.com/sevranty/tech-card-generator/pull/19) |
| Local WebFactoryOS ownership and dependency boundary | [TCG#20](https://github.com/sevranty/tech-card-generator/issues/20), [PR#22](https://github.com/sevranty/tech-card-generator/pull/22) |
| Debt ledger implementation chain normalized into one canonical document | [TCG#21](https://github.com/sevranty/tech-card-generator/issues/21), [PR#23](https://github.com/sevranty/tech-card-generator/pull/23), [PR#24](https://github.com/sevranty/tech-card-generator/pull/24), [PR#25](https://github.com/sevranty/tech-card-generator/pull/25), [PR#26](https://github.com/sevranty/tech-card-generator/pull/26), merge `6f99ecc1e5892b377dc611a23c7f07879d340cab` |
| Numberless primary-project chat naming contract | [WFO#65](https://github.com/sevranty/web-factory-os/issues/65), [PR#77](https://github.com/sevranty/web-factory-os/pull/77) |

Closed duplicate Issues [TCG#13](https://github.com/sevranty/tech-card-generator/issues/13), [TCG#14](https://github.com/sevranty/tech-card-generator/issues/14) and [TCG#15](https://github.com/sevranty/tech-card-generator/issues/15) are cross-linked to their canonical tasks and are not backlog.

PR#23, PR#24 and PR#25 were overlapping TCG#21 implementations. PR#26 removed their combined drift and is the canonical normalization result. Historical commits remain unchanged because Git history is protected.

## Boundaries

TCG owns skill implementation, references, examples, validators, tests, assets, packages, versioning and releases.

WebFactoryOS owns routing, registry placement, naming rules, task relations and orchestration status. A relation does not grant cross-repository write access.

Protected from project-status maintenance:

- `machinery-card-generator/**`
- `dist/**`
- `assets/**`
- `docs/webfactoryos-orchestration.md`
- existing tags and release history
- historical commits and merge commits
- production, deployment, DNS and secrets

See [`webfactoryos-orchestration.md`](webfactoryos-orchestration.md) for the local orchestration contract.

## Verification

- post-merge audit baseline - `6f99ecc1e5892b377dc611a23c7f07879d340cab`
- canonical release target - `168d8342e3d1bbe724a8a06c7823f1e6e22e16ad`
- canonical archive SHA-256 - `5159ff71763fed5cbfac44d24ea57c500fbfcccde8ff674abe299fccbc5282d2`
- GitHub Checks - not configured as a mandatory gate and not reported as passed
- TCG#27 write scope - `docs/project-status.md`; README remains unchanged unless its single status link becomes factually stale
