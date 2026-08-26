# 日志系统质量检查清单

## A. 仓库与范围

- [ ] 已识别语言、框架、运行时和部署形态。
- [ ] 已确认当前 logger、配置位置和直接 print/console 调用。
- [ ] 已确认 HTTP、worker、job、DB、外部调用和错误边界。
- [ ] 已识别 request/trace/context 传播方式。
- [ ] 大型项目已明确本次迁移范围，没有无边界重写。

## B. 架构

- [ ] 只有一个 logger bootstrap/config 入口。
- [ ] Pretty 与 JSON 共享同一结构化事件流水线。
- [ ] 业务代码不判断环境后选择不同日志调用。
- [ ] 没有两套竞争 logger 并行存在。
- [ ] 第三方/框架日志被接入或明确过滤。

## C. 配置

- [ ] 支持语义等价的 `LOG_LEVEL`。
- [ ] 支持 `LOG_FORMAT=auto|pretty|json` 或项目内等价配置。
- [ ] 支持 `LOG_COLOR=auto|always|never` 或项目内等价能力。
- [ ] development 默认 Pretty，production/staging 默认 JSON。
- [ ] 颜色可用的交互式 TTY 默认开启颜色。
- [ ] 非 TTY 不强制 ANSI。
- [ ] `NO_COLOR` 与 `TERM=dumb` 能关闭颜色。
- [ ] JSON 模式无论任何颜色变量都不输出 ANSI。
- [ ] source/callsite 默认关闭，按需开启。

## D. Pretty Terminal

- [ ] 颜色可用的 TTY 中，`DEBUG/INFO/WARN/ERROR/FATAL` level 标签具有固定且可区分的语义色。
- [ ] 时间、level、scope、message、context 顺序固定。
- [ ] 默认列宽已明确；列之间使用固定空格，不使用 Tab。
- [ ] level 宽度一致，可快速纵向扫描。
- [ ] scope 与 message 使用稳定显示宽度，超长值以 `…` 截断。
- [ ] padding/truncation 忽略 ANSI，不把转义序列计入列宽。
- [ ] 中文、全角字符和中英文混排按终端显示宽度对齐。
- [ ] 正常事件保持一个物理行。
- [ ] context 字段顺序稳定。
- [ ] context key 被弱化，value 保持清晰，不按类型彩虹着色。
- [ ] HTTP status、慢耗时等语义强调仅使用有限且稳定的颜色映射。
- [ ] 大对象不会多行展开。
- [ ] 错误堆栈作为缩进续行，首行仍是结构化摘要。
- [ ] 错误类型醒目，stack 弱化，不给整行涂红或加红底。
- [ ] `NO_COLOR` 后列起始位置与彩色模式一致。
- [ ] 没有 Emoji、ASCII Logo、随机 scope 色、彩虹字段或大面积背景色。

## E. JSON / NDJSON

- [ ] 每个物理行都是一个完整 JSON object。
- [ ] 每行包含 `ts`、`level`、`msg`。
- [ ] 重要事件包含稳定 `event`。
- [ ] `ts` 为 UTC RFC 3339。
- [ ] `level` 为规范化小写字符串。
- [ ] 动态字段保留 JSON 原生类型。
- [ ] `ctx` 是 object，不是序列化字符串。
- [ ] JSON 没有缩进、多行或 ANSI。
- [ ] 空值被省略，而非大量输出 null。
- [ ] 每行能通过 `scripts/check_json_logs.py`。

## F. 错误

- [ ] error 保留 type、message、code（有则）和 stack（需要时）。
- [ ] 同一失败不会在多个层重复打印完整堆栈。
- [ ] catch 不会只为记录日志后吞掉异常。
- [ ] logger 不会偷偷改变退出、panic 或 retry 语义。
- [ ] 第三方错误文本经过必要规范化和脱敏。

## G. Context 与关联

- [ ] request ID 在入口创建/读取并传播。
- [ ] tracing 已存在时自动附加 trace ID / span ID。
- [ ] 没有 tracing 时不会伪造 span ID。
- [ ] async/thread/coroutine/task 切换后上下文仍正确。
- [ ] 请求结束后上下文被清理，不串到下一请求。
- [ ] child/bound logger 不会丢失已有字段。

## H. 安全与隐私

- [ ] 脱敏在 logger pipeline 中集中执行。
- [ ] authorization、cookie、password、token、secret、api key 等被覆盖。
- [ ] 请求/响应 body 默认不记录。
- [ ] URL 中的凭据和敏感 query 已移除。
- [ ] PII 默认省略或去标识化。
- [ ] AI prompt、文档正文、音频转录、文件内容等大内容默认不记录。
- [ ] 错误堆栈和第三方对象没有绕过脱敏策略。

## I. 事件选择

- [ ] 服务启动只打印紧凑摘要，不 dump 全部配置。
- [ ] HTTP 默认每请求一条 completion，而不是 start/end/handler 多重重复。
- [ ] 4xx 不会机械全部标为 warn。
- [ ] 记录慢查询/慢调用和失败，而不是每条成功 SQL。
- [ ] worker/job 以终态事件为主。
- [ ] 没有函数入口/出口、循环逐项等噪声日志。
- [ ] 日志没有代替 metrics、tracing 或 audit log 的职责。

## J. 存储与运行环境

- [ ] 容器/服务输出到进程流，默认不在应用内轮转文件。
- [ ] CLI 的业务输出与诊断日志不会互相污染。
- [ ] 桌面 JSON 文件仅在明确需要时启用，并定义大小/数量/保留期。
- [ ] 日志写入失败不会递归记录造成死循环。
- [ ] 高负载路径没有明显同步序列化/网络阻塞风险。

## K. 测试与交付

- [ ] logger 单元测试覆盖 Pretty、JSON、redaction、error、context。
- [ ] Pretty golden/snapshot 覆盖全部 level。
- [ ] 去除 ANSI 后，各列起始位置稳定。
- [ ] 彩色模式中 level 的 SGR 语义已验证。
- [ ] 英文、中文和中英文混排的对齐已验证。
- [ ] 超长 scope/message 的显示宽度截断已验证。
- [ ] `NO_COLOR`、`TERM=dumb` 和非 TTY 行为已验证。
- [ ] JSON 样本已逐行解析。
- [ ] 相关 build/lint/typecheck/test 已运行。
- [ ] `.env.example` 或现有配置文档已更新。
- [ ] 最终报告说明 palette、列宽，并包含彩色 Pretty 说明、无色 Pretty 样例和一条 JSON 样例。
- [ ] 未完成迁移或无法验证的部分已明确列出。
