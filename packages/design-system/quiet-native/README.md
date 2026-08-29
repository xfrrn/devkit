# 静谧原生设计规范 (Quiet Native Design System)

> 一套可跨项目复用的通用 Web/PWA 界面风格（devkit · `packages/design-system/quiet-native`）。
> 目标气质：**iOS 系统界面 × Apple Settings × App Store**——安静、克制、秩序清晰，像自然生长在设备里的产品，而不是套模板的网页。
>
> 本规范附带可直接拷贝的代码骨架：`tokens.css` + `tailwind.config.ts` + `globals.css`。
> 用法见 §14；这是 devkit 的 `design-system` package 中的一套风格规范，根级说明见仓库 `README.md`。
> 测试用例见 [`tests/design-system/quiet-native`](../../../tests/design-system/quiet-native/)。

---

## 0. 一条总原则

**任务 > 信息 > 交互 > 排版 > 装饰。**

任何视觉元素，如果不能帮助用户「识别信息、完成任务、理解状态或继续操作」，就应该被删掉。

判断一个新设计对不对，只看一句：**它退后了吗？** 界面永远退后，让当前任务、关键信息和主要操作成为视觉主体。

---

## 1. 什么时候用这套系统

**适合：**
- 工具、内容、服务、效率类产品
- 移动端优先、同时需要适配桌面端的 Web App / PWA
- 需要「原生 iOS 气质」而不是「Web 后台气质」的界面

**不适合：**
- 极高信息密度的 Dashboard / 专业工作台
- 营销页 / 落地页（需要强视觉刺激的场景）
- 游戏、沉浸式体验或以品牌视觉为主体的产品

---

## 2. 反模式（先说不该做什么）

很多 Web 产品会不自觉地犯这些错。这套系统的价值一半在于**明确禁止**：

| 不要做 | 改成 |
|---|---|
| 大面积彩色渐变、紫到粉 | 中性色为主，只有一个克制的品牌母题 |
| 卡片套卡片套按钮框 | 严格四层视觉层级（见 §9） |
| 每个元素都带阴影、描边 | 普通卡片无阴影，靠背景+分隔线分层 |
| 五六个蓝色按钮抢注意力 | 一个页面最多一个 Primary Action |
| 黄色马克笔式高亮 | 重点信息只改颜色+字重，不滥加底色 |
| 满屏 Badge / 标签 | 状态用文字 + 图标表达，必要时才用标签 |
| 内容卡片用毛玻璃 | Glass 只属于控制层（导航/Sheet/Toolbar） |
| 旋转、弹跳、缩放特效 | 动画只表达物理关系，不炫技 |
| 13px / 27px 这种随机间距 | 只允许 4px 网格上的整数倍 |

---

## 3. 色彩

**90% 中性色 + 10% 强调色。** 强调色只用于：链接、选中态、Primary Action、可点击重点。

所有颜色必须使用语义 Token，组件里**禁止写死十六进制**。

### Light
| Token | 值 | 用途 |
|---|---|---|
| `--bg-primary` | `#F2F2F7` | 页面背景 (systemGroupedBackground) |
| `--bg-surface` | `#FFFFFF` | 卡片 / 列表项 (secondarySystemGroupedBackground) |
| `--bg-secondary` | `#E9E9EE` | 填充控件、分段控件轨道 |
| `--text-primary` | `#1C1C1E` | 主要文字（近黑，不用纯黑） |
| `--text-secondary` | `#6E6E73` | 次级信息 |
| `--text-tertiary` | `#A9A9AE` | 时间、辅助信息 |
| `--separator` | `rgba(60,60,67,.12)` | 分隔线（发丝线） |
| `--accent` | `#007AFF` | 主交互色（可整体替换为品牌色） |
| `--danger` / `--success` | `#FF3B30` / `#34C759` | 错误 / 完成 |

### Dark（第一版就支持，不是后补）
| Token | 值 |
|---|---|
| `--bg-primary` | `#000000` |
| `--bg-surface` | `#1C1C1E` |
| `--bg-secondary` | `#2C2C2E` |
| `--text-primary` | `#F2F2F7` |
| `--text-secondary` | `#98989D` |
| `--text-tertiary` | `#636366` |
| `--separator` | `rgba(84,84,88,.60)` |
| `--accent` | `#0A84FF` |

