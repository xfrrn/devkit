# 文档职责、依赖与事实来源

## 1. 文档依赖图

```text
00 Project Brief
      ↓
01 Requirements
      ↓
03 Domain Model
      ↓
02 System Design
   ┌──┴──────────┐
   ↓             ↓
04 API       05 Data
   └──┬──────────┘
      ↓
06 Security
      ↓
08 Testing
      ↓
07 Roadmap
      ↓
09 Progress Log

重大技术取舍 ──→ decisions/ADR-*.md
```

说明：编号是稳定阅读顺序；实际编写时，领域模型通常应先于详细系统设计。

## 2. 单一事实来源

| 信息 | 主要事实来源 | 其他文档如何处理 |
|---|---|---|
| 项目目标与边界 | `00-project-brief.md` | Requirements/Roadmap 引用，不重复长篇定义 |
| 功能与质量要求 | `01-requirements.md` | API、Data、Testing 使用需求 ID 追踪 |
| 领域术语与业务规则 | `03-domain-model.md` | API/Data 使用统一术语，不另造名称 |
| 当前技术架构 | `02-system-design.md` | 关键原因链接 ADR |
| 接口结构 | OpenAPI 或 `04-api-contract.md` | Requirements 只描述行为，不复制字段表 |
| 实际数据库结构 | migration/schema | `05-data-design.md` 解释设计、约束和生命周期 |
| 安全与合规要求 | `06-security-and-compliance.md` | API/Data/Testing 引用具体控制措施 |
| 未来计划 | `07-roadmap.md` | Progress Log 不复制完整未来计划 |
| 测试方法与质量门槛 | `08-testing-strategy.md` | Requirements 只保留验收条件 |
| 真实开发历史 | `09-progress-log.md` | Roadmap 只维护当前状态摘要 |
| 决策原因与备选方案 | `decisions/ADR-*.md` | System Design 只总结最终结论 |

## 3. 常见变更的影响范围

| 变更 | 首先更新 | 检查下游 |
|---|---|---|
| 新增用户能力 | Requirements | Domain、API、Data、Security、Testing、Roadmap |
| 删除或改变 MVP 范围 | Brief | Requirements、Roadmap、Testing |
| 新增核心实体 | Domain Model | API、Data、System Design、Testing |
| 新增公开接口 | API Contract | Requirements、Security、Testing |
| 修改持久化结构 | Data Design + migration | Domain、API、Security、Testing |
| 修改认证/授权 | Security + API | Data、System Design、Testing，必要时 ADR |
| 更换重要框架/架构 | ADR | System Design、Roadmap、Testing、Operations |
| 完成里程碑 | Progress Log | Roadmap 状态 |
| 发现计划偏差 | Progress Log | Roadmap，必要时 ADR/Requirements |

## 4. 文档状态

统一使用：

- `Draft`：仍在形成，可能明显变化；
- `In Review`：内容基本完整，等待确认；
- `Approved`：当前项目基线；
- `Deprecated`：已失效，仅保留历史。
