# 精密工作台设计规范 (Precision Workbench)

> 一套面向桌面工具、运营后台和复杂编辑器的浅色高密度设计语言：固定工作区、清晰边界、紧凑控件、极少装饰。
> 适用于需要同时呈现导航、主任务、状态和辅助面板的专业产品。

随附可直接复制的 `tokens.css`、`globals.css` 和 `tailwind.config.ts`；测试记录见 [`tests/design-system/precision-workbench`](../../../tests/design-system/precision-workbench/)。

---

## 0. 一条总原则

**先固定任务结构，再用密度和边界帮助扫描；装饰永远不与状态争夺注意力。**

任何新增元素都应回答三个问题：它属于哪个工作区、用户能否快速扫到、状态变化是否可被理解。答不出来就删掉。

## 1. 风格画像

### 核心关键词

- **精密**：尺寸、对齐和控件状态严格落在少量 Token 上。
- **高密度**：正文以 14px 为基准，元数据和控件以 12–13px 为主。
- **中性**：白、近黑和灰承担绝大多数界面面积。
- **边界驱动**：细边框和 Surface 切分区域，阴影仅属于浮层。
- **层级可扫描**：固定侧栏、主任务区和辅助面板各自承担稳定职责。
- **桌面工具感**：优先鼠标、键盘和宽屏并行任务，不模拟移动原生界面。
- **状态明确**：选中、错误、成功、运行中均有文字或图标，不只靠颜色。

### 反向关键词

营销感、沉浸式、松软、卡通、玻璃化、强色块。

### 第一视觉印象

像一张组织严密的工作桌：结构先于品牌，信息先于装饰，所有区域都能迅速定位。信息密度偏高，但通过留白、细分隔线和固定列宽避免拥挤。

紫色只作为定位信号——选中图标、少量 Agent 标识和非错误提醒；主操作仍用近黑填充，避免整页被品牌色淹没。

### 与 Quiet Native 的差异

| 维度 | Precision Workbench | Quiet Native |
|---|---|---|
| 主要设备 | 桌面工作区，最小约 760px | 移动优先的 Web/PWA |
| 信息密度 | 高，12–14px UI 文本 | 中低，15–17px UI 文本 |
| 导航 | 200px 固定侧栏，窄屏收为 72px | 移动底栏，宽屏再转侧栏 |
| 层级表达 | 细边框、固定列、表格和列表 | Grouped Surface、留白、原生感 |
| 控件 | 32/36/40px 紧凑高度 | 至少 44px 触控高度 |
| 浮层 | 实色白底 + 克制阴影 | 可使用控制层毛玻璃 |
| 主题 | 仅浅色 | 浅色和深色成对提供 |

## 2. 什么时候使用

### 适合

- 桌面运营台、内部工具和专业后台。
- 编辑器、文件管理器、任务编排器和 AI 工作台。
- 同屏需要导航、列表/画布、状态栏和上下文辅助面板的产品。
- 强调扫描效率、键盘操作和多任务切换的界面。

### 不适合

- 390px 手机作为主要设备的消费产品。
- 营销页、品牌活动页或需要大幅视觉叙事的产品。
- 游戏、娱乐、儿童产品或强沉浸体验。
- 已明确要求完整深色主题的产品。

## 3. 反模式

| 不要做 | 应该改成 |
|---|---|
| 用紫色填满主按钮、标题和大面积背景 | 主按钮用近黑；紫色只标记当前选择或辅助智能能力 |
| 每个区块都做悬浮卡片 | 先用工作区列和 1px 分隔线；只有独立任务单元才加边框 |
| 用阴影区分普通列表行 | 用 `--border`、背景变化和固定对齐线 |
| 把 12–14px 字号继续压小来塞内容 | 保留字号，改用截断、展开详情或稳定列宽 |
| 把右侧辅助面板永久压缩到不可读 | 低于 900px 时改为覆盖面板并提供遮罩和关闭动作 |
| 把桌面侧栏直接改成手机底栏 | 若手机是核心设备，改用移动优先的设计系统 |
| 用 Badge 堆满来源、状态、排名和时间 | 先用一行元数据和分隔符；只让异常或主状态突出 |
| 为页面切换加入滑动、缩放或弹跳 | 页面立即切换，仅浮层使用 120–150ms 淡入/微缩放 |
| 在普通 Surface 上使用毛玻璃 | 使用实色背景；本风格不使用毛玻璃 |

