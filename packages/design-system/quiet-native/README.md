# 静谧原生设计规范 (Quiet Native Design System)

> 一套可跨项目复用的移动端 Web/PWA 设计系统（devkit · `packages/design-system/quiet-native`）。
> 目标气质：**Apple Notes × Apple Podcasts × Safari 阅读模式**——安静、克制、内容优先，像原生 App，而不是传统 SaaS。
>
> 本规范附带可直接拷贝的代码骨架：`tokens.css` + `tailwind.config.ts` + `globals.css`。
> 用法见 §14；这是 devkit 的 `design-system` package 中的一套风格规范，根级说明见仓库 `README.md`。

---

## 0. 一条总原则

**内容 > 排版 > 留白 > 交互 > 装饰。**

任何视觉元素，如果不能帮助用户「记录、阅读、理解、搜索、整理」，就应该被删掉。

判断一个新设计对不对，只看一句：**它退后了吗？** 界面永远退后，让标题、正文、用户自己的内容成为视觉主体。

---

## 1. 什么时候用这套系统

**适合：**
- 内容型 / 工具型产品（笔记、阅读、播客、文档、日记、资料库）
- 移动端优先的 Web App / PWA
- 需要「原生 iOS 气质」而不是「Web 后台气质」的界面

**不适合：**
- 数据密集的 Dashboard / 管理后台
- 营销页 / 落地页（需要强视觉刺激的场景）
- 桌面端生产力软件（信息密度优先于留白）

---

## 2. 反模式（先说不该做什么）

很多 AI / SaaS 产品会不自觉地犯这些错。这套系统的价值一半在于**明确禁止**：

| 不要做 | 改成 |
|---|---|
| 大面积彩色渐变、紫到粉 | 中性色为主，只有一个克制的品牌母题 |
| 卡片套卡片套按钮框 | 严格四层视觉层级（见 §9） |
| 每个元素都带阴影、描边 | 普通卡片无阴影，靠背景+分隔线分层 |
| 五六个蓝色按钮抢注意力 | 一个页面最多一个 Primary Action |
| 黄色马克笔式高亮 | 搜索高亮只改颜色+字重，不上底色 |
| 满屏 Badge / 标签 | 状态用文字颜色表达，不用胶囊 |
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

**双字族是本系统的灵魂**：UI 用无衬线，**长文阅读用衬线**。这是区别于普通工具 App、带来「阅读质感」的关键。

```css
--font-content: ui-serif, "Songti SC", "Noto Serif CJK SC", Georgia, serif;
```

| Token | 字号 | 字重 | 用途 |
|---|---:|---:|---|
| `large-title` | 32 | 700 | 页面主标题 |
| `title-1` | 26 | 700 | 详情页大标题（常配衬线） |
| `title-2` | 21 | 600 | 段落标题 |
| `headline` | 17 | 600 | 卡片标题 |
| `body` | 17 | 400 | 正文（UI 无衬线） |
| `body-serif` | 17 | 400 / lh 1.78 | **长文正文（衬线）** |
| `callout` | 16 | 400 | AI 内容、次要正文 |
| `subheadline` | 15 | 400 | 辅助信息 |
| `caption` | 13 | 400 | 时间、状态 |

**使用规则：**
- 阅读型正文（Transcript、笔记、AI 整理）→ `body-serif` + 衬线，行高 1.78，追求阅读体验而非塞满屏幕。
- UI 元素（按钮、标签、导航、列表行标题）→ 无衬线。
- 详情页大标题可用衬线（`font-serif text-title-1`），像一篇文章的题字。

---

## 5. 间距（4px 网格）

只允许这些值：`4 8 12 16 20 24 32 40 48`

| 场景 | 间距 |
|---|---|
| 页面左右边距 | 16 |
| 大区块之间 | 32 |
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
Level 1   内容 Surface (--bg-surface，圆角白卡片)
Level 2   Navigation / Toolbar（Glass 控制层）
Level 3   Modal / Sheet（Glass + 阴影）
```

**禁止**「卡片里套卡片、卡片里再套一个带框按钮」。这是 AI 产品最容易踩的坑——每多一层嵌套，原生感就丢一分。

---

## 10. 核心组件

下列组件只给契约（结构 + 关键类名），照着即可在任何项目里复刻。完整的 React 参考实现见 devkit 根仓库 `docs/` 里指向的样例工程。

### InsetGroup（分组卡片列表）— 全 App 列表的统一语言
Apple Settings 的 inset-grouped：一个圆角白卡片浮在灰背景上，行与行之间用发丝分隔线，整组一个容器。

```tsx
<div className="overflow-hidden rounded-md bg-surface">
  <div className="divide-y divide-hairline">{rows}</div>
