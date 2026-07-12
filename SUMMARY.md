# Project Summary: Learn Claude Code

> Generated from `README.md` and `requirements.txt`

---

## Overview

**Learn Claude Code** is a hands-on, 20-lesson tutorial repository that teaches
**harness engineering** for AI agents. The central idea:

> **Agency comes from the model. An agent product = Model + Harness.**
> The model is the driver. The harness is the vehicle.

The repository pushes back against no-code "AI Agent" platforms and prompt-chaining
libraries that try to substitute procedural logic for intelligence. Instead, it teaches
you to build the operational environment — tools, knowledge, context management,
permissions — that lets a trained model express its intelligence effectively.

---

## Core Philosophy

- **Agency is trained, not coded.** Models like Claude gain their ability to perceive,
  reason, and act through training (RL, fine-tuning, RLHF), not through orchestration code.
- **The harness is your job.** Most engineers are not training models; they are building
  the world the model operates in.
- **The agent loop never changes.** Every lesson layers one mechanism on top of the same
  fundamental loop:

  ```
  User → messages[] → LLM → response
                                |
                      stop_reason == "tool_use"?
                     /                          \
                   yes                           no
                    |                             |
              execute tools                    return text
              append results
              loop back ───────────────→ messages[]
  ```

---

## What a Harness Includes

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions
```

| Component       | Examples                                           |
|-----------------|----------------------------------------------------|
| Tools           | File I/O, shell, network, database, browser        |
| Knowledge       | Product docs, API specs, style guides              |
| Observation     | git diff, error logs, browser state                |
| Action          | CLI commands, API calls, UI interactions           |
| Permissions     | Sandbox isolation, approval workflows, trust bounds|

---

## 20 Progressive Lessons

Each lesson adds one harness mechanism. The learning path follows six stages:

| Stage | Lessons     | Focus                                      |
|-------|-------------|--------------------------------------------|
| 1     | s01–s04     | Core capabilities: agent loop, tools, permissions, hooks |
| 2     | s05–s06, s08| Handle complex work: planning, subagents, context compaction |
| 3     | s09–s11     | Remember & recover: memory, system prompt, error recovery |
| 4     | s12–s14     | Long-running tasks: task system, background tasks, cron |
| 5     | s15–s18     | Multi-agent coordination: teams, protocols, autonomy, worktree isolation |
| 6     | s07, s19–s20| Extend & assemble: skill loading, MCP plugins, comprehensive agent |

### Full Chapter List

| Chapter | Topic                 | Key Concepts                                      |
|---------|-----------------------|---------------------------------------------------|
| s01     | Agent Loop            | `messages` / `while True` / `stop_reason`         |
| s02     | Tool Use              | `TOOL_HANDLERS` / dispatch map / concurrency      |
| s03     | Permission System     | `PermissionRule` / approval pipeline              |
| s04     | Hook System           | `PreToolUse` / `PostToolUse` / extension points   |
| s05     | TodoWrite             | `TodoItem` / plan-then-execute                    |
| s06     | Subagent              | `fresh messages[]` / context isolation            |
| s07     | Skill Loading         | `SkillManifest` / on-demand injection             |
| s08     | Context Compact       | snipCompact / microCompact / autoCompact          |
| s09     | Memory System         | selection / extraction / consolidation            |
| s10     | System Prompt         | runtime assembly / section concatenation          |
| s11     | Error Recovery        | token escalation / fallback model / retry         |
| s12     | Task System           | `TaskRecord` / `blockedBy` / disk persistence     |
| s13     | Background Tasks      | threaded execution / notification queue           |
| s14     | Cron Scheduler        | durable scheduling / session-scoped triggers      |
| s15     | Agent Teams           | `MessageBus` / inbox / permission bubbling        |
| s16     | Team Protocols        | shutdown handshake / plan approval                |
| s17     | Autonomous Agents     | idle cycle / auto-claim / self-organization       |
| s18     | Worktree Isolation    | `WorktreeRecord` / task-directory binding         |
| s19     | MCP Plugin            | multi-transport / channel routing / tool pool     |
| s20     | Comprehensive Agent   | all mechanisms around one loop                    |

---

## Dependencies (from `requirements.txt`)

| Package            | Minimum Version | Purpose                                      |
|--------------------|-----------------|----------------------------------------------|
| `anthropic`        | >= 0.25.0       | Anthropic API client — powers the LLM calls in the agent loop |
| `python-dotenv`    | >= 1.0.0        | Loads `.env` file for `ANTHROPIC_API_KEY` configuration      |
| `pyyaml`           | >= 6.0          | YAML parsing for skill manifests, configs, etc.              |

---

## Quick Start

```sh
git clone https://github.com/shareAI-lab/learn-claude-code
cd learn-claude-code
pip install -r requirements.txt
cp .env.example .env          # set ANTHROPIC_API_KEY

python s01_agent_loop/code.py      # Start: one loop + bash
python s08_context_compact/code.py # Context compaction
python s20_comprehensive/code.py   # All mechanisms in one loop
```

---

## Repository Structure

```
learn-claude-code/
  s01_agent_loop/ ... s20_comprehensive/  # 20 lesson folders
    README.md / README.en.md / README.ja.md  # Multilingual narratives
    code.py               # Standalone runnable implementation
    images/               # SVG diagrams
  agents/                 # Legacy 12-lesson runnable code
  skills/                 # Skill files used by s07
  docs/                   # Legacy 12-lesson documentation
  web/                    # Web platform (renders legacy track)
  tests/
  requirements.txt
```

---

## Version Status

- **Current track:** Root-level `s01`–`s20` (the canonical 20-lesson version).
- **Legacy track:** `docs/`, `agents/`, and `web/` preserve the older 12-lesson version
  for existing readers and links. Chapter numbers do not match across tracks.

---

## Related Projects

| Project | Description |
|---------|-------------|
| [Kode Agent CLI](https://github.com/shareAI-lab/Kode-CLI) | Open-source coding agent CLI with skill/LSP support, works with GLM, MiniMax, DeepSeek |
| [Kode Agent SDK](https://github.com/shareAI-lab/kode-agent-sdk) | Embed agent capabilities in your own application |
| [claw0](https://github.com/shareAI-lab/claw0) | Sister tutorial: always-on harness (heartbeat, cron, IM channels, memory, Soul) |

---

## License

MIT

---

> **Build the harness well. The model will do the rest.**
