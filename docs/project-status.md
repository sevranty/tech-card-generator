# Project status and debt ledger

- Task: TCG#21 — residual debt ledger and status cleanup.
- PR: Add project status ledger and link from README.
- Status: blocked by external GitHub/release access and dependency download limits; local scope changes complete.
- Scope: audits residual debt on top of `main@45aea73db748adabdc1f851828deeef9bab69f6b` without changing `machinery-card-generator/**`, `dist/**`, or `assets/**`.

## Evidence

- Base HEAD confirmed: `git rev-parse HEAD` returned `45aea73db748adabdc1f851828deeef9bab69f6b` before TCG#21 edits.
- Local Git history confirms merged repository work: PR#4 `8083603`, PR#6 `50b29f1`, PR#9 `5f3c8c8`, PR#16 `806b5f6`, PR#17 `82be3a5`, PR#18 `168d834`, PR#19 `45aea73`.
- GitHub CLI audit blocked: `gh issue list --state all --limit 50 --json number,title,state,url,closedAt,updatedAt && gh pr list --state all --limit 50 --json number,title,state,url,mergedAt,headRefName,baseRefName` failed with `/bin/bash: line 1: gh: command not found`.
- GitHub API audit blocked: `python3 - <<'PY' ... urllib.request.urlopen('https://api.github.com/repos/sevranty/tech-card-generator/issues/12') ... PY` failed with `URLError <urlopen error Tunnel connection failed: 403 Forbidden>` for TCG#12, TCG#20, TCG#21, PR#18, PR#19, WFO#64 and WFO#65.
- Declared dependency install blocked: `python3 -m pip install -r requirements-validation.txt` failed with `ERROR: No matching distribution found for PyYAML<7,>=6` after the package index tunnel returned `403 Forbidden` for `/simple/pyyaml/`.
- Alternate PyPI install blocked the same way: `python3 -m pip install -r requirements-validation.txt --index-url https://pypi.org/simple` returned the same `403 Forbidden` tunnel failure and PyYAML resolution error.
- Repository validation blocked by missing dependency: `python3 machinery-card-generator/scripts/validate-repository.py` failed with `ModuleNotFoundError: No module named 'yaml'`.
- Release reproducibility check blocked by the same missing dependency: `python3 scripts/build-release.py` failed because extracted skill validation returned `ModuleNotFoundError: No module named 'yaml'`.
- Conflict marker scan clean: `rg -n '^(<<<<<<<|=======|>>>>>>>)' README.md docs` produced no output.
- Protected paths clean after validation attempts: `git diff -- machinery-card-generator dist assets --stat` produced no output.

## Debt ledger

| Priority | Item | Owner | Status | Link | Evidence / blocker | Next action |
|---|---|---|---|---|---|---|
| P0 | Annotated tag `v2.1.0`, GitHub Release, ZIP/checksum assets, downloaded checksum verification, actual Social preview, close TCG#12. | TCG#12 | blocked | https://github.com/sevranty/tech-card-generator/issues/12 | Release publication is outside local repository write scope. Live GitHub verification is blocked by missing `gh` and API tunnel `403 Forbidden`. | Owner with GitHub release access publishes and verifies assets, then closes TCG#12. |
| P1 | Local WebFactoryOS ownership and autonomy docs. | TCG#20 | open | https://github.com/sevranty/tech-card-generator/issues/20 | No TCG#20 documentation merge is present in `main@45aea73db748adabdc1f851828deeef9bab69f6b`; live issue verification is blocked. | Land the TCG repository PR for TCG#20, then link the factual document from README. |
| P1 | Register `TECH_CARD_GENERATOR` / `TCG` and relation to TCG#20. | WFO#64 | external | https://github.com/sevranty/web-factory-os/issues/64 | WFO registry and naming files are protected resources for this task and live outside this repository scope; live issue verification is blocked. | Complete WFO#64 in the WebFactoryOS repository. |
| P1 | Numberless primary chat contract for atomic skills. | WFO#65 | external | https://github.com/sevranty/web-factory-os/issues/65 | WFO contract files are protected resources for this task and live outside this repository scope; live issue verification is blocked. | Complete WFO#65 in the WebFactoryOS repository. |
| P1 | Remove stale README future-state text after referenced tasks become factual. | TCG#21 | local scope complete; external follow-up blocked | https://github.com/sevranty/tech-card-generator/issues/21 | README now points to this ledger, removes the empty future-packaging heading, and states project image assets factually. Release and WFO completion are not claimed. | After TCG#12 and TCG#20 are complete, replace remaining blockers with direct factual links. |
| P2 | Native installed-skill runtime smoke with real image generation. | deferred | deferred | `machinery-card-generator/tests/runtime/runtime-report.md` | Deterministic runtime evidence remains valid. Native installed-skill image generation requires an environment that exposes native skill invocation and image generation. | Run only in an environment with native skill invocation and real image generation. |

## Completed work not reopened

- Canonical skill publication: PR#4, commit `8083603`.
- MIT License: PR#6, commit `50b29f1`.
- Root product README: PR#9, commit `5f3c8c8`.
- Runtime evidence: PR#16, commit `806b5f6`.
- Local validation gate: PR#17, commit `82be3a5`.
- Reproducible v2.1.0 package: PR#18, commit `168d834`; artifacts remain under `dist/`.
- Project image assets: PR#19, commit `45aea73`; assets remain under `assets/`.
- Duplicate Issues #13, #14 and #15: not modified by TCG#21; live issue state requires GitHub access.

## Protected path review

TCG#21 changed only `README.md` and `docs/project-status.md`. Protected paths `machinery-card-generator/**`, `dist/**`, and `assets/**` have no final diff.
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