</div>
```

**首页优先用 List，而不是 Card Grid**——因为这是内容工具，不是电商。

### SectionLabel（分区小标签）
```tsx
<div className="px-4 pt-6 pb-2 text-caption-medium text-ink-secondary">{children}</div>
```

### 列表行（List Row）
内容左对齐、可截断，右侧一个 `›` chevron，按下整行轻弹（见 §11 触控反馈）。
**内容本身就是 UI**：节目标题、3 条记录 · 已转录、今天——没有装饰、没有标签堆。

### SegmentedControl（分段控件，带滑动块）
选中项不是瞬间跳变，而是一个白色滑块在选项间**平滑滑动**（实测 DOM 宽度+位移）。轨道用 `bg-subtle`，滑块用 `bg-surface` + `shadow-control`。这是贴合 iOS 的关键细节之一。

### Bottom Navigation（悬浮玻璃胶囊）
参考 Apple Arcade：不是贴底的整宽 bar，而是一个**悬浮圆角胶囊**，内容从下方透出。

- 胶囊 `rounded-full` + `glass-nav`，高约 58px，距底 `safe-area + 10px`。
- 4 个 Tab：图标（线性/filled 两态）+ 10px 文字。
- 选中 = accent 图标 + accent 字；未选 = `--text-secondary` 灰。
- 图标用 SF Symbols 风格：24 视窗、1.8 描边、圆角端点、单色 `currentColor`、选中用 filled 变体。

### Sheet（底部弹层）
- 从底部 `slide-up` 升起，`rounded-t-xl` + `glass-surface` + `shadow-sheet`。
- 顶部一个抓手（`h-1 w-9 rounded-full bg-hairline`）。
- 标题行 + 右上角关闭，内容区 `sheet-body-max` 可滚动，尊重 safe-area。

### Buttons
| 类型 | 样式 | 用途 |
|---|---|---|
| Primary | `bg-accent text-on-accent rounded-md min-h-12` 白字 | 唯一主操作（开始转录） |
| Secondary | `bg-subtle text-ink` | 次要操作（重新识别 / 复制） |
| Plain | 无背景、`text-accent` 或 `text-ink-secondary` | 分享 / 编辑 / 更多 |

所有可点区域 ≥ `44×44`（用 `min-h-11` = 44px 兜底）。

### 触控反馈（克制但有感）
可点列表行按下时轻微回弹 + 高亮，松手弹回：
```tsx
className="transition-all duration-fast ease-ios active:scale-[0.97] active:bg-subtle"
```
幅度只到 `0.97`，绝不夸张。chevron 可在 `group-active` 时轻微右移。

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

## 13. 阅读型内容排版约定

这套系统最擅长的是「把长文读舒服」。

- **Transcript / 采访稿**：不用气泡、不用「蓝框=甲 / 灰框=乙」。Speaker 用 `15px semibold` + 一个彩色小圆点区分，时间用 `13px tertiary`，正文 `17px 衬线 / 1.78`。同一人连续发言不重复署名，只靠留白分段。
- **笔记**：时间戳（小圆点 + caption）+ 衬线正文，记录之间大量留白。
- **AI 整理**：小标题（`caption-medium` + 一小段 accent 横线）+ 衬线正文，不要做成 ChatGPT 克隆的气泡流。
- **搜索高亮**：只 `color: accent` + `font-weight: 600`，**不要黄色底色**。

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
字族    UI=无衬线  长文=衬线(font-serif text-body-serif)
背景    bg-canvas(页面) → bg-surface(卡片) → 控制层 glass
文字    text-ink / text-ink-secondary / text-tertiary
强调    text-accent(仅此一处彩色)
分隔    divide-hairline / border-hairline
列表    InsetGroup = rounded-md bg-surface + divide-y divide-hairline
圆角    sm8 md12 lg16 xl20 full
间距    只用 4 的倍数，页面左右 16
触控    active:scale-[0.97] active:bg-subtle，≥44px
动效    150/220/300ms，cubic-bezier(.2,.8,.2,1)
层级    严格四层，卡片不套卡片
深浅    .dark 类 + 语义 Token，禁写死色值
```

> **最终检验**：用户打开产品时，应该感觉「这是一本专为内容而生的智能笔记本」，而不是「又一个 AI SaaS」。
