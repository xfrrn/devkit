# 各语言日志适配指南

## 1. 选择原则

先检查项目已经在用什么，再选择实现。

```text
已有成熟 logger 可满足契约 → 扩展现有 logger
没有统一 logger             → 使用语言/框架主流结构化方案
默认 console 太丑           → 只替换/扩展 renderer，不重写调用层
```

禁止同时保留两套应用 logger，例如一部分模块用 Pino，另一部分用 Winston，再额外包一层自研 API。

目标不是让所有语言代码长得一样，而是让输出事件语义一致。

---

## 2. 推荐矩阵

| 语言/栈 | 优先方案 | Pretty | JSON | 上下文 |
|---|---|---|---|---|
| Node.js / TypeScript | Pino；已有框架 logger 时优先接入其适配 | `pino-pretty` 或自定义 prettifier，仅开发使用 | Pino 原生 NDJSON，规范化 level/field | child logger + AsyncLocalStorage |
| Python | structlog 与 stdlib logging 协同 | `ConsoleRenderer`，必要时 Rich 异常 | `JSONRenderer` | `contextvars` / bound logger |
| Go | 标准库 `log/slog` | `tint` 或小型自定义 `slog.Handler` | `slog.JSONHandler` | `context.Context` + logger.With |
| Rust | `tracing` + `tracing-subscriber` | compact/custom `FormatEvent`；普通事件保持单行 | `.json()` | spans + fields |
| Java / Kotlin | SLF4J + Logback；Spring 项目延用其现有体系 | PatternLayoutEncoder + ANSI/Jansi 或自定义 converter | Logback JsonEncoder / 项目已有 JSON encoder | MDC + fluent key-value API |
| .NET | `Microsoft.Extensions.Logging`；已有 Serilog/NLog 时继续用 | SimpleConsole 或自定义 ConsoleFormatter | AddJsonConsole 或现有 JSON sink | logging scopes + Activity |
| PHP | Monolog | Console/Stream handler + LineFormatter | JsonFormatter | context + processors |
| 其他语言 | 原生结构化 logger 或项目既有 logger | 自定义小型 formatter | 一行 JSON encoder | 该语言的 request/task context 机制 |

不在 Skill 中固定依赖版本。根据目标项目的运行时、lockfile 和兼容范围选择版本。

### Pretty renderer 的共同硬要求

无论使用哪种语言或库，最终 formatter 都必须满足：

- level 标签使用固定语义色，而不是依赖随机主题；
- ANSI 序列不参与 padding 和截断；
- 中文、全角字符和组合字符按终端显示宽度计算；
- time、level、scope、message、context 使用固定顺序和稳定列宽；
- `NO_COLOR`、`TERM=dumb`、非 TTY 与 JSON 模式不会输出 ANSI；
- 普通对象不会被库默认 formatter 展开为多行；
- 彩色和无色输出去除 ANSI 后具有相同布局。

优先使用生态内成熟的 ANSI-aware 与 Unicode display-width 能力。不要用 `len`、`length`、字节数或 UTF-16 code unit 数直接计算终端列宽。

---

## 3. Node.js / TypeScript

### 首选路径

- 纯 Node、Fastify、NestJS 等项目优先使用现有 Pino 集成；
- Pino 本身保留机器可读 JSON；
- Pretty 只作为开发 transport、worker transport 或管道工具；
- 不在生产调用链同步执行昂贵 prettifier。

### 实现重点

- 在一处创建 root logger；
- 使用 `formatters.level` 将数字级别规范化为字符串或在 collector 侧保留明确映射；
- 配置 timestamp 为 `ts` RFC 3339 UTC；
- 使用 `redact` 集中脱敏；
- 使用 serializers 规范化 Error、Request、Response，禁止直接输出完整对象；
- 使用 child logger 绑定模块字段；
- 使用 AsyncLocalStorage 绑定 request ID / trace ID；
- 避免框架自动 access log 与自定义 access middleware 重复。

### Pretty

`pino-pretty` 默认输出可作为起点，但应检查：

