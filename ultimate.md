# ANRS 目录结构终极方案

> **目标**：清晰界定"开源仓库"与"用户仓库"的边界，规划 CLI 与插件生态，明确区分"人类消费"与"机器消费"内容。
> **核心原则**：开源仓库是"工厂"，用户安装的是"产品"。

---

## 1. 消费对象划分

**两分法原则**：同一目录不应同时包含"人类消费"和"机器消费"内容。

| 类型 | 受众 | 内容特征 | 示例 |
|------|------|----------|------|
| **人类消费** | 开发者、架构师 | 概念说明、安装指南、设计理念 | `docs/`, `README.md` |
| **机器消费** | AI Agent、脚本 | 协议文档、Schema、执行代码 | `spec/`, `harness/`, `contracts/` |

> **注**：机器消费包含两种形式：
> - **AI 读取**：ENTRY.md, state.json, SKILL.md（指导 AI 行为）
> - **脚本执行**：quality_gate.py, CLI 代码（系统直接运行）

---

## 2. 开源仓库结构（Source Repo）

```
anrs/                              # 开源仓库根目录
│
├── spec/                          # [机器] 📜 核心规范（原 ai/，重命名）
│   ├── ENTRY.md                   # [AI] 入口协议
│   ├── core-beliefs.md            # [AI] 核心理念（从 docs/ 移入）
│   ├── state/
│   │   ├── state.schema.json      # [机器] 状态 Schema
│   │   ├── state.template.json    # [机器] 初始状态模板
│   │   ├── scratchpad/
│   │   └── README.md
│   ├── orchestrator/
│   │   ├── ORCHESTRATOR.md        # [AI] 执行协议
│   │   └── strategies/
│   ├── skills/
│   │   ├── index.json             # [机器] 技能注册表
│   │   ├── core/                  # [AI] 核心技能
│   │   ├── engineering/           # [AI] 工程技能
│   │   ├── sre/                   # [AI] SRE 技能
│   │   └── env/                   # [AI] 环境技能
│   ├── contracts/                 # [机器] JSON Schema 契约
│   │   ├── api.schema.json
│   │   ├── plan.schema.json
│   │   ├── task.schema.json
│   │   └── ...
│   ├── rules/
│   │   ├── global.md              # [AI] 全局规则
│   │   ├── coding.md              # [AI] 编码规范
│   │   ├── safety.md              # [AI] 安全规则
│   │   └── constraints.json       # [机器] 机器可读约束
│   └── agents/
│       ├── AGENTS.md
│       └── default.md
│
├── harness/                       # [机器] 🔍 质量门控系统
│   ├── evaluators/
│   │   ├── l1_static_checks.py    # [脚本] L1 静态检查
│   │   ├── l2_dynamic_tests.py    # [脚本] L2 动态测试
│   │   ├── l3_stability.py        # [脚本] L3 稳定性审计
│   │   └── security_scan.py       # [脚本] 安全扫描
│   ├── metrics/
│   ├── reports/
│   ├── quality_gate.py            # [脚本] 主入口
│   ├── error_codes.json           # [机器] 错误码定义
│   └── README.md                  # [人类] 使用说明
│
├── templates/                     # [机器] 📋 安装模板（配置驱动）
│   ├── files/                     # 模板文件池（单一来源，去重）
│   │   ├── ENTRY.md
│   │   ├── config.json
│   │   ├── state.template.json
│   │   ├── scratchpad.md
│   │   ├── plans/
│   │   │   ├── active.README.md
│   │   │   ├── backlog.README.md
│   │   │   └── task-template.md
│   │   ├── skills/
│   │   │   └── index.template.json
│   │   └── failure-cases/
│   │       └── README.md
│   └── manifests/                 # 安装清单
│       ├── minimal.json           # Level 0：仅 ENTRY + state
│       ├── standard.json          # Level 1：+ plans + scratchpad
│       └── full.json              # Level 2：+ skills + failure-cases + harness
│
├── adapters/                      # [人类] 🔌 适配器模板库
│   ├── cursor/
│   │   ├── .cursorrules           # 跳板模板
│   │   ├── modes/
│   │   └── README.md
│   ├── claude-code/
│   │   ├── CLAUDE.md              # 跳板模板
│   │   ├── modes/
│   │   └── README.md
│   ├── codex/
│   └── opencode/
│
├── cli/                           # [机器] 🛠️ CLI 工具（Python）
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                # 入口 (anrs)
│   │   ├── init.py                # anrs init
│   │   ├── harness.py             # anrs harness
│   │   ├── adapter.py             # anrs adapter
│   │   ├── status.py              # anrs status
│   │   └── upgrade.py             # anrs upgrade
│   ├── tests/
│   ├── pyproject.toml
│   ├── requirements.txt           # 依赖（从根目录迁移）
│   └── README.md
│
├── ext/                           # [人类] 🧩 IDE 插件源码
│   ├── vscode/
│   │   ├── src/
│   │   ├── package.json
│   │   └── README.md
│   └── jetbrains/
│       ├── src/
│       └── README.md
│
├── docs/                          # [人类] 📚 文档（纯人类消费）
│   ├── README.md                  # 文档索引
│   ├── getting-started.md         # 快速开始
│   ├── installation.md            # 安装指南
│   ├── migration.md               # 迁移指南
│   ├── concepts/                  # 概念说明
│   │   ├── overview.md            # 整体架构
│   │   ├── state.md               # 状态管理
│   │   ├── skills.md              # 技能系统
│   │   ├── harness.md             # 质量门控
│   │   └── adapters.md            # 适配器
│   ├── design-docs/               # 设计文档（内部）
│   └── generated/                 # 生成文档
│
├── examples/                      # [人类/机器] 📦 示例项目
│   ├── hello-world/
│   │   ├── .anrs/                 # 使用新结构
│   │   ├── src/
│   │   └── README.md
│   ├── todo-app/
│   │   ├── .anrs/
│   │   ├── harness/
│   │   ├── src/
│   │   ├── tests/
│   │   └── README.md
│   └── README.md
│
├── evals/                         # [机器] 📊 评估与基准测试
│   ├── benchmarks/
│   ├── failure-cases/
│   └── prompts/
│
├── scripts/                       # [人类] 🔧 维护脚本
│   ├── rollback.sh
│   └── generate_adapters.sh
│
├── .github/                       # [人类/CI] GitHub 配置
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── README.md                      # [人类] 项目主页
├── LICENSE                        # [人类] MIT 许可证
├── CONTRIBUTING.md                # [人类] 贡献指南
├── CHANGELOG.md                   # [人类] 变更日志
├── CODE_OF_CONDUCT.md             # [人类] 行为准则
├── SECURITY.md                    # [人类] 安全政策
├── .editorconfig                  # [人类] 编辑器配置
└── .gitignore                     # [机器] Git 忽略规则
```

