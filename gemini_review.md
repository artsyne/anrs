# AHES (AI Harness Engineering Standard) 项目评审报告

**评审人**: Gemini 3.1 Pro Preview (AI Native Code Assistant)
**版本**: 0.1.0 (Round 9 优化后评审)
**评审日期**: 2026-03-25

---

## 📝 执行摘要 (Executive Summary)

AHES 项目在“**AI 原生代码库规约 (AI Native Repo Spec)**”这一前沿领域进行了极具开创性的探索。它跳出了传统 AI 辅助编程工具（如 OpenAI SDK、LangChain、各种 IDE 插件）的范畴，不再试图去“教” AI 怎么写代码，而是从代码库 (Repository) 侧建立起一套**强制性的流水线规则与状态约束**。

通过本次 Round 9 优化（Schema 一致性、AI 文档标准化、Harness 安全集成、Plans 目录优化等），项目已经形成了一个高度闭环的机器友好型架构。它通过 `state.json` (SSOT)、`Plans` (无头看板)、`Harness` (质量门禁) 以及 `Evals` (自修复经验池)，有效地解决了大模型在复杂任务中常见的“上下文漂移”、“幻觉”和“破坏性修改”等痛点。

---

## 🔍 核心维度评审

### 1. AI Native 资产与设计 (评分: 9.5/10)
本项目最出彩的地方在于打破了传统 Repo 的文件组织习惯，将目录彻底转变为“机器的上下文插件”。

- **Docs (机器友好的知识库)**：突破了传统面向人类的文档形式，`docs/core-beliefs.md` 等文件用高度精炼的指令为 AI 设定了不可逾越的边界（如 `Determinism Over Creativity`）。
- **Plans (无外设看板 - Headless Kanban)**：`plans/` 目录完美实现了 AI 原生看板。结合 `task-template.md`，这让 AI 仅靠文件读写就能实现任务抓取、推进与归档，将“执行器”升级为了“自驱动的智能体”。
- **Evals (AI 闭环进化系统)**：`evals/failure-cases/` 本质上是一个 **AI 专属的 Debug 经验池**。系统在 Harness 门禁中失败后，可在此沉淀失败上下文，使整个系统具备了自我反思和积累 Debug 经验的能力。
- **YAML Frontmatter 规范**：所有面向 AI 的 Markdown 文件都包含标准的 `name` 和 `description`，并通过 `Read when:` 给出了精确的触发条件，极大提升了 AI 意图识别的准确性，防止信息过载。

### 2. 执行协议与流程 (评分: 9/10)
- **协议闭环**：`Read → Plan → Execute → Verify` 的环路逻辑非常严密。通过 `ORCHESTRATOR.md`，执行的每一步都有对应的输入输出约束，确保了极高的确定性。
- **Harness 级联拦截机制**：采用 `Security 优先 (Cross-level) → L1 → L2 → L3` 级联设计，完美融合了 DevSecOps 理念，避免了恶意代码或存在严重漏洞的代码被提交。
- **失败反射机制**：强制要求在失败时调用 `reflection` 并写入 `SCRATCHPAD`，再通过 error_codes 分析，杜绝了大模型常见的“无脑重试死循环”。

### 3. 契约 (Contracts) 与 Schema (评分: 9/10)
- **定义严谨性**：`ai/contracts/` 下的 JSON Schema (Draft-07) 配合 CI 流程，实现了对 `state.json` 和 `skills/index.json` 的自动化硬性校验。
- **SSOT 状态管理**：`state.json` 实体化了 AI 的思维状态。其 `extensions` 字段提供了良好的厂商/插件 Namespace 扩展机制，兼顾了规范与灵活性。
- **任务命名规范**：统一采用正则表达式 `^[a-z]+-\\d{3,}$`，便于后续的日志解析和溯源。