**深色模式不是简单的「白变黑」**——文字、分隔线、强调色的透明度都要单独调（深色下分隔线更不透明，浅色下几乎不可见）。所有配对值已在 `tokens.css` 的 `:root.dark` 里备好。

> **换成你的品牌色**：只需改 `--accent` 一族（`accent` / `accent-active` / `accent-soft` / `accent-softer`），浅深两套各一组，共 8 个变量。其余全部不用动。

---

## 4. 字体与排版

不打包任何字体，用系统字体栈（iOS 上自然得到 SF Pro / 苹方）：

```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
             "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
```

系统无衬线是默认字族，也是这套风格的主体。衬线字只是一种**可选的长内容模式**，不用它也不影响“静谧原生”的成立。

```css
--font-content: ui-serif, "Songti SC", "Noto Serif CJK SC", Georgia, serif;
```

| Token | 字号 | 字重 | 用途 |
|---|---:|---:|---|
| `large-title` | 32 | 700 | 页面主标题 |
| `title-1` | 26 | 700 | 详情页大标题 |
| `title-2` | 21 | 600 | 段落标题 |
| `headline` | 17 | 600 | 卡片标题 |
| `body` | 17 | 400 | 正文（UI 无衬线） |
| `body-serif` | 17 | 400 / lh 1.78 | 可选长文正文（衬线） |
| `callout` | 16 | 400 | 次要正文、补充说明 |
| `subheadline` | 15 | 400 | 辅助信息 |
| `caption` | 13 | 400 | 时间、状态 |

**使用规则：**
- 导航、表单、按钮、列表、数据和普通正文统一用无衬线。
- 文章、文档等连续长内容可选 `body-serif`，行高 1.78。
- 不要为了“高级感”混用字族；只有内容类型需要时才启用衬线。

---

## 5. 间距（4px 网格）

只允许这些值：`4 8 12 16 20 24 32 40 48`

| 场景 | 间距 |
|---|---|
| 页面左右边距 | 移动端 16；宽屏 24–32 |
| 大区块之间 | 24–32 |
| 标题 → 内容 | 12 |
| 列表项内边距 | 12–16 |
| 正文段落间距 | 12 |

**禁止**出现 `13px / 17px / 27px` 这种随机值。

---

## 6. 圆角

```text
8px   小型控件
12px  Input / Button
16px  Card
20px  Sheet / Modal
999px Pill / 底部胶囊导航
```

默认卡片 16px。不要把所有东西做成巨大圆角。

---

## 7. 阴影与分层

Apple 风格的关键不是「大阴影」，而是**层级极轻**。

- **普通卡片：无阴影。** 靠 `背景 + Surface + 分隔线` 三层区分。
- 只有浮层（Sheet、悬浮导航、下拉）才允许阴影：
  - `--shadow-control`（控件，几乎不可见）
  - `--shadow-sheet`（底部弹层，向上）
  - `--shadow-float`（悬浮导航）

---

## 8. Glass / 毛玻璃

**Glass 是控制层，不是内容层。**

只允许出现在：**底部导航、顶部浮动工具栏、Modal / Sheet**。
**内容卡片禁止用 Glass。**

```css
.glass-surface {          /* 通用：Sheet / 工具栏 */
  background: var(--glass-bg);
  backdrop-filter: saturate(var(--glass-saturate)) blur(var(--glass-blur));
}
.glass-nav {              /* 底部悬浮胶囊导航（参考 Apple Arcade） */
  background: var(--glass-nav-bg);
  backdrop-filter: saturate(var(--glass-saturate)) blur(var(--glass-blur));
  border: 0.5px solid var(--glass-nav-border);
  box-shadow: var(--shadow-float);
}
```

玻璃参数（模糊度、饱和度、不透明度）浅深两套都在 `tokens.css` 里——深色下模糊更小、背景更深。

---

## 9. 视觉层级（严格四层）