---

## 3. 用户仓库结构（Target Repo）

用户通过 `anrs init` 安装后的目录结构。**设计原则**：对用户业务代码零侵入。

### Level 0 - 最小安装

```
user-project/
├── .anrs/
│   ├── ENTRY.md              # [AI] 入口点
│   └── state/
│       └── state.json        # [AI] 当前状态
├── .cursorrules              # [AI] 跳板文件（仅引流到 ENTRY.md）
└── ... (用户代码)
```

### Level 1 - 标准安装（推荐）

```
user-project/
├── .anrs/
│   ├── ENTRY.md              # [AI] 入口点
│   ├── config.json           # [人类/机器] 项目配置
│   ├── state/
│   │   └── state.json
│   ├── plans/
│   │   ├── active/
│   │   └── backlog/
│   └── scratchpad/
│       └── current.md
├── .cursorrules              # [AI] 跳板文件
├── .gitignore                # 自动追加 .anrs/state/scratchpad
└── ... (用户代码)
```

### Level 2 - 完整安装

```
user-project/
├── .anrs/
│   ├── ENTRY.md
│   ├── config.json
│   ├── state/
│   ├── plans/
│   ├── skills/               # [AI] 本地技能覆盖
│   ├── scratchpad/
│   └── failure-cases/        # [AI] 失败案例归档
├── harness/                  # [机器] 独立质量门控
├── .cursorrules
└── ... (用户代码)
```

---

## 4. Adapter 跳板模式（Trampoline）

**核心思想**：胶水文件只做路由，不包含规范内容。

### 旧模式（问题）

```markdown
# .cursorrules（数百行 Prompt）
You are an AI assistant...
Rule 1: ...
Rule 2: ...
(规范更新时需手动同步所有文件)
```

### 新模式（跳板）

```markdown
# .cursorrules（极简版）
# ANRS Integration
You are operating in an ANRS-governed repository.
Before taking any action, you MUST read and strictly follow:
`.anrs/ENTRY.md`
```

**优势**：

| 方面 | 效果 |
|------|------|
| **解耦** | 底层规范通过 `anrs upgrade` 升级，胶水文件永不修改 |
| **统一** | Cursor、Claude、Codex 读取的规范源头完全一致 |
| **简化** | 适配器维护成本降至最低 |

---

## 5. Templates 配置驱动

**原则**：文件去重 + Manifest 清单

### 结构

```
templates/
├── files/                   # 单一来源，所有模板文件
│   ├── ENTRY.md             # 只有一份
│   ├── config.json
│   └── ...
└── manifests/               # 定义每个 level 需要哪些文件
    ├── minimal.json
    ├── standard.json
    └── full.json
```

