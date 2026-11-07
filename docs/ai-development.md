# Develop with AI

SQLModel includes an official **agent skill**, bundled with the Python package, with guidance for the version installed in your project.

## Install the skill

After [installing SQLModel](install.md), run [Library Skills](https://library-skills.io/use/) from your project directory:

```bash
uvx library-skills
```

Select the SQLModel skill and `.agents/skills` for Codex and most agents, or `.claude/skills` for Claude Code. You can select both.

Your agent can then use the skill automatically when working on SQLModel code.

### Install without prompts

For agents and scripts, select the SQLModel skill without interactive prompts:

```bash
uvx library-skills install --skill sqlmodel --yes
```

For Claude Code, add `--claude` to also install it in `.claude/skills`:

```bash
uvx library-skills install --skill sqlmodel --yes --claude
```
