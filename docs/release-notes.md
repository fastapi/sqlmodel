# Release Notes

## Latest Changes

### Refactors

* 🚨 Fix types for new Pydantic. PR [#1131](https://github.com/fastapi/sqlmodel/pull/1131) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Fix typo in the release notes of v0.0.22. PR [#1195](https://github.com/fastapi/sqlmodel/pull/1195) by [@PipeKnight](https://github.com/PipeKnight).
* 📝 Update includes for `docs/advanced/uuid.md`. PR [#1151](https://github.com/fastapi/sqlmodel/pull/1151) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update includes for `docs/tutorial/create-db-and-table.md`. PR [#1149](https://github.com/fastapi/sqlmodel/pull/1149) by [@tiangolo](https://github.com/tiangolo).
* 📝 Fix internal links in docs. PR [#1148](https://github.com/fastapi/sqlmodel/pull/1148) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in documentation. PR [#1106](https://github.com/fastapi/sqlmodel/pull/1106) by [@Solipsistmonkey](https://github.com/Solipsistmonkey).
* 📝 Remove highlights in `indexes.md` . PR [#1100](https://github.com/fastapi/sqlmodel/pull/1100) by [@alejsdev](https://github.com/alejsdev).

### Internal

* ⬆️ Upgrade markdown-include-variants to version 0.0.3. PR [#1152](https://github.com/fastapi/sqlmodel/pull/1152) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update issue manager workflow. PR [#1137](https://github.com/fastapi/sqlmodel/pull/1137) by [@alejsdev](https://github.com/alejsdev).
* 👷 Fix smokeshow, checkout files on CI. PR [#1136](https://github.com/fastapi/sqlmodel/pull/1136) by [@tiangolo](https://github.com/tiangolo).
* 👷 Use uv in CI. PR [#1135](https://github.com/fastapi/sqlmodel/pull/1135) by [@tiangolo](https://github.com/tiangolo).
* ➕ Add docs dependency markdown-include-variants. PR [#1129](https://github.com/fastapi/sqlmodel/pull/1129) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update script to standardize format. PR [#1130](https://github.com/fastapi/sqlmodel/pull/1130) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `labeler.yml`. PR [#1128](https://github.com/fastapi/sqlmodel/pull/1128) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update worfkow deploy-docs-notify URL. PR [#1126](https://github.com/fastapi/sqlmodel/pull/1126) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade Cloudflare GitHub Action. PR [#1124](https://github.com/fastapi/sqlmodel/pull/1124) by [@tiangolo](https://github.com/tiangolo).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#1097](https://github.com/fastapi/sqlmodel/pull/1097) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump tiangolo/issue-manager from 0.5.0 to 0.5.1. PR [#1107](https://github.com/fastapi/sqlmodel/pull/1107) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update `issue-manager.yml`. PR [#1103](https://github.com/fastapi/sqlmodel/pull/1103) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix coverage processing in CI, one name per matrix run. PR [#1104](https://github.com/fastapi/sqlmodel/pull/1104) by [@tiangolo](https://github.com/tiangolo).
* 💚 Set `include-hidden-files` to `True` when using the `upload-artifact` GH action. PR [#1098](https://github.com/fastapi/sqlmodel/pull/1098) by [@svlandeg](https://github.com/svlandeg).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#1088](https://github.com/fastapi/sqlmodel/pull/1088) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.0.22

### Fixes

* 🐛 Fix support for types with `Optional[Annotated[x, f()]]`, e.g. `id: Optional[pydantic.UUID4]`. PR [#1093](https://github.com/fastapi/sqlmodel/pull/1093) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Fix a typo in `docs/virtual-environments.md`. PR [#1085](https://github.com/fastapi/sqlmodel/pull/1085) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add docs for virtual environments and environment variables, update contributing. PR [#1082](https://github.com/fastapi/sqlmodel/pull/1082) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add docs about repo management and team. PR [#1059](https://github.com/tiangolo/sqlmodel/pull/1059) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in `cascade_delete` docs. PR [#1030](https://github.com/tiangolo/sqlmodel/pull/1030) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ✅ Refactor test_enums to make them independent of previous imports. PR [#1095](https://github.com/fastapi/sqlmodel/pull/1095) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `latest-changes` GitHub Action. PR [#1087](https://github.com/fastapi/sqlmodel/pull/1087) by [@tiangolo](https://github.com/tiangolo).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#1028](https://github.com/fastapi/sqlmodel/pull/1028) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump ruff from 0.4.7 to 0.6.2. PR [#1081](https://github.com/fastapi/sqlmodel/pull/1081) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update lint script. PR [#1084](https://github.com/fastapi/sqlmodel/pull/1084) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update Python version for coverage. PR [#1083](https://github.com/fastapi/sqlmodel/pull/1083) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update coverage config files. PR [#1077](https://github.com/fastapi/sqlmodel/pull/1077) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add URLs to `pyproject.toml`, show up in PyPI. PR [#1074](https://github.com/fastapi/sqlmodel/pull/1074) by [@tiangolo](https://github.com/tiangolo).
* 👷 Do not sync labels as it overrides manually added labels. PR [#1073](https://github.com/fastapi/sqlmodel/pull/1073) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update configs for GitHub Action labeler, to add only one label. PR [#1072](https://github.com/fastapi/sqlmodel/pull/1072) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update labeler GitHub Actions permissions and dependencies. PR [#1071](https://github.com/fastapi/sqlmodel/pull/1071) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action label-checker. PR [#1069](https://github.com/fastapi/sqlmodel/pull/1069) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action labeler. PR [#1068](https://github.com/fastapi/sqlmodel/pull/1068) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action add-to-project. PR [#1067](https://github.com/fastapi/sqlmodel/pull/1067) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action add-to-project. PR [#1066](https://github.com/fastapi/sqlmodel/pull/1066) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update admonitions in annotations. PR [#1065](https://github.com/fastapi/sqlmodel/pull/1065) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update links from github.com/tiangolo/sqlmodel to github.com/fastapi/sqlmodel. PR [#1064](https://github.com/fastapi/sqlmodel/pull/1064) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update members. PR [#1063](https://github.com/tiangolo/sqlmodel/pull/1063) by [@tiangolo](https://github.com/tiangolo).
* 💄 Add dark-mode logo. PR [#1061](https://github.com/tiangolo/sqlmodel/pull/1061) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update docs.py script to enable dirty reload conditionally. PR [#1060](https://github.com/tiangolo/sqlmodel/pull/1060) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update MkDocs previews. PR [#1058](https://github.com/tiangolo/sqlmodel/pull/1058) by [@tiangolo](https://github.com/tiangolo).
* 💄 Update Termynal line-height. PR [#1057](https://github.com/tiangolo/sqlmodel/pull/1057) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade build docs configs. PR [#1047](https://github.com/tiangolo/sqlmodel/pull/1047) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add alls-green for test-redistribute. PR [#1055](https://github.com/tiangolo/sqlmodel/pull/1055) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update docs-previews to handle no docs changes. PR [#1056](https://github.com/tiangolo/sqlmodel/pull/1056) by [@tiangolo](https://github.com/tiangolo).
* 👷🏻 Show docs deployment status and preview URLs in comment. PR [#1054](https://github.com/tiangolo/sqlmodel/pull/1054) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Enable auto dark mode. PR [#1046](https://github.com/tiangolo/sqlmodel/pull/1046) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update issue-manager. PR [#1045](https://github.com/tiangolo/sqlmodel/pull/1045) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update issue-manager.yml GitHub Action permissions. PR [#1040](https://github.com/tiangolo/sqlmodel/pull/1040) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor Deploy Docs GitHub Action to be a script and update token preparing for org. PR [#1039](https://github.com/tiangolo/sqlmodel/pull/1039) by [@tiangolo](https://github.com/tiangolo).

## 0.0.21

### Features

* ✨ Add support for cascade delete relationships: `cascade_delete`, `ondelete`, and `passive_deletes`. Initial PR [#983](https://github.com/tiangolo/sqlmodel/pull/983) by [@estebanx64](https://github.com/estebanx64).
  * New docs at: [Cascade Delete Relationships](https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/).

### Docs

* 📝 Update docs . PR [#1003](https://github.com/tiangolo/sqlmodel/pull/1003) by [@alejsdev](https://github.com/alejsdev).

### Internal

* ⬆ Bump actions/cache from 3 to 4. PR [#783](https://github.com/tiangolo/sqlmodel/pull/783) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cairosvg from 2.7.0 to 2.7.1. PR [#919](https://github.com/tiangolo/sqlmodel/pull/919) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump jinja2 from 3.1.3 to 3.1.4. PR [#974](https://github.com/tiangolo/sqlmodel/pull/974) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.8.11 to 1.9.0. PR [#987](https://github.com/tiangolo/sqlmodel/pull/987) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mkdocstrings[python] from 0.23.0 to 0.25.1. PR [#927](https://github.com/tiangolo/sqlmodel/pull/927) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dorny/paths-filter from 2 to 3. PR [#972](https://github.com/tiangolo/sqlmodel/pull/972) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.20

### Features

* ✨ Add official UUID support, docs and tests, internally using new SQLAlchemy 2.0 types. Initial PR [#992](https://github.com/tiangolo/sqlmodel/pull/992) by [@estebanx64](https://github.com/estebanx64).
  * New docs in the [Advanced User Guide: UUID (Universally Unique Identifiers)](https://sqlmodel.tiangolo.com/advanced/uuid/).

### Docs

* ✏️ Fix internal link in `docs/tutorial/create-db-and-table.md`. PR [#911](https://github.com/tiangolo/sqlmodel/pull/911) by [@tfpgh](https://github.com/tfpgh).
* ✏️ Add missing step in `create-db-and-table-with-db-browser.md`. PR [#976](https://github.com/tiangolo/sqlmodel/pull/976) by [@alejsdev](https://github.com/alejsdev).
* ✏️ Fix typo in `docs/tutorial`. PR [#943](https://github.com/tiangolo/sqlmodel/pull/943) by [@luco17](https://github.com/luco17).
* ✏️ Fix typo in `sqlmodel/_compat.py`. PR [#950](https://github.com/tiangolo/sqlmodel/pull/950) by [@Highfire1](https://github.com/Highfire1).
* ✏️ Update pip installation command in tutorial. PR [#975](https://github.com/tiangolo/sqlmodel/pull/975) by [@alejsdev](https://github.com/alejsdev).
* ✏️ Fix typo in `docs/tutorial/relationship-attributes/index.md`. PR [#880](https://github.com/tiangolo/sqlmodel/pull/880) by [@UncleGoogle](https://github.com/UncleGoogle).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#979](https://github.com/tiangolo/sqlmodel/pull/979) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🔨 Update docs Termynal scripts to not include line nums for local dev. PR [#1018](https://github.com/tiangolo/sqlmodel/pull/1018) by [@tiangolo](https://github.com/tiangolo).

## 0.0.19

### Fixes

* 🐛 Fix pydantic `EmailStr` support and `max_length` in several String subclasses. PR [#966](https://github.com/tiangolo/sqlmodel/pull/966) by [@estebanx64](https://github.com/estebanx64).
* 🐛 Fix set varchar limit when `max_length` is set on Pydantic models using Pydantic v2. PR [#963](https://github.com/tiangolo/sqlmodel/pull/963) by [@estebanx64](https://github.com/estebanx64).

### Refactors

* ♻️ Refactor generate select template to isolate templated code to the minimum. PR [#967](https://github.com/tiangolo/sqlmodel/pull/967) by [@tiangolo](https://github.com/tiangolo).

### Upgrades

* ⬆️ Update minimum SQLAlchemy version to 2.0.14 as that one includes `TryCast` used internally. PR [#964](https://github.com/tiangolo/sqlmodel/pull/964) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Fix broken link to `@dataclass_transform` (now PEP 681) in `docs/features.md`. PR [#753](https://github.com/tiangolo/sqlmodel/pull/753) by [@soof-golan](https://github.com/soof-golan).

### Internal

* ⬆️ Upgrade Ruff and Black. PR [#968](https://github.com/tiangolo/sqlmodel/pull/968) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/issue-manager from 0.4.1 to 0.5.0. PR [#922](https://github.com/tiangolo/sqlmodel/pull/922) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 📌 Pin typing-extensions in tests for compatiblity with Python 3.8, dirty-equals, Pydantic. PR [#965](https://github.com/tiangolo/sqlmodel/pull/965) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Actions to download and upload artifacts. PR [#936](https://github.com/tiangolo/sqlmodel/pull/936) by [@tiangolo](https://github.com/tiangolo).
* 👷 Tweak CI for test-redistribute, add needed env vars for slim. PR [#929](https://github.com/tiangolo/sqlmodel/pull/929) by [@tiangolo](https://github.com/tiangolo).

## 0.0.18

### Internal

* ✨ Add `sqlmodel-slim` setup. PR [#916](https://github.com/tiangolo/sqlmodel/pull/916) by [@tiangolo](https://github.com/tiangolo).

In the future SQLModel will include the standard default recommended packages, and `sqlmodel-slim` will come without those recommended standard packages and with a group of optional dependencies `sqlmodel-slim[standard]`, equivalent to `sqlmodel`, for those that want to opt out of those packages.

* 🔧 Re-enable MkDocs Material Social plugin. PR [#915](https://github.com/tiangolo/sqlmodel/pull/915) by [@tiangolo](https://github.com/tiangolo).

## 0.0.17

### Refactors

* ♻️ Refactor types to properly support Pydantic 2.7. PR [#913](https://github.com/tiangolo/sqlmodel/pull/913) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update ModelRead to ModelPublic documentation and examples. PR [#885](https://github.com/tiangolo/sqlmodel/pull/885) by [@estebanx64](https://github.com/estebanx64).
* ✨ Add source examples for Python 3.10 and 3.9 with updated syntax. PR [#842](https://github.com/tiangolo/sqlmodel/pull/842) by [@tiangolo](https://github.com/tiangolo) and [@estebanx64](https://github.com/estebanx64).

### Internal

* ⬆ Bump actions/setup-python from 4 to 5. PR [#733](https://github.com/tiangolo/sqlmodel/pull/733) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔨 Update internal scripts and remove unused ones. PR [#914](https://github.com/tiangolo/sqlmodel/pull/914) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Migrate from Poetry to PDM for the internal build config. PR [#912](https://github.com/tiangolo/sqlmodel/pull/912) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update MkDocs, disable cards while I can upgrade to the latest MkDocs Material, that fixes an issue with social cards. PR [#888](https://github.com/tiangolo/sqlmodel/pull/888) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add cron to run test once a week on monday. PR [#869](https://github.com/tiangolo/sqlmodel/pull/869) by [@estebanx64](https://github.com/estebanx64).
* ⬆️ Upgrade Ruff version and configs. PR [#859](https://github.com/tiangolo/sqlmodel/pull/859) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove Jina QA Bot as it has been discontinued. PR [#840](https://github.com/tiangolo/sqlmodel/pull/840) by [@tiangolo](https://github.com/tiangolo).

## 0.0.16

### Features

* ✨ Add new method `.sqlmodel_update()` to update models in place, including an `update` parameter for extra data. And fix implementation for the (now documented) `update` parameter for `.model_validate()`. PR [#804](https://github.com/tiangolo/sqlmodel/pull/804) by [@tiangolo](https://github.com/tiangolo).
    * Updated docs: [Update Data with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/update/).
    * New docs: [Update with Extra Data (Hashed Passwords) with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/update-extra-data/).

## 0.0.15

### Fixes

* 🐛 Fix class initialization compatibility with Pydantic and SQLModel, fixing errors revealed by the latest Pydantic. PR [#807](https://github.com/tiangolo/sqlmodel/pull/807) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump tiangolo/issue-manager from 0.4.0 to 0.4.1. PR [#775](https://github.com/tiangolo/sqlmodel/pull/775) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Fix GitHub Actions build docs filter paths for GitHub workflows. PR [#738](https://github.com/tiangolo/sqlmodel/pull/738) by [@tiangolo](https://github.com/tiangolo).

## 0.0.14

### Features

* ✨ Add support for Pydantic v2 (while keeping support for v1 if v2 is not available). PR [#722](https://github.com/tiangolo/sqlmodel/pull/722) by [@tiangolo](https://github.com/tiangolo) including initial work in PR [#699](https://github.com/tiangolo/sqlmodel/pull/699) by [@AntonDeMeester](https://github.com/AntonDeMeester).

## 0.0.13

### Fixes

* ♻️ Refactor type generation of selects re-order to prioritize models to optimize editor support. PR [#718](https://github.com/tiangolo/sqlmodel/pull/718) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* 🔇 Do not raise deprecation warnings for execute as it's automatically used internally. PR [#716](https://github.com/tiangolo/sqlmodel/pull/716) by [@tiangolo](https://github.com/tiangolo).
* ✅ Move OpenAPI tests inline to simplify updating them with Pydantic v2. PR [#709](https://github.com/tiangolo/sqlmodel/pull/709) by [@tiangolo](https://github.com/tiangolo).

### Upgrades

* ⬆️ Add support for Python 3.11 and Python 3.12. PR [#710](https://github.com/tiangolo/sqlmodel/pull/710) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Fix typo, simplify single quote/apostrophe character in "Sister Margaret's" everywhere in the docs. PR [#721](https://github.com/tiangolo/sqlmodel/pull/721) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for Decimal, use proper types. PR [#719](https://github.com/tiangolo/sqlmodel/pull/719) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add source examples for Python 3.9 and 3.10. PR [#715](https://github.com/tiangolo/sqlmodel/pull/715) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🙈 Update gitignore, include all coverage files. PR [#711](https://github.com/tiangolo/sqlmodel/pull/711) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update config with new pymdown extensions. PR [#712](https://github.com/tiangolo/sqlmodel/pull/712) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update docs build setup, add support for sponsors, add sponsor GOVCERT.LU. PR [#720](https://github.com/tiangolo/sqlmodel/pull/720) by [@tiangolo](https://github.com/tiangolo).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#697](https://github.com/tiangolo/sqlmodel/pull/697) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🔧 Show line numbers in docs during local development. PR [#714](https://github.com/tiangolo/sqlmodel/pull/714) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update details syntax with new pymdown extensions format. PR [#713](https://github.com/tiangolo/sqlmodel/pull/713) by [@tiangolo](https://github.com/tiangolo).

## 0.0.12

### Features

* ✨ Upgrade SQLAlchemy to 2.0. PR [#700](https://github.com/tiangolo/sqlmodel/pull/700) by [@tiangolo](https://github.com/tiangolo) including initial work in PR [#563](https://github.com/tiangolo/sqlmodel/pull/563) by [@farahats9](https://github.com/farahats9).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#686](https://github.com/tiangolo/sqlmodel/pull/686) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 👷 Upgrade latest-changes GitHub Action. PR [#693](https://github.com/tiangolo/sqlmodel/pull/693) by [@tiangolo](https://github.com/tiangolo).

## 0.0.11

### Features

* ✨ Add support for passing a custom SQLAlchemy type to `Field()` with `sa_type`. PR [#505](https://github.com/tiangolo/sqlmodel/pull/505) by [@maru0123-2004](https://github.com/maru0123-2004).
    * You might consider this a breaking change if you were using an incompatible combination of arguments, those arguments were not taking effect and now you will have a type error and runtime error telling you that.
* ✨ Do not allow invalid combinations of field parameters for columns and relationships, `sa_column` excludes `sa_column_args`, `primary_key`, `nullable`, etc. PR [#681](https://github.com/tiangolo/sqlmodel/pull/681) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 🎨 Update inline source examples, hide `#` in annotations (from MkDocs Material). PR [#677](https://github.com/tiangolo/sqlmodel/pull/677) by [@Matthieu-LAURENT39](https://github.com/Matthieu-LAURENT39).

### Internal

* ⬆ Update coverage requirement from ^6.2 to >=6.2,<8.0. PR [#663](https://github.com/tiangolo/sqlmodel/pull/663) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update mkdocs-material requirement from 9.1.21 to 9.2.7. PR [#675](https://github.com/tiangolo/sqlmodel/pull/675) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Upgrade mypy manually. PR [#684](https://github.com/tiangolo/sqlmodel/pull/684) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Update black requirement from ^22.10.0 to >=22.10,<24.0. PR [#664](https://github.com/tiangolo/sqlmodel/pull/664) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update CI to build MkDocs Insiders only when the secrets are available, for Dependabot. PR [#683](https://github.com/tiangolo/sqlmodel/pull/683) by [@tiangolo](https://github.com/tiangolo).

## 0.0.10

### Features

* ✨ Add support for all `Field` parameters from Pydantic `1.9.0` and above, make Pydantic `1.9.0` the minimum required version. PR [#440](https://github.com/tiangolo/sqlmodel/pull/440) by [@daniil-berg](https://github.com/daniil-berg).

### Internal

* 🔧 Adopt Ruff for formatting. PR [#679](https://github.com/tiangolo/sqlmodel/pull/679) by [@tiangolo](https://github.com/tiangolo).

## 0.0.9

### Breaking Changes

* 🗑️ Deprecate Python 3.6 and upgrade Poetry and Poetry Version Plugin. PR [#627](https://github.com/tiangolo/sqlmodel/pull/627) by [@tiangolo](https://github.com/tiangolo).

### Features

* ✨ Raise a more clear error when a type is not valid. PR [#425](https://github.com/tiangolo/sqlmodel/pull/425) by [@ddanier](https://github.com/ddanier).

### Fixes

* 🐛 Fix `AsyncSession` type annotations for `exec()`. PR [#58](https://github.com/tiangolo/sqlmodel/pull/58) by [@Bobronium](https://github.com/Bobronium).
* 🐛 Fix allowing using a `ForeignKey` directly, remove repeated column construction from `SQLModelMetaclass.__init__` and upgrade minimum SQLAlchemy to `>=1.4.36`. PR [#443](https://github.com/tiangolo/sqlmodel/pull/443) by [@daniil-berg](https://github.com/daniil-berg).
* 🐛 Fix enum type checks ordering in `get_sqlalchemy_type`. PR [#669](https://github.com/tiangolo/sqlmodel/pull/669) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix SQLAlchemy version 1.4.36 breaks SQLModel relationships (#315). PR [#461](https://github.com/tiangolo/sqlmodel/pull/461) by [@byrman](https://github.com/byrman).

### Upgrades

* ⬆️ Upgrade support for SQLAlchemy 1.4.49, update tests. PR [#519](https://github.com/tiangolo/sqlmodel/pull/519) by [@sandrotosi](https://github.com/sandrotosi).
* ⬆ Raise SQLAlchemy version requirement to at least `1.4.29` (related to #434). PR [#439](https://github.com/tiangolo/sqlmodel/pull/439) by [@daniil-berg](https://github.com/daniil-berg).

### Docs

* 📝 Clarify description of in-memory SQLite database in `docs/tutorial/create-db-and-table.md`. PR [#601](https://github.com/tiangolo/sqlmodel/pull/601) by [@SimonCW](https://github.com/SimonCW).
* 📝 Tweak wording in `docs/tutorial/fastapi/multiple-models.md`. PR [#674](https://github.com/tiangolo/sqlmodel/pull/674) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix contributing instructions to run tests, update script name. PR [#634](https://github.com/tiangolo/sqlmodel/pull/634) by [@PookieBuns](https://github.com/PookieBuns).
* 📝 Update link to docs for intro to databases. PR [#593](https://github.com/tiangolo/sqlmodel/pull/593) by [@abenezerBelachew](https://github.com/abenezerBelachew).
* 📝 Update docs, use `offset` in example with `limit` and `where`. PR [#273](https://github.com/tiangolo/sqlmodel/pull/273) by [@jbmchuck](https://github.com/jbmchuck).
* 📝 Fix docs for Pydantic's fields using `le` (`lte` is invalid, use `le` ). PR [#207](https://github.com/tiangolo/sqlmodel/pull/207) by [@jrycw](https://github.com/jrycw).
* 📝 Update outdated link in `docs/db-to-code.md`. PR [#649](https://github.com/tiangolo/sqlmodel/pull/649) by [@MatveyF](https://github.com/MatveyF).
* ✏️ Fix typos found with codespell. PR [#520](https://github.com/tiangolo/sqlmodel/pull/520) by [@kianmeng](https://github.com/kianmeng).
* 📝 Fix typos (duplication) in main page. PR [#631](https://github.com/tiangolo/sqlmodel/pull/631) by [@Mr-DRP](https://github.com/Mr-DRP).
* 📝 Update release notes, add second author to PR. PR [#429](https://github.com/tiangolo/sqlmodel/pull/429) by [@br-follow](https://github.com/br-follow).
* 📝 Update instructions about how to make a foreign key required in `docs/tutorial/relationship-attributes/define-relationships-attributes.md`. PR [#474](https://github.com/tiangolo/sqlmodel/pull/474) by [@jalvaradosegura](https://github.com/jalvaradosegura).
* 📝 Update help SQLModel docs. PR [#548](https://github.com/tiangolo/sqlmodel/pull/548) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in internal function name `get_sqlachemy_type()`. PR [#496](https://github.com/tiangolo/sqlmodel/pull/496) by [@cmarqu](https://github.com/cmarqu).
* ✏️ Fix typo in docs. PR [#446](https://github.com/tiangolo/sqlmodel/pull/446) by [@davidbrochart](https://github.com/davidbrochart).
* ✏️ Fix typo in `docs/tutorial/create-db-and-table.md`. PR [#477](https://github.com/tiangolo/sqlmodel/pull/477) by [@FluffyDietEngine](https://github.com/FluffyDietEngine).
* ✏️ Fix small typos in docs. PR [#481](https://github.com/tiangolo/sqlmodel/pull/481) by [@micuffaro](https://github.com/micuffaro).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#672](https://github.com/tiangolo/sqlmodel/pull/672) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.2 to 2.28.0. PR [#660](https://github.com/tiangolo/sqlmodel/pull/660) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ✅ Refactor OpenAPI FastAPI tests to simplify updating them later, this moves things around without changes. PR [#671](https://github.com/tiangolo/sqlmodel/pull/671) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/checkout from 3 to 4. PR [#670](https://github.com/tiangolo/sqlmodel/pull/670) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update mypy config, use `strict = true` instead of manual configs. PR [#428](https://github.com/tiangolo/sqlmodel/pull/428) by [@michaeloliverx](https://github.com/michaeloliverx).
* ⬆️ Upgrade MkDocs Material. PR [#668](https://github.com/tiangolo/sqlmodel/pull/668) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Update docs format and references with pre-commit and Ruff. PR [#667](https://github.com/tiangolo/sqlmodel/pull/667) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Run pre-commit on all files and autoformat. PR [#666](https://github.com/tiangolo/sqlmodel/pull/666) by [@tiangolo](https://github.com/tiangolo).
* 👷 Move to Ruff and add pre-commit. PR [#661](https://github.com/tiangolo/sqlmodel/pull/661) by [@tiangolo](https://github.com/tiangolo).
* 🛠️ Add `CITATION.cff` file for academic citations. PR [#13](https://github.com/tiangolo/sqlmodel/pull/13) by [@sugatoray](https://github.com/sugatoray).
* 👷 Update docs deployments to Cloudflare. PR [#630](https://github.com/tiangolo/sqlmodel/pull/630) by [@tiangolo](https://github.com/tiangolo).
* 👷‍♂️ Upgrade CI for docs. PR [#628](https://github.com/tiangolo/sqlmodel/pull/628) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update CI debug mode with Tmate. PR [#629](https://github.com/tiangolo/sqlmodel/pull/629) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update latest changes token. PR [#616](https://github.com/tiangolo/sqlmodel/pull/616) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade analytics. PR [#558](https://github.com/tiangolo/sqlmodel/pull/558) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update new issue chooser to point to GitHub Discussions. PR [#546](https://github.com/tiangolo/sqlmodel/pull/546) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add template for GitHub Discussion questions and update issues template. PR [#544](https://github.com/tiangolo/sqlmodel/pull/544) by [@tiangolo](https://github.com/tiangolo).
* 👷 Refactor CI artifact upload/download for docs previews. PR [#514](https://github.com/tiangolo/sqlmodel/pull/514) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/cache from 2 to 3. PR [#497](https://github.com/tiangolo/sqlmodel/pull/497) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.0 to 2.24.2. PR [#493](https://github.com/tiangolo/sqlmodel/pull/493) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update Smokeshow coverage threshold. PR [#487](https://github.com/tiangolo/sqlmodel/pull/487) by [@tiangolo](https://github.com/tiangolo).
* 👷 Move from Codecov to Smokeshow. PR [#486](https://github.com/tiangolo/sqlmodel/pull/486) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/setup-python from 2 to 4. PR [#411](https://github.com/tiangolo/sqlmodel/pull/411) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update black requirement from ^21.5-beta.1 to ^22.10.0. PR [#460](https://github.com/tiangolo/sqlmodel/pull/460) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ➕ Add extra dev dependencies for MkDocs Material. PR [#485](https://github.com/tiangolo/sqlmodel/pull/485) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Update mypy requirement from 0.930 to 0.971. PR [#380](https://github.com/tiangolo/sqlmodel/pull/380) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update coverage requirement from ^5.5 to ^6.2. PR [#171](https://github.com/tiangolo/sqlmodel/pull/171) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump codecov/codecov-action from 2 to 3. PR [#415](https://github.com/tiangolo/sqlmodel/pull/415) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/upload-artifact from 2 to 3. PR [#412](https://github.com/tiangolo/sqlmodel/pull/412) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update flake8 requirement from ^3.9.2 to ^5.0.4. PR [#396](https://github.com/tiangolo/sqlmodel/pull/396) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update pytest requirement from ^6.2.4 to ^7.0.1. PR [#242](https://github.com/tiangolo/sqlmodel/pull/242) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 2 to 3.1.0. PR [#458](https://github.com/tiangolo/sqlmodel/pull/458) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.9.0 to 2.24.0. PR [#470](https://github.com/tiangolo/sqlmodel/pull/470) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update Dependabot config. PR [#484](https://github.com/tiangolo/sqlmodel/pull/484) by [@tiangolo](https://github.com/tiangolo).

## 0.0.8

### Fixes

* 🐛 Fix auto detecting and setting `nullable`, allowing overrides in field. PR [#423](https://github.com/tiangolo/sqlmodel/pull/423) by [@JonasKs](https://github.com/JonasKs) and [@br-follow](https://github.com/br-follow).
* ♻️ Update `expresion.py`, sync from Jinja2 template, implement `inherit_cache` to solve errors like: `SAWarning: Class SelectOfScalar will not make use of SQL compilation caching`. PR [#422](https://github.com/tiangolo/sqlmodel/pull/422) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Adjust and clarify docs for `docs/tutorial/create-db-and-table.md`. PR [#426](https://github.com/tiangolo/sqlmodel/pull/426) by [@tiangolo](https://github.com/tiangolo).
* ✏ Fix typo in `docs/tutorial/connect/remove-data-connections.md`. PR [#421](https://github.com/tiangolo/sqlmodel/pull/421) by [@VerdantFox](https://github.com/VerdantFox).

## 0.0.7

### Features

* ✨ Allow setting `unique` in `Field()` for a column. PR [#83](https://github.com/tiangolo/sqlmodel/pull/83) by [@raphaelgibson](https://github.com/raphaelgibson).
* ✨ Update GUID handling to use stdlib `UUID.hex` instead of an `int`. PR [#26](https://github.com/tiangolo/sqlmodel/pull/26) by [@andrewbolster](https://github.com/andrewbolster).
* ✨ Raise an exception when using a Pydantic field type with no matching SQLAlchemy type. PR [#18](https://github.com/tiangolo/sqlmodel/pull/18) by [@elben10](https://github.com/elben10).
* ⬆ Upgrade constrain for SQLAlchemy = ">=1.4.17,<=1.4.41". PR [#371](https://github.com/tiangolo/sqlmodel/pull/371) by [@RobertRosca](https://github.com/RobertRosca).
* ✨ Add new `Session.get()` parameter `execution_options`. PR [#302](https://github.com/tiangolo/sqlmodel/pull/302) by [@tiangolo](https://github.com/tiangolo).

### Fixes

* 🐛 Fix type annotations for `Model.parse_obj()`, and `Model.validate()`. PR [#321](https://github.com/tiangolo/sqlmodel/pull/321) by [@phi-friday](https://github.com/phi-friday).
* 🐛 Fix `Select` and `SelectOfScalar` to inherit cache to avoid warning: `SAWarning: Class SelectOfScalar will not make use of SQL compilation caching`. PR [#234](https://github.com/tiangolo/sqlmodel/pull/234) by [@rabinadk1](https://github.com/rabinadk1).
* 🐛 Fix handling validators for non-default values. PR [#253](https://github.com/tiangolo/sqlmodel/pull/253) by [@byrman](https://github.com/byrman).
* 🐛 Fix fields marked as "set" in models. PR [#117](https://github.com/tiangolo/sqlmodel/pull/117) by [@statt8900](https://github.com/statt8900).
* 🐛 Fix Enum handling in SQLAlchemy. PR [#165](https://github.com/tiangolo/sqlmodel/pull/165) by [@chriswhite199](https://github.com/chriswhite199).
* 🐛 Fix setting nullable property of Fields that don't accept `None`. PR [#79](https://github.com/tiangolo/sqlmodel/pull/79) by [@van51](https://github.com/van51).
* 🐛 Fix SQLAlchemy version 1.4.36 breaks SQLModel relationships (#315). PR [#322](https://github.com/tiangolo/sqlmodel/pull/322) by [@byrman](https://github.com/byrman).

### Docs

* 📝 Update docs for models for updating, `id` should not be updatable. PR [#335](https://github.com/tiangolo/sqlmodel/pull/335) by [@kurtportelli](https://github.com/kurtportelli).
* ✏ Fix broken variable/typo in docs for Read Relationships, `hero_spider_boy.id` => `hero_spider_boy.team_id`. PR [#106](https://github.com/tiangolo/sqlmodel/pull/106) by [@yoannmos](https://github.com/yoannmos).
* 🎨 Remove unwanted highlight in the docs. PR [#233](https://github.com/tiangolo/sqlmodel/pull/233) by [@jalvaradosegura](https://github.com/jalvaradosegura).
* ✏ Fix typos in `docs/databases.md` and `docs/tutorial/index.md`. PR [#35](https://github.com/tiangolo/sqlmodel/pull/35) by [@prrao87](https://github.com/prrao87).
* ✏ Fix typo in `docs/tutorial/relationship-attributes/define-relationships-attributes.md`. PR [#239](https://github.com/tiangolo/sqlmodel/pull/239) by [@jalvaradosegura](https://github.com/jalvaradosegura).
* ✏ Fix typo in `docs/tutorial/fastapi/simple-hero-api.md`. PR [#80](https://github.com/tiangolo/sqlmodel/pull/80) by [@joemudryk](https://github.com/joemudryk).
* ✏ Fix typos in multiple files in the docs. PR [#400](https://github.com/tiangolo/sqlmodel/pull/400) by [@VictorGambarini](https://github.com/VictorGambarini).
* ✏ Fix typo in `docs/tutorial/code-structure.md`. PR [#344](https://github.com/tiangolo/sqlmodel/pull/344) by [@marciomazza](https://github.com/marciomazza).
* ✏ Fix typo in `docs/db-to-code.md`. PR [#155](https://github.com/tiangolo/sqlmodel/pull/155) by [@gr8jam](https://github.com/gr8jam).
* ✏ Fix typo in `docs/contributing.md`. PR [#323](https://github.com/tiangolo/sqlmodel/pull/323) by [@Fardad13](https://github.com/Fardad13).
* ✏ Fix typo in `docs/tutorial/fastapi/tests.md`. PR [#265](https://github.com/tiangolo/sqlmodel/pull/265) by [@johnhoman](https://github.com/johnhoman).
* ✏ Fix typo in `docs/tutorial/where.md`. PR [#286](https://github.com/tiangolo/sqlmodel/pull/286) by [@jalvaradosegura](https://github.com/jalvaradosegura).
* ✏ Fix typos in `docs/tutorial/fastapi/update.md`. PR [#268](https://github.com/tiangolo/sqlmodel/pull/268) by [@cirrusj](https://github.com/cirrusj).
* ✏ Fix typo in `docs/tutorial/fastapi/simple-hero-api.md`. PR [#247](https://github.com/tiangolo/sqlmodel/pull/247) by [@hao-wang](https://github.com/hao-wang).
* ✏ Fix typos in `docs/tutorial/automatic-id-none-refresh.md`, `docs/tutorial/fastapi/update.md`, `docs/tutorial/select.md`. PR [#185](https://github.com/tiangolo/sqlmodel/pull/185) by [@rootux](https://github.com/rootux).
* ✏ Fix typo in `docs/databases.md`. PR [#177](https://github.com/tiangolo/sqlmodel/pull/177) by [@seandlg](https://github.com/seandlg).
* ✏ Fix typos in `docs/tutorial/fastapi/update.md`. PR [#162](https://github.com/tiangolo/sqlmodel/pull/162) by [@wmcgee3](https://github.com/wmcgee3).
* ✏ Fix typos in `docs/tutorial/code-structure.md`, `docs/tutorial/fastapi/multiple-models.md`, `docs/tutorial/fastapi/simple-hero-api.md`, `docs/tutorial/many-to-many/index.md`. PR [#116](https://github.com/tiangolo/sqlmodel/pull/116) by [@moonso](https://github.com/moonso).
* ✏ Fix typo in `docs/tutorial/fastapi/teams.md`. PR [#154](https://github.com/tiangolo/sqlmodel/pull/154) by [@chrisgoddard](https://github.com/chrisgoddard).
* ✏ Fix typo variable in example about relationships and `back_populates`, always use `hero` instead of `owner`. PR [#120](https://github.com/tiangolo/sqlmodel/pull/120) by [@onionj](https://github.com/onionj).
* ✏ Fix typo in `docs/tutorial/fastapi/tests.md`. PR [#113](https://github.com/tiangolo/sqlmodel/pull/113) by [@feanil](https://github.com/feanil).
* ✏ Fix typo in `docs/tutorial/where.md`. PR [#72](https://github.com/tiangolo/sqlmodel/pull/72) by [@ZettZet](https://github.com/ZettZet).
* ✏ Fix typo in `docs/tutorial/code-structure.md`. PR [#91](https://github.com/tiangolo/sqlmodel/pull/91) by [@dhiraj](https://github.com/dhiraj).
* ✏ Fix broken link to newsletter sign-up in `docs/help.md`. PR [#84](https://github.com/tiangolo/sqlmodel/pull/84) by [@mborus](https://github.com/mborus).
* ✏ Fix typos in `docs/tutorial/many-to-many/create-models-with-link.md`. PR [#45](https://github.com/tiangolo/sqlmodel/pull/45) by [@xginn8](https://github.com/xginn8).
* ✏ Fix typo in `docs/tutorial/index.md`. PR [#398](https://github.com/tiangolo/sqlmodel/pull/398) by [@ryangrose](https://github.com/ryangrose).

### Internal

* ♻ Refactor internal statements to simplify code. PR [#53](https://github.com/tiangolo/sqlmodel/pull/53) by [@yezz123](https://github.com/yezz123).
* ♻ Refactor internal imports to reduce redundancy. PR [#272](https://github.com/tiangolo/sqlmodel/pull/272) by [@aminalaee](https://github.com/aminalaee).
* ⬆ Update development requirement for FastAPI from `^0.68.0` to `^0.68.1`. PR [#48](https://github.com/tiangolo/sqlmodel/pull/48) by [@alucarddelta](https://github.com/alucarddelta).
* ⏪ Revert upgrade Poetry, to make a release that supports Python 3.6 first. PR [#417](https://github.com/tiangolo/sqlmodel/pull/417) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add dependabot for GitHub Actions. PR [#410](https://github.com/tiangolo/sqlmodel/pull/410) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade Poetry to version `==1.2.0b1`. PR [#303](https://github.com/tiangolo/sqlmodel/pull/303) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add CI for Python 3.10. PR [#305](https://github.com/tiangolo/sqlmodel/pull/305) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add Jina's QA Bot to the docs to help people that want to ask quick questions. PR [#263](https://github.com/tiangolo/sqlmodel/pull/263) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade Codecov GitHub Action. PR [#304](https://github.com/tiangolo/sqlmodel/pull/304) by [@tiangolo](https://github.com/tiangolo).
* 💚 Only run CI on push when on master, to avoid duplicate runs on PRs. PR [#244](https://github.com/tiangolo/sqlmodel/pull/244) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Upgrade MkDocs Material and update configs. PR [#217](https://github.com/tiangolo/sqlmodel/pull/217) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Upgrade mypy, fix type annotations. PR [#218](https://github.com/tiangolo/sqlmodel/pull/218) by [@tiangolo](https://github.com/tiangolo).

## 0.0.6

### Breaking Changes

**SQLModel** no longer creates indexes by default for every column, indexes are now opt-in. You can read more about it in PR [#205](https://github.com/tiangolo/sqlmodel/pull/205).

Before this change, if you had a model like this:

```Python
from typing import Optional

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

...when creating the tables, SQLModel version `0.0.5` and below, would also create an index for `name`, one for `secret_name`, and one for `age` (`id` is the primary key, so it doesn't need an additional index).

If you depended on having an index for each one of those columns, now you can (and would have to) define them explicitly:

```Python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
```

There's a high chance you don't need indexes for all the columns. For example, you might only need indexes for `name` and `age`, but not for `secret_name`. In that case, you could define the model as:

```Python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
```

If you already created your database tables with SQLModel using versions `0.0.5` or below, it would have also created those indexes in the database. In that case, you might want to manually drop (remove) some of those indexes, if they are unnecessary, to avoid the extra cost in performance and space.

Depending on the database you are using, there will be a different way to find the available indexes.

For example, let's say you no longer need the index for `secret_name`. You could check the current indexes in the database and find the one for `secret_name`, it could be named `ix_hero_secret_name`. Then you can remove it with SQL:

```SQL
DROP INDEX ix_hero_secret_name
```

or

```SQL
DROP INDEX ix_hero_secret_name ON hero;
```

Here's the new, extensive documentation explaining indexes and how to use them: [Indexes - Optimize Queries](https://sqlmodel.tiangolo.com/tutorial/indexes/).

### Docs

* ✨ Document indexes and make them opt-in. Here's the new documentation: [Indexes - Optimize Queries](https://sqlmodel.tiangolo.com/tutorial/indexes/). This is the same change described above in **Breaking Changes**. PR [#205](https://github.com/tiangolo/sqlmodel/pull/205) by [@tiangolo](https://github.com/tiangolo).
* ✏ Fix typo in FastAPI tutorial. PR [#192](https://github.com/tiangolo/sqlmodel/pull/192) by [@yaquelinehoyos](https://github.com/yaquelinehoyos).
* 📝 Add links to the license file. PR [#29](https://github.com/tiangolo/sqlmodel/pull/29) by [@sobolevn](https://github.com/sobolevn).
* ✏ Fix typos in docs titles. PR [#28](https://github.com/tiangolo/sqlmodel/pull/28) by [@Batalex](https://github.com/Batalex).
* ✏ Fix multiple typos and some rewording. PR [#22](https://github.com/tiangolo/sqlmodel/pull/22) by [@egrim](https://github.com/egrim).
* ✏ Fix typo in `docs/tutorial/automatic-id-none-refresh.md`. PR [#14](https://github.com/tiangolo/sqlmodel/pull/14) by [@leynier](https://github.com/leynier).
* ✏ Fix typos in `docs/tutorial/index.md` and `docs/databases.md`. PR [#5](https://github.com/tiangolo/sqlmodel/pull/5) by [@sebastianmarines](https://github.com/sebastianmarines).

## 0.0.5

### Features

* ✨ Add support for Decimal fields from Pydantic and SQLAlchemy. Original PR [#103](https://github.com/tiangolo/sqlmodel/pull/103) by [@robcxyz](https://github.com/robcxyz). New docs: [Advanced User Guide - Decimal Numbers](https://sqlmodel.tiangolo.com/advanced/decimal/).

### Docs

* ✏ Update decimal tutorial source for consistency. PR [#188](https://github.com/tiangolo/sqlmodel/pull/188) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔧 Split MkDocs insiders build in CI to support building from PRs. PR [#186](https://github.com/tiangolo/sqlmodel/pull/186) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Format `expression.py` and expression template, currently needed by CI. PR [#187](https://github.com/tiangolo/sqlmodel/pull/187) by [@tiangolo](https://github.com/tiangolo).
* 🐛Fix docs light/dark theme switcher. PR [#1](https://github.com/tiangolo/sqlmodel/pull/1) by [@Lehoczky](https://github.com/Lehoczky).
* 🔧 Add MkDocs Material social cards. PR [#90](https://github.com/tiangolo/sqlmodel/pull/90) by [@tiangolo](https://github.com/tiangolo).
* ✨ Update type annotations and upgrade mypy. PR [#173](https://github.com/tiangolo/sqlmodel/pull/173) by [@tiangolo](https://github.com/tiangolo).

## 0.0.4

* 🎨 Fix type detection of select results in PyCharm. PR [#15](https://github.com/tiangolo/sqlmodel/pull/15) by [@tiangolo](https://github.com/tiangolo).

## 0.0.3

* ⬆️ Update and relax specification range for `sqlalchemy-stubs`. PR [#4](https://github.com/tiangolo/sqlmodel/pull/4) by [@tiangolo](https://github.com/tiangolo).

## 0.0.2

* This includes several small bug fixes detected during the first CI runs.
* 💚 Fix CI installs and tests. PR [#2](https://github.com/tiangolo/sqlmodel/pull/2) by [@tiangolo](https://github.com/tiangolo).

## 0.0.1

* First release. 🎉
