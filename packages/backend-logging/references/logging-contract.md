# 跨语言日志事件契约

## 1. 总原则

日志首先是**结构化事件**，其次才是字符串输出。

同一个事件经过两个渲染器：

```text
结构化事件 → Pretty Terminal
          └→ NDJSON
```

调用方不关心当前输出格式，不得出现：

```text
if production:
    log_json(...)
else:
    log_pretty(...)
```

这份契约约束字段语义，不要求所有语言使用相同的日志库。

---

## 2. 顶层字段

| 字段 | 必需性 | 类型 | 说明 |
|---|---|---|---|
| `ts` | 必需 | string | 事件发生时间；JSON 使用 UTC RFC 3339，例如 `2026-08-26T05:42:18.604Z` |
| `level` | 必需 | string | `debug` / `info` / `warn` / `error`；`trace`、`fatal` 仅在项目确有需要时扩展 |
| `msg` | 必需 | string | 面向人的简短说明；不承载动态字段 |
| `event` | 重要事件必需 | string | 稳定、可查询的事件名，例如 `http.request.completed` |
| `service` | 服务建议 | string | 服务或进程名，不使用主机名代替 |
| `env` | 服务建议 | string | `development` / `test` / `staging` / `production` 或项目已有语义 |
| `version` | 建议 | string | 构建版本、Git SHA 或发布版本 |
| `logger` | 建议 | string | 组件/作用域，例如 `http.access`、`worker.publish` |
| `request_id` | 有则必填 | string | 当前请求或操作的关联 ID |
| `trace_id` | 有则必填 | string | 32 位小写十六进制 Trace ID |
| `span_id` | 有则必填 | string | 16 位小写十六进制 Span ID；存在时应同时存在 `trace_id` |
| `ctx` | 可选 | object | 事件特有的结构化上下文 |
| `error` | 失败事件可选/建议 | object | 规范化错误对象 |

允许日志库或运行时补充 `pid`、`thread`、`host` 等字段，但不得改变上表字段的语义。

空值应省略，不要输出大量 `null`。

---

## 3. JSON 示例

```json
{
  "ts": "2026-08-26T05:42:18.604Z",
  "level": "info",
  "msg": "HTTP request completed",
  "event": "http.request.completed",
  "service": "api",
  "env": "production",
  "version": "1.8.0",
  "logger": "http.access",
  "request_id": "req_01K3N7VZ7HY5TQH6E4K4X8NFKG",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "ctx": {
    "method": "GET",
    "route": "/v1/posts/:id",
    "status": 200,
    "duration_ms": 38.4
  }
}
```

实际 NDJSON 必须压缩成一行；上面仅为阅读而缩进。

---

## 4. `msg` 与 `event`

两者职责不同：

- `msg`：给人看，可以调整措辞，但应简洁稳定。
- `event`：给机器查，修改相当于改变查询契约。

推荐命名：

```text
<domain>.<entity-or-operation>.<outcome>
```

示例：

```text
service.started
http.request.completed
http.request.failed
job.transcription.completed
job.transcription.failed
external.x.publish.failed
db.query.slow
auth.login.denied
```

规则：

- 全小写；
- 使用点分段；
- 分段内部使用 `snake_case`；
- 不把 ID、用户名、HTTP 状态码等动态值写进事件名；
- 同一结果不要同时出现 `publish_failed`、`publish.error`、`x_publish_fail` 三套命名。

---

## 5. 日志级别

| 级别 | 使用场景 | 不该记录 |
|---|---|---|
| `debug` | 开发诊断、分支选择、缓存命中、有限状态快照 | 高频循环逐项输出、完整负载、生产默认开启 |
| `info` | 服务生命周期、请求/任务完成、重要业务结果、配置模式摘要 | 每个内部函数入口、无运营价值的“执行成功” |
| `warn` | 可恢复异常、降级、重试、慢操作、接近容量/限额 | 所有 4xx、用户正常输入错误、已经升级为 error 的同一失败 |
| `error` | 当前操作失败、需要排查、对调用方返回失败或任务终止 | 已被上层统一记录的同一异常、预期分支 |

可选扩展：

- `trace`：比 debug 更细的临时诊断，默认关闭。
- `fatal`：进程无法继续。日志调用本身不应偷偷终止进程；退出由调用方明确控制。

### HTTP 状态不是级别的唯一依据

- 2xx/3xx 通常为 `info`；
- 预期的 4xx 可为 `info`，异常激增或安全风险才使用 `warn`；
- 5xx 通常为 `error`；
- 取消请求、客户端断开等需结合框架语义判断，不能机械归类。

---

## 6. `ctx` 字段规则

`ctx` 只放本事件特有的数据，值必须能够安全转为 JSON 原生类型：

- string
- number
- boolean
- array
- object

不要直接塞入：

- 任意 ORM 实体；
- HTTP Request/Response 对象；
- 大模型完整 prompt/response；
- 二进制数据；
- 大型数组；
- 未知 `toString()` 行为的业务对象。

动态值必须作为字段传入：

```text
正确：msg="Publish failed", ctx.account_id="acc_7", ctx.attempt=2
错误：msg="Publish failed for acc_7 at attempt 2"
```

推荐单位：

