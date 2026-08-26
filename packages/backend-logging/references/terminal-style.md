# Pretty Terminal 日志视觉规范（强制）

## 1. 视觉目标

Pretty Terminal 不是 JSON 日志的随意打印版本，也不是可有可无的装饰。对于交互式终端，它必须同时满足：

```text
有颜色区分
列对齐稳定
层级清楚
单行紧凑
错误醒目
浅色/深色终端均可读
关闭颜色后仍然整齐
```

验收顺序：

1. 先看是否能快速纵向扫描；
2. 再看颜色是否传达语义；
3. 最后看信息是否完整、可复制、可查询。

默认 formatter 只要不满足本规范，就不能因为“库自带”而直接接受。

---

## 2. 标准布局

完整模式默认使用以下列：

```text
TIME          LEVEL  SCOPE                 MESSAGE                         CONTEXT
12 cells      5      20 cells              30 cells                       remaining
```

列之间固定使用两个普通空格，禁止使用 Tab。

去除颜色后的参考输出：

```text
13:42:18.604  INFO   http.access           Request completed               method=GET route=/v1/posts/:id status=200 duration=38.4ms request_id=req_01K3N7VZ7HY5TQH6E4K4X8NFKG
13:42:20.087  WARN   db.query              Slow query                      operation=list_posts duration=842.7ms rows=24
13:42:21.311  ERROR  publisher.x           Publish failed                  account_id=acc_7 attempt=2
              ╰─ TimeoutError: upstream timed out after 10s
                 at publisher/client.ts:184
                 at worker/run.ts:72
```

字段顺序不可随机变化：

```text
时间 → 级别 → logger/scope → message → 关键上下文
```

### 固定列宽

| 列 | 默认显示宽度 | 规则 |
|---|---:|---|
| time | 12 | `HH:mm:ss.SSS` |
| level | 5 | 右侧补空格，不缩写为单字符 |
| scope | 20 | 超出后按显示宽度截断 |
| message | 30 | 简短消息补空格；过长时显示省略号 |
| context | 剩余宽度 | 使用稳定字段顺序 |

推荐允许项目通过 formatter 常量调整 `scope_width` 与 `message_width`，但同一进程内不能逐行变化。

---

## 3. 对齐必须按终端显示宽度计算

不能直接使用字符串长度做 padding 或截断。

必须忽略：

- ANSI SGR 转义序列；
- 零宽连接符和组合字符；
- 不占显示宽度的控制字符。

必须正确处理：

- 中文、日文、韩文等通常占两个终端单元格的字符；
- 全角标点；
- Unicode 省略号 `…`；
- 用户提供的非 ASCII scope 或 message。

例如：

```text
13:42:18.604  INFO   api.auth             用户登录成功                    user_id=user_42
13:42:19.012  INFO   worker.publish       Publish completed                task_id=task_17
```

这两行的 context 起始列应一致。

实现时优先使用语言生态成熟的 `wcwidth`、Unicode display width、ANSI-aware truncate/pad 能力。若自行实现，必须有中英文混合与 ANSI 嵌套测试。

---

## 4. 强制颜色主题

在支持颜色的交互式 TTY 中，颜色默认开启。颜色不是随机装饰，而是固定的语义映射。

参考主题见 [`../assets/terminal-theme.json`](../assets/terminal-theme.json)。

### 基础元素

| 元素 | 默认样式 | 目的 |
|---|---|---|
| 时间 | dim + bright black / gray | 提供定位但不抢注意力 |
| `TRACE` | dim gray | 最低优先级 |
| `DEBUG` | bright cyan | 调试信息，与业务成功区分 |
| `INFO` | bright green | 正常成功与生命周期 |
| `WARN` | bold bright yellow | 需要关注但系统仍可继续 |
| `ERROR` | bold bright red | 当前操作失败 |
| `FATAL` | bold bright red；仅 level 标签可选红底 | 进程级不可恢复失败 |
| scope | bright blue | 快速定位组件 |
| message | 默认前景色，可对错误首行加粗 | 保持主体可读 |
| context key | dim gray | 弱化结构标记 |
| context value | 默认前景色 | 保证复制与阅读 |
| error type | bold bright red | 突出错误类别 |
| stack | dim gray | 保留诊断信息但降低噪声 |

使用 ANSI 16 色作为默认语义层最稳妥，因为具体色值由用户终端主题映射。只有项目明确控制终端主题时，才使用固定 256 色或 TrueColor RGB。

### 级别标签必须着色