## 4. 色彩系统

### 基础层级

| Token | 默认值 | 用途 |
|---|---|---|
| `--bg-primary` | `#ffffff` | 页面与主画布 |
| `--bg-surface` | `#ffffff` | 卡片、输入区、列表和面板 |
| `--bg-elevated` | `#ffffff` | Dialog、Popover、Drawer |
| `--bg-secondary` | `#fafafa` | 侧栏、表头、次级区域 |
| `--bg-muted` | `#f5f5f5` | Hover、选中轨道、代码块 |
| `--text-primary` | `#171717` | 标题、正文和主操作 |
| `--text-secondary` | `#737373` | 描述、元数据、未选状态 |
| `--text-tertiary` | `#a3a3a3` | 占位和低优先级状态 |
| `--border` | `#e5e5e5` | 默认边框与分隔线 |
| `--border-strong` | `#d4d4d4` | Hover 或需要额外识别的边界 |

### 强调与状态

- `--accent` 仅用于选中图标、当前能力、链接定位或非错误提醒，不作为所有 Primary Button 的默认填充。
- Primary Button 使用 `--text-primary` 背景与 `--text-on-strong` 文字。
- 成功用绿、错误/破坏性操作用红；警告沿用紫色提示语法，并必须附带文字。
- 状态软背景只用于小范围提示、Diff 行或错误区域，禁止铺满主画布。
- 推荐面积比例：中性色约 95%，强调和状态色合计不超过 5%。

所有组件只消费语义 Token。禁止在组件里新增十六进制色值；品牌替换只改 `--accent`、`--accent-soft` 及其交互派生值。

## 5. 字体与排版

本包不携带字体文件。默认使用 Inter（环境已有时）和系统中文无衬线回退：

```css
font-family: Inter, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
```

| 层级 | Token | 规则 |
|---|---|---|
| 页面标题 | `--font-size-2xl` / 24px | 600，行高 1.25 |
| 面板标题 | `--font-size-xl` / 20px | 600，少量使用 |
| 区块标题 | `--font-size-lg` / 16px | 600 |
| 默认正文 | `--font-size-md` / 14px | 400，行高 1.5 |
| 控件/列表 | `--font-size-sm` / 13px | 400–600 |
| 元数据 | `--font-size-xs` / 12px | 400–600 |
| 极短分组标签 | 10px | 600，可加 `0.08em` 字距；不得用于正文 |

中文与英文共用字号层级；中文标题不要依赖过紧字距。数字统计、排名、时间和表格金额使用 `font-variant-numeric: tabular-nums`。代码、命令和标识符使用系统等宽字体。

衬线字体不是本风格的稳定特征。连续长文可按业务单独选择，但不能把衬线斜体当装饰性强调。

## 6. 间距与密度

基础网格为 4px，只使用 `4 / 8 / 12 / 16 / 20 / 24 / 32 / 40`。

| 场景 | 建议值 |
|---|---|
| 页面主内容内边距 | 24px |
| 页面大区块间距 | 24–32px |
| 区块标题到内容 | 12–16px |
| 卡片内边距 | 12–16px |
| 紧凑列表行 | 32px |
| 主导航行 | 38px |
| 小/中/大控件 | 32 / 36 / 40px |
| Dialog 内边距 | 24px |

密度模式只允许通过控件高度和纵向 Padding 成组切换：紧凑 `32px`、默认 `36px`、宽松 `40px`。不要在同一工具栏混用三个高度，也不要出现 13px、17px、27px 等随机间距。

## 7. 圆角、边框、阴影和模糊

| 对象 | 圆角 | 其他规则 |
|---|---:|---|
| 小菜单项、紧凑标签 | 6px | 无阴影 |
| Input、Button、列表选择 | 8px | 1px 边框 |
| Card、Table 容器 | 8–10px | 普通状态无阴影 |
| Dialog、Drawer、Popover | 14px | 实色背景 + 浮层阴影 |
| Avatar、状态圆点 | 50% / full | 只用于真正的圆形对象 |