### 4. 厂商适配与跨平台 (评分: 8.5/10)
- **降维打击式接管**：对 Cursor、Claude Code 等主流工具，通过原生配置文件（如 `.cursorrules`、`CLAUDE.md`）进行无缝接管，统一注入“必须读 state.json”、“不跳过 Harness”的底线原则。
- **多模式支持**：适配器提供了 `build`, `plan`, `review` 模式，贴合了软件生命周期的不同阶段。

### 5. 开源治理与业界标准对比 (评分: 9/10)
- **工程化治理**：完善的 `.github/workflows/ci.yml` 实现了文档与契约的自动化守护；标准的 `CONTRIBUTING.md` 明确了 Skill 和 Evaluator 的扩展路径。
- **与 `obra/superpowers` 的对比分析**：
  - **不重复且高度互补**。`superpowers` 是 **AI Agent 侧的增强工具**（教 AI 如何运用 TDD、如何拆解任务），而 AHES 是 **Repo 侧的治理规约**（约束任何进入该 Repo 的 AI 必须遵守底线规则）。
  - **结合潜力巨大**：如果让一个安装了 `superpowers` 的强力 AI，在一个遵循 AHES 规范的 Repo 中工作，那就是“最强的大脑（高超编码技巧）”加上“最严的工厂（绝对的安全门禁与状态溯源）”，能产生 1+1>2 的效果。

---

## 🎯 亮点总结 (Highlights)

1. **面向 AI 的 SSOT (Single Source of Truth)**：彻底解决了长上下文对话带来的状态丢失问题。
2. **Headless Kanban 与闭环进化**：`Plans` 与 `Evals` 使得 Repo 自身成为一个具备任务编排与错误自愈能力的生命体。
3. **物理隔离的质量门禁**：Harness 脱离了单纯的 Prompt 约束，用真实的脚本当裁判，极大地提高了代码可靠性。

---

## 🛠 存在的问题 (Areas for Improvement)

1. **P1 - Evaluator 的骨架化**：目前 `harness/quality_gate.py` 中的验证依然是 Placeholder。缺乏与真实工具（如 `pytest`, `eslint`, `bandit`）对接的参考实现，导致验证环节停留在概念阶段。
2. **P1 - Subagent 并发隔离策略缺失**：`dispatch-subagent` 描述了并行能力，但在面对多个子任务并发读写同一文件或 `state.json` 时，缺乏明确的架构约束。
3. **P2 - Failure Case 自动化归档链路断层**：虽然 `evals/failure-cases` 设计极佳，但目前 `reflection` skill 失败时，没有强制的自动化链路将其转译并归档为标准的 Failure Case Markdown。

---

## 💡 优化建议 (Actionable Recommendations)

1. **引入真实 Harness 插件示例**：在 `examples/` 目录下，提供一个真实可运行的例子（例如：集成 `pre-commit` hook、`bandit` 扫码或 `pytest` 跑测的 Python Demo），让开发者看到非骨架的实际拦截效果。
2. **Subagent 隔离与无状态化 (Map-Reduce 架构)**：
   - **不要引入文件锁 (File Lock)**，因为这会造成 AI 严重的认知过载和死锁问题，违背 `Simplicity > Cleverness`。
   - 建议在 `dispatch-subagent` 协议中采用 **Shared-Nothing (隔离) 架构**（类似 Git Worktrees 隔离）。规定 Subagents **绝对禁止**修改全局 `state.json`。它们只负责在隔离区执行任务并返回结果，由 Orchestrator（主 Agent）统一进行结果合并与状态更新。
3. **闭环自动化 Reflection -> Evals**：更新 `reflection` skill 的 checklist，增加强制性步骤：当遇到无法恢复的错误或达到最大 Retry 次数时，必须自动生成一份遵循 `evals/failure-cases/README.md` 模板的 Postmortem 报告并存入，形成知识沉淀。
4. **引入 LLM as a Judge (L3 层)**：在 `L3 (Stability/Risk Analysis)` 层，建议提供一段标准的 Risk Analysis 提示词模板，直接集成 LLM API 进行风险打分，实现真正的 AI-driven Risk Analysis。