颜色开启时，至少 `DEBUG`、`INFO`、`WARN`、`ERROR` 必须能仅凭颜色区分。不得只给前面的圆点或图标着色而让 level 本身无差异。

推荐：

```text
DEBUG → cyan
INFO  → green
WARN  → yellow + bold
ERROR → red + bold
FATAL → bright red + bold
```

不要给整行上色。整行绿色、黄色或红色会导致上下文字段难以扫描，也容易污染浅色主题。

---

## 5. 允许的语义强调

除 level 外，只允许少量稳定、可解释的语义着色。

### HTTP status

```text
2xx → green
3xx → cyan
4xx → yellow
5xx → red
```

### duration

当项目已有明确慢操作阈值时：

```text
正常       → 默认前景色
超过慢阈值 → yellow
超过严重阈值 → red
```

### 状态结果

只对有限枚举做语义映射，例如：

```text
completed / ready / healthy → green
retrying / degraded         → yellow
failed / unhealthy          → red
```

禁止根据字符串、数字、布尔值的“类型”做彩虹渲染。随机颜色会破坏稳定视觉记忆。

---

## 6. 时间列

- 本地终端默认 `HH:mm:ss.SSS`；
- 使用 dim gray；
- 宽度固定为 12 个显示单元格；
- 不默认重复日期、时区、服务名和环境；
- 跨天守护进程或审计型 CLI 可通过配置开启日期；
- JSON 始终使用完整 UTC RFC 3339。

不要把时间染成高亮蓝、绿或白色粗体。

---

## 7. Level 列

固定宽度 5：

```text
"TRACE"
"DEBUG"
"INFO "
"WARN "
"ERROR"
"FATAL"
```

实现要求：

- level 文字本身着色；
- `WARN`、`INFO` 右侧补空格；
- 颜色代码不计入列宽；
- 不使用 `I/W/E` 等单字符缩写；
- 不使用不同长度的 `[INFO]`、`[WARNING]` 破坏对齐；
- 不为每条日志额外添加 Emoji 或彩色圆点。

---

## 8. Scope 列

推荐格式：

```text
http.access
db.query
worker.publish
publisher.x
```

规则：

- 使用模块或职责语义，不默认显示完整包名、类名和绝对路径；
- 默认宽度 20；
- 使用 bright blue 或终端主题中的低侵入强调色；
- 短值右侧补空格；
- 超长值使用显示宽度感知的省略号；
- 推荐保留开头领域和末尾组件，例如 `publisher.…worker`；
- 同一 scope 在整个项目中名称稳定。

不允许随机给不同 scope 分配不同颜色。scope 只使用一个统一色。

---

## 9. Message 列

message 应描述“发生了什么”，动态值放 context：

```text
Request completed
Slow query
Publish failed
用户登录成功
```

不要：

```text
Request GET /v1/posts/42 completed in 38.4ms with 200
```

默认宽度 30 个显示单元格：

- 短消息右侧补空格；
- 设计新事件时尽量控制在 30 个显示单元格内；
- 过长时在 Pretty 中用 `…` 截断；
- 完整 `msg` 仍保留在结构化事件和 JSON 中；
- 普通消息使用终端默认前景色；
- ERROR/FATAL 的 message 可加粗，但不整行染红。

---

## 10. Context 列

格式：

```text
key=value key=value key=value
```

推荐色彩：

```text
key   → dim gray
=     → dim gray
value → terminal default
```

字段顺序必须稳定，优先级如下：

1. 本事件核心字段：`method`、`route`、`status`、`operation`、`duration_ms`；
2. 结果字段：`attempt`、`rows`、`size_bytes`、`items_count`；
3. 关联字段：`request_id`、`trace_id`、`job_id`、`task_id`、`account_id`；
4. 其他字段按显式定义或字典序。

不要依赖 map/object 的随机遍历顺序。

### 字符串

无空格和特殊字符：

```text
status=ready
```

有空格、换行或歧义：

```text
reason="rate limit exceeded"
```

### 数字与布尔值

```text
status=200 attempt=2 cached=true
```

不要加无意义引号。

### 耗时

结构化事件保留 `duration_ms` 数值；Pretty 可人性化：

```text
38.4ms
1.28s
2m14s
```

### 字节

结构化事件保留 `size_bytes` 数值；Pretty 可显示：

```text
842B
1.4MiB
2.1GiB
```

### ID

- 默认完整显示，便于复制查询；
- 放在 context 后部；
- 不使用随机颜色；
- 只有交互式 UI 明确提供复制完整值时才允许缩写。

### 对象和数组