```text
Level 0   页面背景 (--bg-primary)
Level 1   内容 Surface (--bg-surface，列表、表单、卡片)
Level 2   Navigation / Toolbar（Glass 控制层）
Level 3   Modal / Sheet（Glass + 阴影）
```

**禁止**「卡片里套卡片、卡片里再套一个带框按钮」。每多一层无意义嵌套，原生感就丢一分。

---

## 10. 核心组件

下列组件只给契约（结构 + 关键类名），照着即可在任何项目里复刻。

### InsetGroup（分组列表）— 同类信息的统一语言
Apple Settings 的 inset-grouped：一个圆角白卡片浮在灰背景上，行与行之间用发丝分隔线，整组一个容器。

```tsx
<div className="overflow-hidden rounded-md bg-surface">
  <div className="divide-y divide-hairline">{rows}</div>
</div>
```

连续、同构的信息优先用 List；只有多个入口地位相同、需要并列浏览时才用 Card Grid。

### SectionLabel（分区小标签）
```tsx
<div className="px-4 pt-6 pb-2 text-caption-medium text-ink-secondary">{children}</div>
```

### 列表行（List Row）
内容左对齐、可截断，需要进入下一级时右侧放 `›` chevron，按下整行轻弹（见 §11 触控反馈）。
**内容本身就是 UI**：标题、摘要、状态、时间足够表达时，不再添加装饰和标签堆。

### SegmentedControl（分段控件，带滑动块）
选中项不是瞬间跳变，而是一个白色滑块在选项间**平滑滑动**（实测 DOM 宽度+位移）。轨道用 `bg-subtle`，滑块用 `bg-surface` + `shadow-control`。这是贴合 iOS 的关键细节之一。

### Bottom Navigation（悬浮玻璃胶囊）
参考 Apple Arcade：不是贴底的整宽 bar，而是一个**悬浮圆角胶囊**，内容从下方透出。

- 胶囊 `rounded-full` + `glass-nav`，高约 58px，距底 `safe-area + 10px`。
- 3–5 个 Tab：图标（线性/filled 两态）+ 10px 文字。
- 选中 = accent 图标 + accent 字；未选 = `--text-secondary` 灰。
- 图标用 SF Symbols 风格：24 视窗、1.8 描边、圆角端点、单色 `currentColor`、选中用 filled 变体。

### Sheet（底部弹层）
- 从底部 `slide-up` 升起，`rounded-t-xl` + `glass-surface` + `shadow-sheet`。
- 顶部一个抓手（`h-1 w-9 rounded-full bg-hairline`）。
- 标题行 + 右上角关闭，内容区 `sheet-body-max` 可滚动，尊重 safe-area。

### Buttons
| 类型 | 样式 | 用途 |
|---|---|---|
| Primary | `bg-accent text-on-accent rounded-md min-h-12` 白字 | 唯一主操作（保存 / 继续） |
| Secondary | `bg-subtle text-ink` | 次要操作（取消 / 稍后） |
| Plain | 无背景、`text-accent` 或 `text-ink-secondary` | 编辑 / 分享 / 更多 |

所有可点区域 ≥ `44×44`（用 `min-h-11` = 44px 兜底）。

### Form Controls
`input` / `textarea` 优先保留原生语义并套用 `min-h-11 rounded-md border border-hairline bg-surface`。`select` 是例外：桌面浏览器的原生选项面板无法完整继承本系统的色彩、圆角、间距和选中态，产品界面默认使用项目已有的可访问 Select / Listbox 组件。

- Trigger 与相邻控件同高；选项浮层使用 `bg-surface`、`border-hairline`、`rounded-lg` 和浮层阴影，当前项用 `accent-soft` + 对勾表达。
- 保留标签、键盘导航、Escape 关闭、焦点返回和正确的 `aria` 语义；不要为换皮手写一套不完整的键盘与焦点管理。
- 仅当移动触控流程明确需要系统选择器，或产品本身刻意采用平台原生控件时，才直接显示原生 `<select>`。