- 普通 Surface 不使用阴影。
- 轻控件选中态只允许 `0 1px 2px` 的极浅阴影。
- Popover、Dialog、Drawer 分别使用 `--shadow-popover`、`--shadow-dialog`、`--shadow-drawer`。
- 不使用模糊和毛玻璃；浮层用不透明白色保证复杂内容可读。

## 8. 布局系统

### 应用 Shell

```text
┌─ 200px Sidebar ─┬──────────── Main Workspace ────────────┬─ Assistant ─┐
│ 40px app tab    │ 40px browser/title strip              │ header      │
│ navigation      │ scrollable feature stage              │ timeline    │
│ resources       │ primary task                          │ composer    │
│ user footer     │ 32px runtime status                    │             │
└─────────────────┴─────────────────────────────────────────┴─────────────┘
```

- 侧栏宽 200px，背景 `--bg-secondary`，右侧 1px 分隔线。
- 顶部标签/标题条高 40px；状态栏高 32px。
- 主 Feature 默认 24px 内边距并独立滚动。
- 带辅助面板的页面使用 `minmax(0, 1fr) minmax(300px, 30%)`；辅助面板不是内容卡片，而是稳定职责列。
- 首页内容最大宽 1120px，核心任务区最大宽 960px；资源页可放宽到 1280px。
- 编辑器和文件管理器允许取消主区 Padding，用 210–248px 的内部目录列与画布并排。
- 表单默认单列，字段宽度由任务约束，账号安全类表单建议不超过 440px。

## 9. 视觉层级

```text
Level 0  Canvas：页面背景
Level 1  Structural Surface：侧栏、主区、辅助列，以分隔线切分
Level 2  Task Surface：卡片、表格、输入区，1px 边框
Level 3  Sticky Control：工具栏、编辑器控制条、局部状态条
Level 4  Floating Layer：Dropdown / Popover / Assistant Overlay
Level 5  Blocking Layer：Dialog / Drawer + Overlay
```

Level 1 可以包含多个 Level 2，但不要在 Card 内继续套同样边框和圆角的 Card。Level 3 只为保持任务上下文，不得用阴影伪装成悬浮内容。Level 4/5 才允许明显阴影。

## 10. 核心组件契约

### Button

- Primary：近黑背景、白字、8px 圆角；每个任务区最多一个。
- Secondary：白底 + 默认边框；用于取消、刷新或替代路径。
- Ghost：透明底，Hover 进入 `--bg-muted`；适合工具栏和导航。
- Danger：红底白字，只用于不可恢复或高风险确认。
- 状态必须覆盖 Hover、Active、Focus-visible、Disabled 和 Loading；Loading 保留按钮宽度。

### Input / Select / Textarea

- Input 紧凑高度 32px，普通表单可用 36–40px；统一 8px 圆角和 1px 边框。
- 标签常显，Placeholder 只提供示例，不替代标签。
- Focus 同时改变边框并显示 3px 低透明焦点环。
- Textarea 默认最小 80px，可纵向调整；编辑器正文由画布控制，不嵌套第二个滚动区。
- Select 的 Trigger 与相邻控件同高；Popover 最高不超过可用视口。

### Checkbox / Switch

- 优先原生控件，视觉尺寸 18px，保留键盘和高对比模式行为。
- 开关旁始终有动作名称；复杂后台任务另附当前状态和隐私/副作用说明。

### Tabs

- 页面级 Tabs 使用文字 + 底部 2px 当前指示线，不使用大面积紫底。
- 紧凑分段控件可用 `--bg-muted` 轨道和白色活动块，仅用于互斥视图。
- 当前项同时设置 `aria-selected` 或 `aria-current`。

### Navigation

- 主侧栏一行 38px，图标 17px，文字 13px。
- 活动项白底、文字 600、图标 Accent，并可加极浅 `--shadow-control`。
- 子导航行高 32px、图标 14px；用左分隔线表达层级。
- 分区标签 10px、大写或适度字距，只用于少量导航分组。