- 小对象可用紧凑 JSON；
- 大对象改为摘要字段，例如 `items_count=128`；
- 不在普通日志中多行 pretty-print 对象；
- 不让对象展开破坏一事件一行。

---

## 11. 错误与堆栈

错误首行仍遵守标准列布局：

```text
13:42:21.311  ERROR  publisher.x           Publish failed                  account_id=acc_7 attempt=2
              ╰─ TimeoutError: upstream timed out after 10s
                 at publisher/client.ts:184
                 at worker/run.ts:72
```

颜色：

- 首行 level：bold bright red；
- 首行 message：默认前景色或 bold；
- `╰─` 与错误类型：bright red；
- 错误 message：默认前景色；
- stack frame：dim gray；
- 关键 cause 链可逐级缩进，但默认不超过合理深度。

规则：

- `╰─` 仅用于错误详情，不用于普通日志；
- 不重复打印同一个错误 message；
- JSON 中 stack 保持字符串，换行由 JSON 转义；
- WARN/INFO 默认不打印完整堆栈；
- 无 UTF-8 能力时退化为 `|-`；
- 同一异常只在拥有 retry、response、fail、exit 或 recovery 结果的边界记录一次。

---

## 12. 颜色开关与优先级

项目应提供语义等价配置：

```text
LOG_COLOR=auto|always|never
```

推荐优先级：

1. `LOG_COLOR=always`：Pretty 强制颜色；JSON 仍禁止 ANSI；
2. `LOG_COLOR=never`：关闭颜色；
3. `NO_COLOR`：关闭颜色；
4. `FORCE_COLOR`：开启颜色；
5. `auto`：仅交互式 TTY 且 `TERM != dumb` 时开启。

`LOG_FORMAT=json` 时，无论任何颜色变量都不得输出 ANSI。

默认行为：

```text
TTY + Pretty + 非 production → Color ON
NO_COLOR                    → Color OFF，列布局保留
非 TTY / 重定向             → Color OFF 或直接 JSON
TERM=dumb                    → Color OFF
```

---

## 13. 终端宽度模式

默认完整模式适合约 120 列及以上终端。

推荐支持：

| 模式 | scope | message | 说明 |
|---|---:|---:|---|
| full | 20 | 30 | 默认，美观且信息完整 |
| compact | 14 | 22 | 适合 80–119 列 |
| minimal | 12 | 不固定 | 极窄终端，只保留关键 context |

可提供：

```text
LOG_PRETTY_MODE=auto|full|compact|minimal
```

`auto` 可根据可获取的终端宽度选择模式。无法可靠获取宽度时使用 full，不要逐行抖动布局。

普通事件不应由 formatter 任意拆成多行。极窄终端允许终端自身自然换行，但 formatter 仍输出一个物理行。

---

## 14. 禁止的视觉做法

不要：

- 每条日志前添加 Emoji；
- 启动时打印大型 ASCII Logo；
- 用方框包住每个事件；
- 给整条 INFO 涂绿、整条 ERROR 加红底；
- 每个 key 使用不同颜色；
- 随机给 scope 分配颜色；
- 把对象展开为十几行彩色文本；
- 使用 Tab 对齐；
- 用字节长度代替终端显示宽度；
- 让 ANSI 代码参与 padding 计算；
- 在重定向文件或 JSON 中留下 ANSI；
- 为了视觉整齐隐藏错误码、完整异常类型或关联 ID；
- 接受一个明显不对齐的默认 formatter，仅因为它来自官方库。

---

## 15. 必测快照

至少添加以下 Pretty golden/snapshot tests：

1. `TRACE/DEBUG/INFO/WARN/ERROR/FATAL` 六种 level；
2. 去掉 ANSI 后各列起始位置一致；
3. 每个 level 在颜色模式下具有预期 SGR 语义；
4. `NO_COLOR`、非 TTY、`TERM=dumb` 不包含 ANSI；
5. JSON 永远不包含 ANSI；
6. 英文、中文、中英混合 message 对齐；
7. 超长 scope 和 message 正确显示 `…`；
8. context 字段顺序稳定；
9. 正常事件为一个物理行；
10. 错误首行、错误类型和 stack 缩进稳定；
11. 2xx/4xx/5xx 或慢耗时语义强调符合项目阈值；
12. 关闭颜色后日志仍清晰整齐。

运行参考预览：

```bash
python packages/backend-logging/scripts/preview_terminal_theme.py --force-color
python packages/backend-logging/scripts/preview_terminal_theme.py --no-color
```

预览脚本只是视觉参考。目标项目仍应使用其语言生态的 logger/formatter 实现同一契约。
