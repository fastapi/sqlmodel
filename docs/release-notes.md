# Release Notes

## Latest Changes

* 👷 Update docs deployments to Cloudflare. PR [#630](https://github.com/tiangolo/sqlmodel/pull/630) by [@tiangolo](https://github.com/tiangolo).
* 👷‍♂️ Upgrade CI for docs. PR [#628](https://github.com/tiangolo/sqlmodel/pull/628) by [@tiangolo](https://github.com/tiangolo).
* 🗑️ Deprecate Python 3.6 and upgrade Poetry and Poetry Version Plugin. PR [#627](https://github.com/tiangolo/sqlmodel/pull/627) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update CI debug mode with Tmate. PR [#629](https://github.com/tiangolo/sqlmodel/pull/629) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update latest changes token. PR [#616](https://github.com/tiangolo/sqlmodel/pull/616) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade analytics. PR [#558](https://github.com/tiangolo/sqlmodel/pull/558) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update help SQLModel docs. PR [#548](https://github.com/tiangolo/sqlmodel/pull/548) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update new issue chooser to point to GitHub Discussions. PR [#546](https://github.com/tiangolo/sqlmodel/pull/546) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add template for GitHub Discussion questions and update issues template. PR [#544](https://github.com/tiangolo/sqlmodel/pull/544) by [@tiangolo](https://github.com/tiangolo).
* 👷 Refactor CI artifact upload/download for docs previews. PR [#514](https://github.com/tiangolo/sqlmodel/pull/514) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in internal function name `get_sqlachemy_type()`. PR [#496](https://github.com/tiangolo/sqlmodel/pull/496) by [@cmarqu](https://github.com/cmarqu).
* ⬆ Bump actions/cache from 2 to 3. PR [#497](https://github.com/tiangolo/sqlmodel/pull/497) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ✏️ Fix typo in docs. PR [#446](https://github.com/tiangolo/sqlmodel/pull/446) by [@davidbrochart](https://github.com/davidbrochart).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.0 to 2.24.2. PR [#493](https://github.com/tiangolo/sqlmodel/pull/493) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ✏️ Fix typo in `docs/tutorial/create-db-and-table.md`. PR [#477](https://github.com/tiangolo/sqlmodel/pull/477) by [@FluffyDietEngine](https://github.com/FluffyDietEngine).
* ✏️ Fix small typos in docs. PR [#481](https://github.com/tiangolo/sqlmodel/pull/481) by [@micuffaro](https://github.com/micuffaro).
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

* 🐛 Fix auto detecting and setting `nullable`, allowing overrides in field. PR [#423](https://github.com/tiangolo/sqlmodel/pull/423) by [@JonasKs](https://github.com/JonasKs).
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
