<p align="center">
  <a href="https://sqlmodel.tiangolo.com"><img src="https://sqlmodel.tiangolo.com/img/logo-margin/logo-margin-vector.svg#only-light" alt="SQLModel"></a>

</p>
<p align="center">
    <em>SQLModel，专为简洁、高兼容性与高稳健性设计的 Python SQL 数据库交互库。</em>
</p>
<p align="center">
    <b>简体中文</b> | <a href="README.md"><b>English</b></a>
</p>
<p align="center">
<a href="https://github.com/fastapi/sqlmodel/actions?query=workflow%3ATest+event%3Apush+branch%3Amain">
    <img src="https://github.com/fastapi/sqlmodel/actions/workflows/test.yml/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/sqlmodel">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/sqlmodel.svg" alt="Coverage">
<a href="https://pypi.org/project/sqlmodel">
    <img src="https://img.shields.io/pypi/v/sqlmodel?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**官方文档**：[https://sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)

**源代码**：[https://github.com/fastapi/sqlmodel](https://github.com/fastapi/sqlmodel)

---

SQLModel 是一个在 Python 代码中通过原生 Python 对象与<abbr title="亦称关系型数据库">SQL 数据库</abbr>进行交互的高级库。其核心设计目标为：符合直觉、极简易用、高度兼容与运行稳健。

**SQLModel** 基于 Python 类型注解构建，底层由 [Pydantic](https://pydantic-docs.helpmanual.io/) 与 [SQLAlchemy](https://sqlalchemy.org/) 强力驱动。

核心特性包括：

* **直观的书写体验**：极致的编辑器支持，随处可见的代码<abbr title="亦称自动补全、代码智能感知、IntelliSense">自动补全</abbr>，显著减少调试时间。易学易用，大幅降低查阅文档的心智负担。
* **极简易用**：具备合理的默认配置，底层自动完成繁复的胶水层操作以简化业务代码。
* **高度兼容**：专为深度兼容 **FastAPI**、Pydantic 和 SQLAlchemy 而设计。
* **功能易于扩展**：底层完整保留了 SQLAlchemy 和 Pydantic 的全部强大功能。
* **代码精炼**：最大限度消除代码重复定义。单次类型注解即可同时满足数据验证与数据库映射，无需在 SQLAlchemy 与 Pydantic 之间重复声明模型。

## 赞助商 (Sponsors)

<!-- sponsors -->

<a href="https://www.govcert.lu" target="_blank" title="This project is being supported by GOVCERT.LU"><img src="https://sqlmodel.tiangolo.com/img/sponsors/govcert.png"></a>

<!-- /sponsors -->

## FastAPI 中的 SQL 数据库支持

<a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" style="width: 20%;"></a>

**SQLModel** 专为简化 [FastAPI](https://fastapi.tiangolo.com) 应用中与 SQL 数据库的交互而打造，两者出自同一[作者](https://tiangolo.com/)之手。😁

它将 SQLAlchemy 与 Pydantic 融为一体，最大程度精简业务代码，使**代码冗余降至最低**，同时提供**极致的开发者体验**。

事实上，**SQLModel** 是位于 **Pydantic** 与 **SQLAlchemy** 之上的精简抽象层，经过严谨设计以确保与两者的深度无缝兼容。

## 环境要求

需要受官方支持的较新 [Python 版本](https://www.python.org/downloads/)。

由于 **SQLModel** 基于 **Pydantic** 和 **SQLAlchemy** 构建，因此需要这两个核心依赖项。在安装 SQLModel 时它们将被自动解析并安装。

## 安装指南

首先[安装 `uv`](https://docs.astral.sh/uv/getting-started/installation/)，然后在项目中引入 SQLModel：

<div class="termy">

```console
$ uv add sqlmodel
---> 100%
```

</div>

若偏好使用 `pip`，建议在虚拟环境中安装 `sqlmodel`。其他安装方式请参阅[安装指南](https://sqlmodel.tiangolo.com/install/)。

## 快速上手示例

如需了解数据库、SQL 及相关基础知识，请参阅 [SQLModel 官方教程](https://sqlmodel.tiangolo.com/databases/)。

以下为快速上手演示。✨

### 1. SQL 数据表

假设存在一个名为 `hero` 的 SQL 数据表，包含以下字段：

* `id`
* `name`
* `secret_name`
* `age`

期望表中包含如下记录：

| id | name | secret_name | age |
| :--- | :--- | :--- | :--- |
| 1  | Deadpond | Dive Wilson | null |
| 2  | Spider-Boy | Pedro Parqueador | null |
| 3  | Rusty-Man | Tommy Sharp | 48 |

### 2. 定义 SQLModel 模型

可以使用 **SQLModel** 按如下方式声明模型类：

```Python
from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
```

上述 `Hero` 类即为一个 **SQLModel** 模型，对应于 Python 代码中对 SQL 数据表的完整映射。

每个类属性均一一对应于数据表中的**列（Column）**。

### 3. 创建数据行记录

随后可将数据表的**每一行记录**创建为该模型的**对象实例**：

```Python
hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
```

通过这种方式，便可使用符合 Python 原生习惯的**类**与**实例**来表达**数据表**与**数据行**，进而实现与 **SQL 数据库**的顺畅通信。

### 4. 极致的编辑器支持

所有接口均经过精心考量，旨在带来最优质的开发体验与 IDE 编辑器支持。

涵盖**智能代码自动补全**：

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/autocompletion01.png">

以及**代码行内错误提示**：

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/inline-errors01.png">

### 5. 数据持久化写入数据库

通过阅读完整的**官方教程**可深入掌握 **SQLModel** 的各项高级功能；若想快速了解如何将上述模型整合并写入数据库，可参考以下代码：

```Python hl_lines="16  19  21-25"
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


engine = create_engine("sqlite:///database.db")


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
```

上述代码将在本地生成一个持久化保存有 3 位英雄记录的 **SQLite** 数据库文件。

### 6. 从数据库中查询数据

随后可编写查询语句从该数据库中检索数据，例如：

```Python hl_lines="13-17"
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


engine = create_engine("sqlite:///database.db")

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    hero = session.exec(statement).first()
    print(hero)
```

### 7. 全流程的类型与自动补全支持

**SQLModel** 经过深度打磨，**即使在从数据库执行查询提取数据后**，也能始终提供完整的类型推导与编辑器自动补全：

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/autocompletion02.png">

## 深度整合 SQLAlchemy 与 Pydantic

上述 `Hero` 类是一个 **SQLModel** 模型。

但与此同时，✨ 它本身就是一个标准的 **SQLAlchemy** 模型 ✨。因此，可以将其与其他原生的 SQLAlchemy 模型自由混用与组合，或将现有的 SQLAlchemy 应用平滑迁移至 **SQLModel**。

此外，✨ 它同时也是一个原生的 **Pydantic** 模型 ✨。可以通过类继承机制定义所有的**数据传输对象（DTO）模型**，完全杜绝重复代码。这使得与 **FastAPI** 的集成变得异常轻巧自然。

## 许可证 (License)

本项目遵循 [MIT 许可证](https://github.com/fastapi/sqlmodel/blob/main/LICENSE)条款授权发布。