### 触控反馈（克制但有感）
可点列表行按下时轻微回弹 + 高亮，松手弹回：
```tsx
className="transition-all duration-fast ease-ios active:scale-[0.97] active:bg-subtle"
```
幅度只到 `0.97`，绝不夸张。chevron 可在 `group-active` 时轻微右移。
桌面端 hover 只轻改背景，键盘操作保留全局 `:focus-visible` 焦点环。

---

## 11. 动效（Motion）

动画只表达**物理关系**，不炫技。

| 时长 | 用途 |
|---|---|
| 150ms (`fast`) | 按下、hover、颜色反馈 |
| 220ms (`normal`) | 普通过渡、分段滑块、淡入 |
| 300ms (`slow`) | Sheet 升起、页面切换 |

统一缓动（iOS 感）：
```css
cubic-bezier(.2, .8, .2, 1)
```

**页面转场（贴合 iOS 的克制）：**
- Tab 之间切换：仅淡入。
- 进入下一级（列表→详情）：从右侧轻推入（前进）。
- 返回上一级：从左侧轻推入（后退），形成「上一页被接回来」的视差回拉。

**必须尊重 `prefers-reduced-motion`**：全局 CSS 已兜底（所有动画/过渡压到 0.01ms）。

---

## 12. 深色模式实现

- 给 `<html>` 加/去 `.dark` 类（`tailwind.config.ts` 已配 `darkMode: 'class'`）。
- 同时设置 `root.style.colorScheme`，让系统控件（滚动条、表单）跟着变。
- 跟随系统：监听 `prefers-color-scheme` 的 `change`。
- PWA 进阶：同步 `theme-color` meta、`apple-mobile-web-app-status-bar-style`、manifest 与启动图。

---

## 13. 通用页面与响应式约定

同一套风格通过布局适配场景，不为每类产品另造视觉语言。

- **导航**：移动端优先底部导航；宽屏改为侧栏或顶部栏，不把移动胶囊强行拉宽。
- **列表与数据**：同构信息用 InsetGroup；少量结构化数据可用表格，但只保留必要分隔线。
- **表单**：一列完成一个任务；宽屏只扩展留白或并排强相关字段，不无限拉长输入框。
- **状态与反馈**：局部结果就地显示；全局结果用 Toast / Banner；错误需同时提供文字说明和恢复动作。
- **长内容**：文章、文档可选衬线正文；其余界面保持系统无衬线。
- **空白 / 加载 / 错误**：说明发生了什么，并只给一个明确的下一步，不用插画堆占页面。

---

## 14. 落地到新项目（三步）

1. **拷贝三件套**（同目录）：
   - `tokens.css` → 最先引入
   - `globals.css` → 其后引入
   - `tailwind.config.ts` → 替换项目的，改 `content` 路径
2. **确认引入顺序**（入口 `main.tsx` / `main.ts`）：
   ```ts
   import './styles/tokens.css'
   import './styles/globals.css'
   ```
3. **改品牌**：只改 `tokens.css` 里 `--accent` 一族（浅 8 + 深 8 个值）。

然后在组件里只用语义类名：`bg-canvas / bg-surface / text-ink / text-ink-secondary / text-accent / border-hairline / rounded-md` 等。

---

## 15. 一页速查

```
字族    默认=系统无衬线  长内容可选衬线(font-serif text-body-serif)
背景    bg-canvas(页面) → bg-surface(卡片) → 控制层 glass
文字    text-ink / text-ink-secondary / text-tertiary
强调    text-accent(仅此一处彩色)
分隔    divide-hairline / border-hairline
内容    同构信息用 InsetGroup，表单/卡片共用 Surface
选择器  默认用 Token 化 Select/Listbox；原生 select 仅用于明确的系统选择器
圆角    sm8 md12 lg16 xl20 full
间距    只用 4 的倍数，页面左右 16
触控    active:scale-[0.97] active:bg-subtle，≥44px
动效    150/220/300ms，cubic-bezier(.2,.8,.2,1)
层级    严格四层，卡片不套卡片
深浅    .dark 类 + 语义 Token，禁写死色值
```

> **最终检验**：换掉产品名称后，界面仍应像设备里自然存在的系统级产品，而不是只能服务某一种内容的模板。
