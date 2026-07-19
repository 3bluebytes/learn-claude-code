# thinking / reasoning 是什么，为什么要回传

> 用大白话记一遍，不堆术语。

## reasoning 到底是什么

不是什么单独的「推理引擎」。它就是 **transformer 在已有上下文上继续往后生成 token**，和最终答案走的是同一条自回归路径。区别只在于：

- **训练层面**：模型被训出来「先吐一段草稿，再给答案」。
- **API 层面**：把那段草稿 token 打上 `thinking` / `reasoning` 标签，方便单独算预算、展示、回传。

所以本质上，thinking 就是「模型脑子里的草稿区」，不是另一个模块。

## 两家的区别

| | OpenAI（o 系列） | Anthropic（extended thinking） |
|---|---|---|
| 长什么样 | reasoning tokens，默认**不可见**，黑盒 | `thinking` block，明文，和 text/tool_use 平级 |
| 下一轮还留着吗 | Chat Completions 里**直接丢**（重新想）；Responses API 里能回传一个**加密**的版本 | 需要你**把 thinking block 原样回传**，带签名 |
| 你能控什么 | `reasoning_effort: low/medium/high` | `thinking: { budget_tokens: N }` |

一句话：OpenAI 默认把推理当一次性副产品；Anthropic 把推理当对话状态的一部分。

## 为什么 agentic loop 要回传 thinking

transformer **跨请求是无状态的**。一次调用结束，除了你下次请求里重新塞进去的 token，啥都不留。attention 每一步都重新读全部 token。

所以「回传 thinking」字面意思就是：**把那段草稿 token 再放进下一次请求，让 attention 能重新读到它。**

不回传会怎样？模型在 turn 2 只看到「我调了某个工具、拿到某个结果」，但看不到**当初为什么这么决定**。回传了，它能接着自己之前的思路走。这就是「推理是对话状态的一部分」的机械解释。

## 回传是为了 KV cache 吗

**主要是为了别的，KV cache 是顺带的好处。** 别把因果搞反了。

真正的原因是**推理连贯 + 保真**：

- 连贯：让 attention 能读到上一段推理。
- 保真：Anthropic 的 thinking block **带签名**，要求**原样、不改**地回传。如果是为了省算力，塞任何相同 token 都行，不会非得是 thinking 且签名一致。这个硬要求本身就说明：驱动因素是「保证模型续写的是自己真实的上一段推理，不是被伪造/编辑过的」。

顺带的好处：Anthropic 有 **prompt caching**（`cache_control`），相同前缀的 KV 能在服务端缓存复用。thinking 被回传、又落在可缓存前缀里，确实能命中缓存、省重算。但这是「已经回传相同 token 之后」搭便车触发的，不是回传的理由。

因果顺序：

- ❌ 「为了省 KV 才回传」
- ✅ 「为了连贯+保真必须回传相同 token → 顺带让 prompt cache 命中」

## 和 s05 的 todo 不是一回事

容易混，但完全是两层东西：

- **thinking / reasoning**：**模型层**，模型脑子里自发的草稿，隐式、易丢。
- **todo (TodoWrite)**：**harness 层**，让模型**主动调工具**把计划写成一张清单，明文、持久、每轮可重新注入。s05 还做了「连续 3 轮没更新就 reminder」的机制。

各自解决的问题：

- thinking 解决「每一步想得对不对」。
- todo 解决「长任务里不忘事、不偏题」（上下文一长，系统提示被稀释，模型做完前几步就开始即兴发挥）。

两者互补：开 thinking 但没 todo，长任务照样跑偏；没 thinking 但有 todo，照样能靠外化计划扛长任务（s05 就是这么演示的，没开 thinking）。

## 一句话总结

- reasoning ＝ transformer 在上下文上继续生成，划成草稿区而已。
- 回传 thinking ＝ 把那段 token 重新喂回去给 attention 读，保连贯 + 用签名保真；KV cache 复用是搭便车的副作用，不是动机。

## 确定性边界

- 对外公开文档（签名、redacted_thinking、tool-use 多轮要回传 thinking）有把握。
- 服务端 KV 的精确内部实现是 Anthropic 的事，KV 那部分是基于 transformer 机制 + API 约束的合理推断。