### Card / List Row / Table

- Card 是独立任务单元：白底、1px 边框、8–10px 圆角，无默认阴影。
- List Row 通过统一列、截断和 Hover 背景支持快速扫描；不要为每个字段加 Badge。
- Table 外层允许 10px 圆角和横向滚动；表头用 `--bg-secondary`，行只保留水平分隔线。
- 单元格默认 `12px 16px`；数字右对齐并启用 tabular nums。
- 窄屏无法保留关键列时，改成定义列表/行详情，不把整张表缩成不可读字体。

### Badge

只用于短状态、权限或不可从上下文判断的类别。默认用文字色 + 软背景；来源、时间、排名等普通元数据写成一行，不做胶囊墙。

### Dropdown

- 4px 内边距、10px 圆角、1px 边框和 `--shadow-popover`。
- 菜单项至少 32px 高，当前项用 Muted 背景；危险项用红色文字且与普通项分隔。
- Escape 关闭，关闭后焦点回到 Trigger。

### Modal / Dialog

- 使用框架可访问 Dialog 或原生 `<dialog>`，禁止 `window.alert` / `window.confirm`。
- 宽度不超过 `min(32rem, 100vw - 32px)`，最大高度为视口减 32px并允许内容滚动。
- 标题、说明、正文和右对齐动作区顺序固定；关闭按钮必须有可访问名称。
- 仅 Dialog 使用 `--shadow-dialog`，遮罩使用 `--overlay`。

### Drawer / Sheet

- 桌面设置优先右侧 Drawer，宽约 400–440px；从来源方向进入，使用 `--shadow-drawer`。
- 低于 900px 的辅助面板宽度为 `min(360px, 100% - 48px)`，配遮罩和关闭按钮。
- 本风格不使用移动端底部 Sheet 作为主要导航。

### Toast / Banner

- 局部结果优先就地写在动作附近，成功状态可自动消退。
- 全局阻断、离线或跨页面任务才使用 Banner/Toast。
- 错误必须包含发生了什么和下一步，不能只写“失败”。

### Empty / Loading / Error

- Empty：在所属区域居中，使用标题 + 一句说明 + 最多一个下一步，不放大插画。
- Loading：保留最终布局轮廓；小区域可用 14–16px 线性 Spinner，周期 800–900ms。
- Error：`role="alert"`、错误文字、可恢复动作；不要仅用红边框。
- Disabled：降低到 40% 不透明度，并保留可解释的原因文本或 Tooltip。

## 11. 图标与媒体

- 使用单色线性图标，默认 14–17px，主入口可到 24px。
- 描边、圆角端点和 ViewBox 必须来自同一图标集；不混用手绘 SVG。
- 未选图标使用 `--text-secondary`，选中图标使用 `--accent`。
- 彩色平台图标、品牌 Logo 和插画不属于本设计系统，需由业务层提供。
- Avatar 为 32–40px 圆形；无图片时用姓名首字占位，不生成装饰头像。
- 资源缩略图使用稳定比例和 `object-fit: cover`；缺失媒体用中性类型占位，不拉伸原图。

## 12. 交互与动效

| 状态 | 规则 |
|---|---|
| Hover | 背景从透明变 Muted，或边框从默认变 Strong |
| Active | 延续 Hover 并轻微加深；不做大幅缩放 |
| Focus | 3px 低透明焦点环，不能被 `outline: none` 无替代地移除 |
| Selected | 白底/Muted + 600 字重 + Accent 图标或 2px 指示线 |
| Disabled | 40% 不透明度、默认光标、禁止触发 |
| Loading | Spinner + 动词进行态，区域尺寸不跳变 |

- Hover、边框和颜色反馈用 120ms `ease`。
- Dialog/Popover 用 120–150ms `ease-out`，仅透明度与 `scale(0.98 → 1)` 或 2% 位移。
- 页面和主导航切换不做空间转场。
- 无限动效仅限 Spinner、进度或流式光标。
- `prefers-reduced-motion: reduce` 下把动画/过渡压到 0.01ms，Spinner 只保留静态状态文字。

