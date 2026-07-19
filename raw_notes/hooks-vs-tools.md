# Hooks vs Tools 的本质区别

> 用大白话记一遍。

## 一句话区分

**hooks 的触发权在 harness（写代码的人），tools 的触发权在模型（LLM）。**

这才是本质区别，不是「固定流程 vs 选择性使用」--那个二分会误导。

## 对比表

| | Hooks | Tools |
|---|---|---|
| 谁决定触发 | harness，按事件触发（确定性） | 模型，自己决定调不调（概率性） |
| 模型知不知道 | 不知道（不进 tools 列表，对模型透明） | 知道（写在 tools schema 里，模型能选） |
| 触发时机 | 事件点：UserPromptSubmit / PreToolUse / PostToolUse / Stop | 模型 emit `tool_use` block 时 |
| 代码入口 | `trigger_hooks("PreToolUse", block)`，循环调用 | `TOOL_HANDLERS[block.name]`，循环按模型选的名字分发 |
| 目的 | 扩展 harness 行为（权限、日志、注入上下文） | 给模型提供能力（读文件、跑命令） |

## 编码思路是一样的（注册表模式）

两者本质都是「全局注册表 + register + 写具体方法」：

- hooks：`HOOKS` 字典，按**事件名**注册（`HOOKS["PreToolUse"].append(...)`），同一事件能挂多个回调。
- tools：`TOOL_HANDLERS` 字典，按**工具名**注册（`TOOL_HANDLERS["bash"] = ...`），一个名字一个 handler。

区别在注册的 key 和多了什么：

- hooks 的 key 是**事件名**，tools 的 key 是**工具名**。
- tools 比 hooks 多一样东西：**给模型看的 schema**（告诉模型「这工具叫什么、怎么用」）。
- hooks 不需要 schema，因为模型根本看不到它。

## 两者都能影响流程，但方式不同

区别不在「能不能影响流程」，而在**站在哪一边**：

- **hook**：PreToolUse 可以**拦截**（返回 blocked，工具就不执行）。这是 harness 在「审查」模型的行为。
- **tool**：模型调了工具，结果回到 messages，影响后续推理。这是模型在「使用」能力。

所以 hook 站 harness 这边管流程，tool 站模型这边干活。

## 为什么「固定 vs 选择性」会误导

- hooks 并不完全是「固定的」--它也可选、可配置（可以 `register_hook` 也可以不注册）。
- tools 也并非「随意选用」--模型不调工具就解不了题，某种意义上也不算「可选」。

所以这个二分不准，换成「**harness 触发 vs 模型触发**」就对上了。

## 配合 s04 README 的一句话

> "挂在循环上, 不写进循环里"

hook 是给 **harness 自己**用的扩展点，不该污染循环核心。循环应该是个稳定的核心，扩展挂在外面。

## 一句话总结

两者都是注册表模式，但：
- hooks 是 harness 给自己挂的扩展点（模型无感，按事件自动触发）。
- tools 是 harness 暴露给模型的能力（模型主动选，需要 schema）。