- 耗时：`duration_ms`，number；
- 字节：`size_bytes`，integer；
- 数量：`*_count`，integer；
- 比例：使用明确语义，例如 `success_rate`；
- 时间点：RFC 3339 字符串；
- 枚举：稳定的小写字符串。

---

## 7. 错误对象

标准形态：

```json
{
  "error": {
    "type": "TimeoutError",
    "message": "upstream timed out after 10s",
    "code": "UPSTREAM_TIMEOUT",
    "stack": "TimeoutError: upstream timed out after 10s\n    at ..."
  }
}
```

字段：

| 字段 | 说明 |
|---|---|
| `type` | 异常/错误类型 |
| `message` | 原始错误说明，经过必要脱敏 |
| `code` | 稳定错误码；没有则省略 |
| `stack` | 可操作失败的堆栈；JSON 内以转义换行保存 |
| `cause` | 可选的单层原因对象；避免无限递归 |

规则：

1. 同一个异常只在**最终拥有处理结果的边界**记录一次。
2. 底层可以补充上下文并向上返回，但不要每层都打印堆栈。
3. 不要把错误对象仅转成字符串后丢失类型、错误码和堆栈。
4. Pretty 模式可以多行展示堆栈；JSON 仍必须保持一个物理行。
5. `warn` 也可以带 `error`，用于已恢复、会重试或已降级的失败。

---

## 8. 关联上下文

优先使用已有机制传播：

- HTTP request ID；
- OpenTelemetry trace/span；
- AsyncLocalStorage / contextvars / Context / MDC / logging scope；
- worker/job 的 operation ID。

`trace_id` 和 `span_id` 作为顶层字段，便于日志与追踪关联。没有 tracing 时不要为了字段完整而伪造 Span ID。

异步场景必须测试上下文不会串请求、丢失或泄漏到下一个任务。

---

## 9. 边界事件

### 服务启动

只记录一条紧凑摘要：

```text
event=service.started
ctx.port=8080
ctx.log_format=json
ctx.log_level=info
```

可以包含版本、环境、监听地址，不得打印完整配置和秘密。

### HTTP 请求

默认在响应完成时记录一次：

```text
event=http.request.completed
ctx.method=GET
ctx.route=/v1/posts/:id
ctx.status=200
ctx.duration_ms=38.4
```

- 使用路由模板，不默认记录带 ID/查询参数的原始 URL；
- 不默认记录 body、cookie、authorization、user-agent；
- request ID 放顶层；
- 长连接或长任务可以在开始时增加一条明确的 started 事件。

### 外部调用

```text
event=external.x.publish.failed
ctx.operation=publish_post
ctx.status=503
ctx.duration_ms=10024.8
ctx.attempt=3
```

记录目标服务/主机和路由模板，不记录 URL 中的凭据与敏感查询参数。

### 数据库

重点记录：

- 连接/事务失败；
- 超过项目阈值的慢查询；
- migration 结果；
- 关键一致性冲突。

不要默认记录 SQL 参数、用户输入或每条成功查询。

### 后台任务

推荐终态事件：

```text
job.<name>.completed
job.<name>.failed
```

字段包含 job ID、attempt、duration、结果计数。只有长任务或排队诊断需要时才记录 started。

---

## 10. 脱敏契约

脱敏必须位于日志流水线中，不能只依赖调用方自觉。

至少覆盖大小写不敏感的键：

```text
authorization
proxy-authorization
cookie
set-cookie
password
passwd
secret
token
access_token
refresh_token
api_key
client_secret
private_key
session
otp
credit_card
```

默认替换为：

```text
[REDACTED]
```

其他规则：

- 请求/响应 body 默认不记录；
- 邮箱、手机号、身份证件、精确地址等 PII 默认省略或按业务规则去标识化；
- URL 去掉 userinfo，并移除敏感 query 参数；
- AI、播客、文档等内容型系统只记录模型、长度、token/字符数、耗时和内容 ID，不记录完整内容；
- 文件只记录受控路径、文件名、MIME、大小与 ID，不记录文件内容；
- 第三方错误信息可能包含请求内容，写入前需要规范化。

---

## 11. 输出与存储

### 服务、容器、Serverless

- 输出到进程流；
- 默认 NDJSON；
- 每行一个事件；
- 文件收集、轮转和保留由运行环境负责；
- 不在业务进程里同步写数据库作为主日志存储。

### CLI

- 交互 TTY 默认 Pretty；
- 管道或重定向默认 JSON/无颜色格式，取决于命令契约；
- 业务结果输出与诊断日志应使用不同流或明确模式，避免破坏机器消费。

### 桌面/本地运行时

- 终端 Pretty 用于开发；
- 若产品需要可提交诊断包，可额外写受控的滚动 NDJSON 文件；
- 明确文件大小、数量、保留期和敏感字段；
- 不要与终端输出维护两套事件定义。

---

## 12. 与 OpenTelemetry 的映射

本契约不是 OTLP 序列化格式，但字段可以直接映射：

| 本契约 | OpenTelemetry Log Data Model |
|---|---|
| `ts` | Timestamp |
| `level` | SeverityText / SeverityNumber |
| `msg` | Body |
| `event` | EventName |
| `service` / `env` / `version` | Resource attributes |
| `logger` | InstrumentationScope |
| `ctx` | Attributes |
| `trace_id` / `span_id` | TraceId / SpanId |

因此后续接 Collector 或 exporter 时，不需要重写调用方日志语义。
