# AHES 项目 Review 请求 (Round 7)

> **版本**: 0.1.0  
> **上轮优化**: 2026-03-24  
> **已完成优化**: Schema 一致性、AI 文档标准化、Harness 安全集成、Subagent 并行、AI 友好性全面优化、Adapters 多模式支持、Codex CLI 适配

## 项目定位

AHES (AI Harness Engineering Standard) 是一个 **AI Native Repo Spec**，定义 AI Agent 与代码库协作的标准协议。

**核心理念**：
- 定义 AI Agent 与代码库协作的标准协议
- 通过 State（SSOT）+ Skills（白名单）+ Harness（质量门禁）约束 AI 行为
- 厂商中立，支持 Cursor、Claude、OpenAI 等多种 AI 平台
- 确定性执行：Read State → Plan → Execute → Verify → Commit/Retry

**重要说明**：
1. `harness/evaluators/` 下的评估器是 **协议骨架**，展示预期接口
2. `examples/` 中的代码 **故意未完成**，是让 AI 按协议完成任务的练习场景
3. 核心价值在于 **规范定义**（ai/、contracts/、skills/）
4. **项目内容默认面向 AI 消费**，只有少量文件（README.md 等）面向人类阅读

## 上轮已优化项 (Round 6)

| 优化项 | 状态 |
|--------|------|
| 将 adapters/openai/ 重命名为 adapters/codex/ | ✅ 已完成 |
| 新增 Codex CLI AGENTS.md 配置格式 | ✅ 已完成 |
| 新增 codex/modes/ (build, plan, review) | ✅ 已完成 |
| 更新 adapters/README.md 为 Codex CLI | ✅ 已完成 |
| 更新 README.md Quick Start 为 Codex | ✅ 已完成 |

## 上轮已优化项 (Round 5)