## 13. 响应式规则

本风格是**桌面优先**，不是手机优先。

| 断点 | 行为 |
|---|---|
| `> 1100px` | 主内容 + 至少 300px/30% 辅助列 |
| `≤ 1100px` | 辅助列最小约 260px，非关键大纲可隐藏 |
| `≤ 900px` | 主侧栏收为 72px 图标栏；辅助列改为覆盖面板 |
| `≤ 760px` | 工具栏和资源页多列改为单列；这是已验证的桌面最小宽度 |
| `≤ 620px` | 表单、卡片和元数据可堆叠；不代表完整手机导航已经成立 |

- 1440×900 与 760×520 是推荐验收视口。
- 点击区域在鼠标优先桌面可使用 32–40px；若产品进入触屏场景，改 `--control-height-*` 至至少 44px。
- 超长标题和账号信息单行截断，并提供完整值的可访问名称或详情入口。
- 主画布不得产生页面级横向滚动；只有表格、代码块和画布可在自身区域横向滚动。
- Web/PWA 若运行在带刘海设备，另加 safe-area 适配；来源项目没有该约束。

## 14. 深色模式

来源项目只实现浅色主题，因此本包**不伪造深色 Token**，`color-scheme` 固定为 `light`。

需要深色时，不要只反转黑白：必须重新验证 Surface 层级、边框对比、状态软背景、浮层阴影、媒体亮度和系统控件，并为所有语义 Token 提供成对值后再启用主题切换。

## 15. 可访问性

- 正文与背景至少满足 WCAG AA；12px 元数据只能用于非关键辅助信息。
- 所有交互保留 `:focus-visible`，焦点不能被 Sticky Toolbar 或浮层遮挡。
- 图标按钮必须有 `aria-label`；纯装饰图标使用 `aria-hidden="true"`。
- Tabs、列表选择和菜单分别使用 `aria-selected`、`aria-current`、`role` 等正确语义。
- Dialog 支持 Escape、焦点约束和关闭后焦点恢复；危险动作有明确标题、说明和 Danger Button。
- 加载、保存和异步结果使用 `role="status"` / `aria-live="polite"`；错误使用 `role="alert"`。
- 状态不能只靠颜色：同时给出文字、图标、形状或位置变化。
- 触屏消费者把点击区域提升到至少 44×44px；桌面紧凑模式不能直接视为触屏合格。
- Reduced Motion 和系统高对比模式必须保留功能；原生表单控件优先于自绘替代。

## 16. 落地到新项目

1. 复制 `tokens.css`、`globals.css` 和 `tailwind.config.ts` 到同一前端项目。
2. 入口按顺序引入：

   ```ts
   import './styles/tokens.css'
   import './styles/globals.css'
   ```

3. 修改 `tailwind.config.ts` 的 `content` 路径；若使用 Tailwind 4，可把映射迁入项目现有 `@theme`，不要同时维护两份值。
4. 只改 `--accent` 与 `--accent-soft` 替换品牌定位色；Primary Button 仍保持中性近黑，除非品牌明确要求改变操作层级。
5. 从 App Shell 开始：200px 侧栏、主区、可选辅助列和 32px 状态栏；再实现页面组件。
6. 组件只使用 `bg-canvas / bg-surface / bg-subtle / text-ink / text-ink-secondary / border-border / text-accent` 等语义类名。
7. React、Vue、Svelte 或原生 HTML 均可复用 Token；Dialog、Popover、Focus 管理按项目框架选择成熟原生/既有方案。
8. 需要手机或深色主题时应作为明确扩展单独验收，不要假设本包已经覆盖。

## 17. 一页速查

```text
风格      浅色、桌面优先、高密度、边界驱动
字体      Inter/系统无衬线；12/13/14/16/20/24
背景      #fff Canvas → #fafafa Structural → #fff Task Surface
文字      #171717 / #737373 / #a3a3a3
强调      #8b5cf6，仅定位选中和辅助能力；Primary 仍用近黑
间距      4px 网格；页面 24；区块 24–32
控件      32/36/40px；触屏项目提升到 ≥44px
圆角      6/8/10/14/full
边界      普通层用 1px #e5e5e5；Hover #d4d4d4
阴影      只给 Popover/Dialog/Drawer
布局      Sidebar 200→72；Assistant 30%→Overlay
动效      120/150ms；只表达浮层和状态
主题      仅浅色，不提供推测的 Dark
禁令      无卡片套卡片、无玻璃、无 Badge 墙、无紫色泛滥
```

