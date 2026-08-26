# Quiet Native 测试

## 运行配置

- Skill：`quiet-native`
- Source：`packages/design-system/quiet-native`
- Model：`gpt-5.6-sol`
- Reasoning：`medium`
- Agent Harness：Codex Desktop

## 测试内容

用非阅读场景验证 Quiet Native 是否是一套通用、响应式的界面风格。

## 提示词

```text
读取 packages/design-system/quiet-native，实现响应式任务管理页：列表、表单、空态、错误、弹层、深色模式。
```

## 验收

- 移动端与桌面端布局自然。
- 浅色与深色语义一致。
- 列表、表单、状态和弹层遵循 Quiet Native。
- 无多余渐变、卡片嵌套或标签堆砌。
- 键盘焦点清晰，可点击区域不小于 44×44px。