| 优化项 | 状态 |
|--------|------|
| 删除根目录 src/ （AHES 是规范框架，不需要业务代码目录） | ✅ 已完成 |
| 删除空目录 adapters/openclaw/, opencode/ | ✅ 已完成 |
| 新增 OpenCode 适配器 (opencode.json + 3 agents) | ✅ 已完成 |
| Claude 适配器增强 (README + projects/*.md) | ✅ 已完成 |
| Cursor 适配器增强 (README + modes/*) | ✅ 已完成 |
| OpenAI 适配器增强 (README + assistants/*.json) | ✅ 已完成 |
| adapters/README.md 更新为多模式对比表 | ✅ 已完成 |
| README.md Quick Start 添加 adapters 多模式说明 | ✅ 已完成 |

## 上轮已优化项 (Round 4)

| 优化项 | 状态 |
|--------|------|
| docs/references/ 转换为 Markdown + YAML frontmatter | ✅ 已完成 |
| 空目录添加 README.md (docs/design-docs, generated, plans/completed) | ✅ 已完成 |
| evals/ 下 3 个子目录添加 README.md | ✅ 已完成 |
| ENTRY.md Key Files 表格扩展 (6 个关键文件) | ✅ 已完成 |
| README.md Directory Structure 完善 | ✅ 已完成 |
| README.md Documentation 链接补全 | ✅ 已完成 |
| ORCHESTRATOR.md 步骤编号重构为三阶段 | ✅ 已完成 |

## Round 3 已优化项

| 优化项 | 状态 |
|--------|------|
| 新增 dispatch-subagent 技能（并行任务执行） | ✅ 已完成 |
| Orchestrator 支持并行执行模式 | ✅ 已完成 |
| 技能注册表更新至 15 个技能 | ✅ 已完成 |
| CSO (Claude Search Optimization) 审查 | ✅ 已完成 |

## Round 2 已优化项

| 优化项 | 状态 |
|--------|------|
| AI 消费文档标准化 (35 个文件添加 YAML frontmatter) | ✅ 已完成 |
| Harness 安全扫描集成 (security_scan 集成到执行流程) | ✅ 已完成 |
| 添加 harness/README.md 架构文档 | ✅ 已完成 |
| 修复 ai/ENTRY.md 表格格式错误 | ✅ 已完成 |
| 移除所有 AI 消费文档中的 emoji | ✅ 已完成 |
| 添加 adapters/openai/system-prompt.txt | ✅ 已完成 |
| 示例项目 state.json 添加 $schema 引用 | ✅ 已完成 |
| 删除空目录 generate-fmea-report | ✅ 已完成 |

## 历史优化 (Round 1)

| 优化项 | 状态 |
|--------|------|
| 创建 `skill_registry.schema.json` | ✅ 已完成 |
| 统一 Task ID 命名规则 `^[a-z]+-\d{3,}$` | ✅ 已完成 |
| State Schema 添加 `extensions` 扩展字段 | ✅ 已完成 |
| CI 增强：校验 registry + 目录一致性 | ✅ 已完成 |
| 创建 `plan.schema.json` | ✅ 已完成 |
| `error_codes.json` 添加 E6xx 环境错误 | ✅ 已完成 |
| 所有 SKILL.md 标准化 (YAML frontmatter) | ✅ 已完成 |

## 项目结构

```
AHES/
├── ai/                      # 核心规范层 (AI 消费)
│   ├── ENTRY.md             # AI Agent 入口点 (含协议版本)
│   ├── state/               # 状态管理 (SSOT)
│   ├── skills/              # 技能注册表与定义 (15 个标准化 SKILL.md)
│   ├── orchestrator/       # 执行协议 (含并行/串行模式)
│   ├── rules/               # 约束规则
│   ├── contracts/           # JSON Schema 契约
│   └── agents/              # Agent 定义
├── harness/                 # 评估系统 (含 Security 扫描)
│   ├── evaluators/          # L1/L2/L3 + Security 评估器
│   ├── quality_gate.py      # 质量门禁入口
│   ├── README.md            # Harness 架构文档
│   └── error_codes.json     # 错误码定义
├── adapters/                # 厂商适配器 (claude/cursor/openai)
├── examples/                # 示例项目 (含完整 state.json)
├── docs/                    # 架构文档 (AI 消费)
├── scripts/                 # 工具脚本
└── plans/                   # 任务管理 (AI 消费)
```

## Review 请求

请从以下维度评审这个项目：

### 1. AI Native 设计评审
- **项目默认面向 AI 消费** 的定位是否清晰
- AI 消费文档的 YAML frontmatter 格式是否有效
- 文档触发条件描述是否准确有用

### 2. 执行流程评审
- 执行协议（Read → Plan → Execute → Verify）的完整性
- Harness 执行流程（Security → L1 → L2 → L3）的设计
- 失败反射和重试机制的合理性

### 3. 契约与 Schema 评审
- `ai/contracts/` 下 JSON Schema 的定义完整性
- State Schema 的 `extensions` 扩展机制
- Task ID 统一命名规则的合理性

### 4. 厂商适配评审
- `adapters/` 下各厂商适配器的完整性
- System prompt 的一致性和有效性
- 跨厂商协议兼容性

### 5. 开源治理评审
- CI/CD 配置的完整性
- 社区治理文件完整性（CoC、Security、Contributing）
- 文档结构与可发现性

### 6. 与业界标准对比
- 与 OpenAI Agents SDK、LangChain、AutoGPT 等框架的设计差异
- 是否有可借鉴的业界最佳实践
- 规范的可采纳性和推广潜力

## 期望输出

1. **评分**：对各维度给出 1-10 分评价
2. **上轮改进评估**：评估 Round 2 优化的效果
3. **亮点**：项目做得好的地方
4. **问题**：需要改进的具体问题（标注优先级：P0/P1/P2）
5. **建议**：基于业界最佳实践的具体优化方案

---

**请先阅读以下核心文件，然后进行 review：**

1. `README.md` - 项目概述
2. `ai/ENTRY.md` - AI 入口协议（含版本号和规范语义）
3. `ai/orchestrator/ORCHESTRATOR.md` - 执行协议
4. `ai/state/state.schema.json` - 状态 Schema
5. `ai/contracts/skill_registry.schema.json` - 技能注册表 Schema
6. `ai/skills/index.json` - 技能注册表
7. `harness/README.md` - Harness 架构文档
8. `harness/quality_gate.py` - 质量门禁（含 Security 扫描）
9. `adapters/claude/system-prompt.txt` - Claude 适配器
10. `adapters/openai/system-prompt.txt` - OpenAI 适配器