## 18. 来源与抽象边界

### 来源

- 来源项目：AutoUp-On（仅用于分析，不构成本风格名称）。
- 分析 Commit：`510132af0462a2bccd421ae264a7edab3a393982`。
- 许可证：Desktop 包声明 `UNLICENSED`，仓库未发现根级 LICENSE；因此只提炼抽象规律，所有骨架均重新编写。
- 实际检查：登录页、首页、热点列表、右侧 Agent 面板；视口为 1440×900 与 760×520。
- 运行方式：Vite 生产构建 + Desktop Bridge 测试替身；验证的是 Renderer 布局与交互状态，不替代真实 Electron/Cloud 集成测试。

### 关键证据

| 观察 | 路由/区域 | 文件或选择器 | 证据 | 结论 | 置信度 |
|---|---|---|---|---|---|
| 中性色和紫色定位 | 全局 | `shared/ui/tokens/colors.css`、`themes/light.css` | 灰阶 + `#8b5cf6`，Primary Button 仍为近黑 | Accent 是定位信号，不是主面积色 | 高 |
| 4px 网格和紧凑控件 | 全局 | `shared/ui/tokens/spacing.css` | 4–40px 间距；32/36/40px 控件 | 高密度桌面基线 | 高 |
| 12–14px UI 字体 | 全局 | `shared/ui/tokens/typography.css` | xs 12、sm 13、md 14 | 快速扫描优先 | 高 |
| 固定工作台壳 | 首页/热点 | `.workbench-shell`、`.workspace` | 200px 侧栏、40px 顶栏、32px 状态栏 | 结构层级先于卡片 | 高 |
| 窄屏收栏 | 首页 760×520 | `@media (width <= 900px)` | 侧栏收为 72px，文字隐藏，无横向溢出 | 桌面窄窗而非手机重排 | 高 |
| 辅助上下文列 | 热点 | `.workspace-content`、`.assistant-panel` | 至少 300px/30%；窄屏变右侧 Overlay | 辅助任务保持独立职责 | 高 |
| 边框而非阴影分层 | 首页/热点 | `.home-assistant`、`.radar-card` | 1px 边框、白底、普通状态无阴影 | Task Surface 依赖边界 | 高 |
| 简短浮层动效 | Dialog/Select | `shared/ui/components/components.css` | 120–150ms fade/scale | 只给浮层和状态反馈 | 高 |
| 原生 Dialog 语法 | 多个管理页面 | `account-add-dialog`、`command-palette.tsx` | `<dialog>` + labelledby + 关闭按钮 | 阻断操作统一可访问浮层 | 高 |
| 深色缺失 | 设计系统 | `themes/light.css`、模块 README | 仅 `color-scheme: light` | 不推测 Dark Token | 高 |

### 归一化和推断

- **直接提取**：基础颜色、字号、间距、圆角、控件高度、主要布局宽度、断点、浮层时长和 z-index 层级。
- **归一化**：将项目内部 `background/foreground/brand` 命名对齐 devkit 的语义接口；Accent Hover/Active 由 `color-mix()` 从同一基色派生；把来源中的提示色语法统一为 `warning`。
- **推断**：Toast/Banner、跨框架落地和触屏扩展未在实际页面完整呈现，规则来自相邻状态模式与可访问性边界，使用时需按业务验证。
- **主动排除**：项目名、产品文案、平台 Logo、平台 SVG、账号数据、业务状态名、专有组件实现和任何凭据/Session 数据。
- **字体处理**：未复制来源字体文件；Token 使用字体名称和系统回退，消费者自行确认字体来源或直接使用系统栈。

最终检验：换成实验室库存、财务审核或代码发布等完全不同业务后，界面仍应像一套精密桌面工具，而不是来源产品的换皮。
