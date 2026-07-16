# WebFactoryOS orchestration

## Identity

| Field | Value |
|---|---|
| PROJECT_ID | `TECH_CARD_GENERATOR` |
| SHORT_ID | `TCG` |
| Project | `tech-card-generator` |
| Skill | [`machinery-card-generator`](../machinery-card-generator/SKILL.md) |
| Repository | `https://github.com/sevranty/tech-card-generator` |
| Tasks | `https://github.com/sevranty/tech-card-generator/issues` |

`tech-card-generator` is orchestrated by [WebFactoryOS](https://github.com/sevranty/web-factory-os) but remains an autonomous repository.

## Ownership

TCG owns:

- skill implementation and prompts
- references, examples, tests and validators
- project images and release packages
- versioning, tags and GitHub Releases

WebFactoryOS owns:

- project routing and registry placement
- shared naming rules
- cross-project task relations
- orchestration status

A task relation does not grant cross-repository write access.

## Dependency boundary

WebFactoryOS is not a runtime, build, validation or release dependency of TCG.

TCG must remain usable from a clean checkout without cloning or executing WebFactoryOS. Do not import WFO scripts, reusable workflows, registry files or a second project registry into this repository.

Local validation remains canonical:

```bash
python3 -m pip install -r requirements-validation.txt
python3 machinery-card-generator/scripts/validate-repository.py
python3 scripts/build-release.py
```

## Related tasks

- [TCG#20](https://github.com/sevranty/tech-card-generator/issues/20) - local ownership and autonomy contract
- [WFO#64](https://github.com/sevranty/web-factory-os/issues/64) - project registry and task relation
- [WFO#65](https://github.com/sevranty/web-factory-os/issues/65) - atomic-skill chat naming
- [TCG#12](https://github.com/sevranty/tech-card-generator/issues/12) - independent v2.1.0 publication gate