### Manifest 示例

```json
// manifests/standard.json
{
  "level": "standard",
  "description": "Recommended for most projects",
  "structure": {
    ".anrs/": {
      "files": ["ENTRY.md", "config.json"],
      "dirs": {
        "state/": ["state.template.json"],
        "plans/": {
          "active/": ["plans/active.README.md"],
          "backlog/": ["plans/backlog.README.md"]
        },
        "scratchpad/": ["scratchpad.md"]
      }
    }
  },
  "adapters": ["cursor", "claude"],
  "harness": false
}
```

### CLI 安装流程

```
1. 读取 manifests/{level}.json
2. 根据 structure 创建目录
3. 从 files/ 复制对应文件
4. 替换模板变量（项目名、路径）
5. 生成跳板适配器文件
```

---

## 6. CLI 设计（Python）

### 安装

```bash
pip install anrs-cli
```

### 核心命令

```bash
# 初始化
anrs init                    # 交互式
anrs init --level minimal    # 最小安装
anrs init --level standard   # 标准安装（默认）
anrs init --level full       # 完整安装

# 适配器
anrs adapter add cursor      # 添加跳板文件
anrs adapter add claude
anrs adapter mode plan       # 切换模式

# Harness
anrs harness                 # 运行质量门控
anrs harness --level L1      # 只运行 L1
anrs harness --strict        # 严格模式

# 状态
anrs status                  # 查看当前状态

# 升级
anrs upgrade                 # 升级 .anrs/ 内规范
```

---

## 7. 迁移映射表

| 当前路径 | 新路径 | 说明 |
|----------|--------|------|
| `ai/` | `spec/` | 重命名，明确是规范定义 |
| `ai/ENTRY.md` | `spec/ENTRY.md` | - |
| `ai/state/` | `spec/state/` | - |
| `ai/skills/` | `spec/skills/` | - |
| `ai/orchestrator/` | `spec/orchestrator/` | - |
| `ai/contracts/` | `spec/contracts/` | - |
| `ai/rules/` | `spec/rules/` | - |
| `ai/agents/` | `spec/agents/` | - |
| `docs/core-beliefs.md` | `spec/core-beliefs.md` | AI 决策参考，移入规范 |
| `docs/architecture/` | `docs/concepts/` | 简化为人类概念说明 |
| `docs/references/*.json` | `spec/contracts/` | 机器可读 Schema |
| `plans/` | 删除 | 模板移入 templates/，示例移入 examples/ |
| `scripts/run_*.sh` | `cli/src/` | CLI 化 |
| `requirements.txt` | `cli/requirements.txt` | 随 CLI 发布 |
| `plugins/` | `ext/` | 简化命名 |

---

## 8. 实施优先级

| 阶段 | 任务 | 优先级 |
|------|------|--------|
| **P0** | 重构 `ai/` → `spec/` | 高 |
| **P0** | 设计 `.anrs/` + 跳板模式 | 高 |
| **P1** | 实现 `anrs init` CLI | 高 |
| **P1** | 更新 examples/ 使用新结构 | 高 |
| **P1** | 更新 adapters/ 为跳板模式 | 高 |
| **P2** | 实现 `anrs harness/upgrade` | 中 |
| **P2** | 编写迁移文档 | 中 |
| **P3** | 开发 VSCode 插件 | 低 |
| **P3** | 发布到 PyPI | 低 |

---

## 9. 总结

```
┌─────────────────────────────────────────────────────────────┐
│                    ANRS 开源仓库                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
│  │ spec/  │ │harness/│ │adapters│ │  ext/  │ │  cli/  │     │
│  │[机器]  │ │[机器]  │ │[人类]  │ │[人类]  │ │[机器]  │     │
│  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘     │
└──────┼──────────┼──────────┼──────────┼──────────┼──────────┘
       │          │          │          │          │
       ▼          ▼          ▼          ▼          ▼
   ┌─────────────────────────────────────────────────────────┐
   │                   anrs init / upgrade                    │
   └─────────────────────────────────────────────────────────┘
                              │
                              ▼
   ┌─────────────────────────────────────────────────────────┐
   │                    用户项目                               │
   │  ┌─────────┐                                             │
   │  │ .anrs/  │  ← 精简运行时（ENTRY + state + plans）       │
   │  └─────────┘                                             │
   │  .cursorrules  ← 跳板文件（仅引流到 .anrs/ENTRY.md）      │
   │  src/ tests/   ← 用户代码（零侵入）                       │
   └─────────────────────────────────────────────────────────┘
```

**核心理念**：
1. 开源仓库 = 完整开发平台
2. 用户安装 = 精简协议运行时
3. 跳板模式 = 胶水文件永不修改
4. 配置驱动 = 模板文件去重
