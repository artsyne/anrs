# AHES 项目 Review 请求 (Round 2)

> **版本**: 0.1.0  
> **上轮优化**: 2026-03-24  
> **已完成优化**: Schema 一致性修复、扩展性增强、CI 增强、规范语义

## 项目定位

AHES (AI Harness Engineering Standard) 是一个 **AI 协同研发标准规范框架**，不是一个可执行的产品代码库。

**核心理念**：
- 定义 AI Agent 与代码库协作的标准协议
- 通过 State（SSOT）+ Skills（白名单）+ Harness（质量门禁）约束 AI 行为
- 厂商中立，支持 Cursor、Claude、OpenAI 等多种 AI 平台
- 确定性执行：Read State → Plan → Execute → Verify → Commit/Retry

**重要说明**：
1. `harness/evaluators/` 下的评估器是 **协议骨架**，展示预期接口，不是要交付的产品代码
2. `examples/` 中的代码 **故意未完成**，是让 AI 按协议完成任务的练习场景
3. 核心价值在于 **规范定义**（ai/、contracts/、skills/），不在于代码执行能力

## 上轮已优化项

| 优化项 | 状态 |
|--------|------|
| 创建 `skill_registry.schema.json` | ✅ 已完成 |
| 统一 Task ID 命名规则 `^[a-z]+-\d{3,}$` | ✅ 已完成 |
| State Schema 添加 `extensions` 扩展字段 | ✅ 已完成 |
| CI 增强：校验 registry + 目录一致性 | ✅ 已完成 |
| ENTRY.md 添加版本号和 MUST/SHOULD/MAY | ✅ 已完成 |
| 创建 `plan.schema.json` | ✅ 已完成 |
| `error_codes.json` 添加 E6xx 环境错误 | ✅ 已完成 |
| 所有 SKILL.md 标准化 (YAML frontmatter) | ✅ 已完成 |

## 项目结构

```
AHES/
├── ai/                      # 核心规范层
│   ├── ENTRY.md             # AI Agent 入口点 (含协议版本)
│   ├── state/               # 状态管理 (SSOT，支持 extensions)
│   ├── skills/              # 技能注册表与定义 (标准化 SKILL.md)
│   ├── orchestrator/        # 执行协议
│   ├── rules/               # 约束规则
│   ├── contracts/           # JSON Schema 契约 (新增 skill_registry、plan)
│   └── agents/              # Agent 定义
├── harness/                 # 评估系统（协议骨架）
│   ├── evaluators/          # L1/L2/L3 评估器
│   ├── quality_gate.py      # 质量门禁入口
│   └── error_codes.json     # 错误码定义 (含 E6xx 环境错误)
├── adapters/                # 厂商适配器
├── examples/                # 示例项目
├── docs/                    # 架构文档
├── scripts/                 # 工具脚本
└── plans/                   # 任务管理
```

## Review 请求

请从以下维度评审这个项目，**重点关注上轮优化后的改进效果**：

### 1. 规范设计评审
- 执行协议（Read → Plan → Execute → Verify）的完整性和可行性
- State 管理模型（SSOT）的设计合理性，`extensions` 扩展机制是否合理
- Skills 系统的扩展性和约束能力
- Harness 分层评估（L1/L2/L3）的设计

### 2. 契约与 Schema 评审
- `ai/contracts/` 下 JSON Schema 的定义完整性
- **新增** `skill_registry.schema.json` 和 `plan.schema.json` 的设计
- Task ID 统一命名规则的合理性
- `additionalProperties` 与 `extensions` 的扩展策略

### 3. 协议表达评审
- `ai/ENTRY.md` 的版本号和规范语义（MUST/SHOULD/MAY）
- `ai/orchestrator/ORCHESTRATOR.md` 的协议表达
- Skills SKILL.md 的 YAML frontmatter 标准化效果

### 4. 开源治理评审
- CI/CD 配置的增强效果（registry 校验、目录一致性检查）
- 社区治理文件完整性（CoC、Security、Contributing）
- 文档结构与可发现性

### 5. 与业界标准对比
- 与 OpenAI Agents SDK、LangChain、AutoGPT 等框架的设计差异
- 是否有可借鉴的业界最佳实践
- 规范的可采纳性和推广潜力

## 期望输出

1. **评分**：对各维度给出 1-10 分评价
2. **上轮改进评估**：评估上轮优化的效果
3. **亮点**：项目做得好的地方
4. **问题**：需要改进的具体问题（标注优先级：P0/P1/P2）
5. **建议**：基于业界最佳实践的具体优化方案

---

**请先阅读以下核心文件，然后进行 review：**

1. `README.md` - 项目概述
2. `ai/ENTRY.md` - AI 入口协议（含版本号和规范语义）
3. `ai/orchestrator/ORCHESTRATOR.md` - 执行协议
4. `ai/state/state.schema.json` - 状态 Schema（含 extensions）
5. `ai/contracts/skill_registry.schema.json` - **新增** 技能注册表 Schema
6. `ai/contracts/plan.schema.json` - **新增** 计划 Schema
7. `ai/skills/index.json` - 技能注册表
8. `harness/error_codes.json` - 错误码定义（含 E6xx）
9. `.github/workflows/ci.yml` - CI 配置（增强版）