- 时间格式；
- level 是否固定宽度；
- scope/logger 是否可见；
- 对象是否被多行展开；
- error 是否正确显示；
- `NO_COLOR` 与非 TTY 行为。

不满足 `terminal-style.md` 时，使用 `messageFormat`、字段忽略/单行配置或小型自定义 prettifier。自定义 formatter 应使用 ANSI-aware truncate/pad 与 Unicode display-width 工具；不要依赖 JavaScript 的 `string.length` 对齐中文。

---

## 4. Python

### 首选路径

structlog 很适合“一套 processor 链 + 两个 renderer”：

```text
shared processors
  → ConsoleRenderer (development)
  → JSONRenderer    (production)
```

### 实现重点

- 与标准库 logging 统一，确保依赖库日志不会消失；
- 使用 `ProcessorFormatter` 或等价配置处理 foreign logs；
- 使用 `contextvars` 传播 request/trace context；
- structlog 默认把人类消息放在 `event` 键；在最终 processor 中将其规范化为 `msg`，把稳定机器事件名保留为单独的 `event`；
- processor 顺序中先绑定 timestamp/level/logger/context，再脱敏，再序列化 error，最后 renderer；
- ConsoleRenderer 与异常格式化器不要重复处理同一个 `exc_info`；
- Rich/structlog 的默认样式只是起点，必须调整为固定 level/scope/message 列；
- 中英文混排时使用 Rich measurement、`wcwidth` 或等价显示宽度能力；
- 测试环境捕获日志时使用确定性 timestamp 或可注入 clock。

### 已有 stdlib logging

已有项目不必为了名称统一重写所有调用。可以：

- 保留 `logging.getLogger(__name__)`；
- 使用 structlog ProcessorFormatter 统一最终输出；
- 或使用已有 JSON formatter + 自定义漂亮 Console formatter；
- 确保 `extra` 字段不会在 formatter 中被丢失。

---

## 5. Go

### 首选路径

Go 1.21+ 优先使用标准库 `log/slog`：

- `slog.JSONHandler` 用于 JSON；
- `tint` 或项目内小型 `slog.Handler` 用于 Pretty；
- `ReplaceAttr` 规范化时间、级别、字段名和脱敏；
- `With` / `WithGroup` 绑定组件和上下文。

### 实现重点

- 不把 `context.Context` 存在全局变量；
- request middleware 从 context 提取 request/trace ID；
- error 使用结构化 attrs，不只传 `err.Error()`；
- 避免每次调用重新创建 logger；
- 只有需要 call site 时开启 `AddSource`；
- 自定义 Handler 必须正确实现 `Enabled`、`WithAttrs`、`WithGroup`，避免字段丢失或 data race；
- Pretty Handler 必须使用 ANSI-aware/Unicode display-width padding，不能直接用 rune 数或字节数对齐。

### 旧版 Go 或已有库

已有 zerolog、zap 等成熟实现时，优先配置其 ConsoleWriter/encoder 和 JSON encoder，不为迁移到 slog 而扩大任务范围。

---

## 6. Rust

### 首选路径

使用 `tracing` 记录事件和 span，`tracing-subscriber` 负责输出：

- JSON：`fmt().json()`；
- Pretty：优先 compact 或自定义 `FormatEvent`，保持普通事件单行；
- context：span fields；
- filtering：EnvFilter 或项目已有配置。

### 注意

`tracing-subscriber` 的 `pretty()` 是偏多行、偏调试的输出。它可以用于临时深度调试，但不一定符合本 Skill 的默认“紧凑单行”终端规范。需要根据项目选择 `compact()` 或实现小型 formatter。自定义 `FormatEvent` 应配合 Unicode width 与 ANSI stripping/truncation 能力，确保 CJK 文本不挤乱后续列。

确保：

- JSON feature 已启用；
- ANSI 只用于 Pretty；
- span context 在 JSON 中按需要 flatten；
- error chain 不重复输出；
- async task 中 span 被正确 instrument。

---

## 7. Java / Kotlin

### 首选路径

应用代码依赖 SLF4J，输出交给 Logback 或项目现有 provider：

