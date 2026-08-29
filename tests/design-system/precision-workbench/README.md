# Precision Workbench 测试

## 运行配置

- Skill：`precision-workbench`
- Source：`packages/design-system/precision-workbench`
- Model：未指定
- Model：`gpt-5.6-sol`
- Reasoning：`medium`
- Agent Harness：Codex Desktop

## 测试目的

用与来源项目不同的“实验室样本库存管理”场景验证规范能否独立生成桌面工作区，而不是复刻内容运营产品。

## 测试提示词

```text
读取 packages/design-system/precision-workbench，为实验室样本库存实现一个响应式桌面管理页。

页面需要包含：
- 左侧主导航和样本分类子导航；
- 样本列表/表格、搜索、状态筛选和批量操作；
- 新建样本表单与删除确认 Dialog；
- 右侧“实验记录”辅助面板；
- 空状态、加载状态、字段错误和保存失败状态；
- 1440×900 与 760×520 两个视口。

只使用该设计系统的语义 Token，不复制来源项目名称、业务文案或图标资产；不要增加深色模式。
```

## 验收标准

- 1440px 下保持 200px 侧栏、主任务区和可读的右侧辅助列。
- 760px 下侧栏收为 72px，辅助列改为可关闭 Overlay，页面无横向溢出。
- 正文与控件主要使用 12–14px 层级，仍保持可读性和清晰焦点。
- 普通卡片、表格和列表通过边框分层，不使用默认阴影或毛玻璃。
- Primary Button 为中性近黑；Accent 只用于当前导航、选择和辅助能力。
- 表格数字使用 tabular nums，窄屏无法保留的列转入行详情。
- Empty、Loading、Error、Disabled、Hover、Selected 和 Focus-visible 状态齐全。
- Dialog 有标题、说明、Escape 关闭、焦点恢复和明确的危险确认按钮。
- `prefers-reduced-motion` 下功能完整。
- 不包含来源项目品牌、文案、Logo、平台图标或业务数据。

## 实际测试结果

- 2026-08-29：完成来源 Renderer 的生产构建和可访问性快照检查。
- 1440×900：登录、首页、热点列表和右侧辅助面板布局正常，控制台无错误。
- 760×520：首页侧栏收为 72px，文字导航隐藏，主区无横向溢出。
- Token 与 Tailwind 映射已做静态一致性检查，CSS 括号和自定义变量引用通过验证。
- 尚未执行上述“实验室样本库存”独立生成测试；当前结果证明提炼依据和代码骨架可用，不证明所有框架消费方式。

## 已知问题

- 本规范只提供浅色主题。
- 390px 手机布局不在目标范围；需要移动优先时改用其他设计系统。
- Inter 仅作为字体栈名称，不随包分发字体文件。
- Tailwind 4 项目需要把配置映射迁入现有 `@theme` 或适配其构建方式。
