# ANRS: AI-Native Repo Spec

> 面向 AI 友好的代码仓库结构规范

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Native-Repo%20Spec-green.svg)]()

[English](README.md) | 中文

---

## ANRS 是什么？

ANRS (AI-Native Repo Spec) 是一个与厂商无关的规范，定义了如何结构化代码仓库，使 AI 代理能够在其中安全有效地工作。

当 AI 代理在传统代码库中工作时，它们经常会丢失当前任务的上下文、产生幻觉命令或修改无关文件。ANRS 通过提供一套标准的边界和上下文来解决这个问题：

- **显式状态 (`.anrs/state.json`)** — 替代脆弱的对话历史。AI 始终先读取此文件以了解"我在执行什么任务"以及"进行到哪一步"。
- **定义的技能 (`.anrs/skills/`)** — 替代开放式猜测。AI 被限制在已记录的清单中，防止未定义的行为。
- **强制质量门控 (`.anrs/harness/`)** — 替代盲目提交。AI 生成的代码在任务完成前必须通过检查和测试。

> **注意**：ANRS 是一个**规范**，而非运行时工具。它是一个标准化的文件夹结构 (`.anrs/`) 加上任何 AI 工具都可以遵循的执行协议。

---

## 设计原则

- **确定性执行** — AI 遵循固定循环：读取 → 计划 → 执行 → 验证。
- **原子性变更** — 代码和状态一起更新。始终可回滚。
- **厂商无关** — 适用于 Cursor、Claude、Codex 等。
- **分层验证** — 安全 → 代码检查 → 测试 → 风险评估。提交前把关。
- **从失败中学习** — 失败的尝试被归档以供未来参考。

---

## 架构概览

```
                    ANRS 框架

    状态 (SSOT)  →  编排器  →  技能
         ↑              |              |
         |              v              v
         |           质量门控  ←───  代码
         |              |
         |         [ 通过? ]
         |          /     \
         |        是       否
         |         |        |
         └── 提交       反思 → 重试
```

---

## 执行工作流

```
1. 读取状态    → .anrs/state.json
2. 加载计划    → .anrs/plans/active/{task_id}.md
3. 选择技能    → .anrs/skills/index.json
4. 执行        → 遵循 SKILL.md 清单
5. 运行质量门控 → L1 (静态) → L2 (测试) → L3 (稳定性)

通过 → 原子提交 → 更新状态 → 完成
失败 → 反思 → 重试 (最多3次) → 上报人工
```

---

## 快速开始

### 方案 1：使用 CLI（推荐）

```bash
pip install anrs
cd your-project
anrs init                    # 标准安装
anrs adapter install cursor  # 添加 AI 适配器
```

这会创建：
```
your-project/
├── .anrs/
│   ├── ENTRY.md      # AI 首先读取此文件
│   ├── state.json    # 当前状态 (唯一事实来源)
│   ├── config.json   # 配置
│   ├── scratchpad.md # 临时笔记
│   └── plans/        # 任务计划
│       ├── active/   # 当前任务
│       ├── backlog/  # 未来任务
│       └── templates/
└── .cursorrules      # AI 适配器
```

### 方案 2：探索源码

```bash
git clone https://github.com/artsyne/anrs.git
cd anrs
ls -la spec/      # 协议规范模板
ls -la cli/       # CLI 工具源码
```

### 方案 3：配置你的 AI 平台

ANRS 提供开箱即用的适配器，支持**多模式**（构建/计划/审查）：

| 平台 | 模式 | 快速开始 |
|------|------|----------|
| **Cursor** | build, plan | `anrs adapter install cursor` |
| **Claude Code** | build, plan, review | `anrs adapter install claude-code` |
| **Codex** | build, plan, review | `anrs adapter install codex` |
| **OpenCode** | build, plan, review | `anrs adapter install opencode` |

查看 [适配器文档](cli/src/anrs/data/adapters/README.md) 了解手动设置和模式切换。

---

## 核心概念

**状态 (SSOT)** — `.anrs/state.json` — 任务状态的唯一事实来源。AI 在执行任何操作前都会读取此文件。

**入口点** — `.anrs/ENTRY.md` — AI 代理的入口点。定义规则、约束和可用技能。

**技能** — `.anrs/skills/` — 注册的操作模板，包含输入/输出模式和约束。

**质量门控** — `.anrs/harness/quality_gate.py`（完整级别）或 `anrs harness` 命令 — 多层评估关卡（安全 → L1: 静态 → L2: 测试 → L3: 稳定性）。

---

## 关键文件参考

| 文件 | 描述 |
|------|------|
| `.anrs/ENTRY.md` | AI 代理入口点 |
| `.anrs/state.json` | 当前执行状态 |
| `.anrs/config.json` | 项目配置 |
| `.anrs/plans/active/` | 活跃任务计划 |
| `.anrs/harness/` | 质量门控评估器（完整级别） |

---

## 文档

- [快速开始](docs/getting-started.md) — 5 分钟快速上手
- [安装指南](docs/installation.md) — 安装选项（最小/标准/完整）
- [核心概念](docs/concepts/overview.md) — 架构和数据流
- [核心理念](spec/core-beliefs.md) — 设计原则
- [贡献指南](CONTRIBUTING.md) — 如何贡献

---

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。