- 使用 SLF4J fluent API 的 key-value pairs；
- 使用 MDC 传播 request ID、trace ID；
- ConsoleAppender + PatternLayoutEncoder 实现 Pretty；
- JsonEncoder 或项目已有 encoder 输出 NDJSON。

### 实现重点

- Pattern 中固定时间、level、logger 与 message 顺序；
- Jansi/PatternLayout 的颜色表达式必须只包围目标列，不能让 ANSI 参与宽度；
- 包含 CJK message 时验证 Pattern padding 的真实终端显示宽度；
- 使用 `%kvp` 或 encoder 支持保留结构化字段；
- 异步/协程/线程池切换时正确复制和清理 MDC；
- 不把完整类名占满终端，可裁剪 logger 名；
- 避免同时配置 Spring 默认 console、Logback 自定义 appender 和另一套 JSON appender造成重复；
- exception 只由 encoder/layout 渲染一次。

Spring Boot 已提供可用的结构化日志能力时，优先沿用现有版本支持，不额外引入平行 provider。

---

## 8. .NET

### 首选路径

优先保留 `ILogger<T>`：

- Pretty：SimpleConsole 可作起点；要满足固定列和错误续行时使用自定义 `ConsoleFormatter`；
- JSON：项目允许原生字段形态时可用 `AddJsonConsole`；要求本 Skill 的精确字段名时使用自定义 formatter 或扩展现有 Serilog/NLog 配置；
- context：`BeginScope` 与 `Activity`；
- 配置：`Logging` section 与环境变量。

### 实现重点

- 使用 message template 和结构化参数，不使用字符串插值；
- JsonConsole 或自定义 JSON formatter 中不要把 message 预先序列化为 JSON；
- scopes 在 formatter 中必须可见；
- 自定义 ConsoleFormatter 需单独处理 ANSI 宽度与 Unicode 显示宽度，不能直接使用 `string.Length`；
- Activity 存在时映射 trace/span ID；
- 若项目已使用 Serilog/NLog，继续扩展现有 sink/formatter，不再并行注册另一套 console provider；
- 高频日志可使用 source-generated logging，但不要为了微优化牺牲契约清晰度。

---

## 9. PHP

Monolog 可使用同一 record 配置两个 formatter：

- Pretty：StreamHandler/ConsoleHandler + LineFormatter；
- JSON：StreamHandler + JsonFormatter；
- processors 绑定 request ID、service、version 和脱敏；
- context 放结构化数组，不依赖 message placeholder 承载全部信息；
- WebProcessor 默认字段可能包含 URI/IP，需要按敏感策略筛选。

---

## 10. 其他语言的最小实现形态

找不到上表对应项时，寻找以下能力：

1. 结构化 key-value API；
2. level filtering；
3. child/bound logger 或 context；
4. JSON encoder；
5. 可替换的 console formatter；
6. error/exception serializer；
7. redaction hook；
8. TTY 与颜色检测。

项目内只需要一个小型 bootstrap/config 模块，不需要发明跨语言抽象层。

---

## 11. 官方资料

- OpenTelemetry Logs Data Model: <https://opentelemetry.io/docs/specs/otel/logs/data-model/>
- OpenTelemetry trace context in log formats: <https://opentelemetry.io/docs/specs/otel/compatibility/logging_trace_context/>
- Twelve-Factor Logs: <https://12factor.net/logs>
- NO_COLOR: <https://no-color.org/>
- Go slog: <https://go.dev/blog/slog>
- tint: <https://github.com/lmittmann/tint>
- Pino: <https://getpino.io/>
- pino-pretty: <https://github.com/pinojs/pino-pretty>
- structlog: <https://www.structlog.org/en/stable/>
- tracing-subscriber fmt: <https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/>
- SLF4J manual: <https://www.slf4j.org/manual.html>
- Logback encoders: <https://logback.qos.ch/manual/encoders.html>
- .NET console log formatting: <https://learn.microsoft.com/dotnet/core/extensions/logging/console-log-formatter>
- Monolog formatters: <https://seldaek.github.io/monolog/doc/02-handlers-formatters-processors.html>
