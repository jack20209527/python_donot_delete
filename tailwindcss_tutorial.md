# Tailwind CSS 学习教程

## 一、布局属性

### 容器查询

| 属性 | 说明 |
|------|------|
| `container` | 启用容器查询，限制元素最大宽度 |

### 显示与定位

| 属性 | 说明 |
|------|------|
| `block` | 块级元素 |
| `inline-block` | 行内块级元素 |
| `inline` | 行内元素 |
| `flex` | 弹性盒子 |
| `inline-flex` | 行内弹性盒子 |
| `grid` | 网格布局 |
| `inline-grid` | 行内网格布局 |
| `hidden` | 隐藏元素 |
| `contents` | 子元素上升 |
| `list-item` | 列表项 |

### Flex 布局

| 属性 | 说明 |
|------|------|
| `flex-row` | 水平排列 |
| `flex-row-reverse` | 水平反向排列 |
| `flex-col` | 垂直排列 |
| `flex-col-reverse` | 垂直反向排列 |
| `flex-wrap` | 允许换行 |
| `flex-nowrap` | 不换行 |
| `flex-wrap-reverse` | 反向换行 |
| `flex-1` | flex: 1 1 0% |
| `flex-auto` | flex: 1 1 auto |
| `flex-initial` | flex: 0 1 auto |
| `flex-none` | flex: none |
| `flex-grow` | flex-grow: 1 |
| `flex-grow-0` | flex-grow: 0 |
| `flex-shrink` | flex-shrink: 1 |
| `flex-shrink-0` | flex-shrink: 0 |

### Grid 布局

| 属性 | 说明 |
|------|------|
| `grid-cols-1` ~ `grid-cols-12` | 列数 |
| `grid-rows-1` ~ `grid-rows-6` | 行数 |
| `col-span-1` ~ `col-span-12` | 跨列数 |
| `col-span-full` | 跨所有列 |
| `row-span-1` ~ `row-span-6` | 跨行数 |
| `row-span-full` | 跨所有行 |
| `grid-flow-row` | 行优先 |
| `grid-flow-col` | 列优先 |
| `grid-flow-dense` | 紧凑填充 |

### 间距 (Gap)

| 属性 | 说明 |
|------|------|
| `gap-0` ~ `gap-96` | 间距 0 ~ 384px (0, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96) |
| `gap-x-*` | 水平间距 |
| `gap-y-*` | 垂直间距 |

---

## 二、间距与尺寸

### 内边距 (Padding)

| 属性 | 说明 |
|------|------|
| `p-0` ~ `p-96` | 四周内边距 0 ~ 384px |
| `px-*` | 水平内边距 (左右) |
| `py-*` | 垂直内边距 (上下) |
| `pt-*` | 上内边距 |
| `pr-*` | 右内边距 |
| `pb-*` | 下内边距 |
| `pl-*` | 左内边距 |
| `ps-*` | 开始内边距 (LTR: 左, RTL: 右) |
| `pe-*` | 结束内边距 (LTR: 右, RTL: 左) |

### 外边距 (Margin)

| 属性 | 说明 |
|------|------|
| `m-0` ~ `m-96` | 四周外边距 0 ~ 384px |
| `mx-*` | 水平外边距 (左右) |
| `my-*` | 垂直外边距 (上下) |
| `mt-*` | 上外边距 |
| `mr-*` | 右外边距 |
| `mb-*` | 下外边距 |
| `ml-*` | 左外边距 |
| `ms-*` | 开始外边距 |
| `me-*` | 结束外边距 |
| `m-auto` | 自动外边距 (居中) |
| `mx-auto` | 水平居中 |
| `my-auto` | 垂直居中 |

### 尺寸

| 属性 | 说明 |
|------|------|
| `w-0` ~ `w-96` | 宽度 0 ~ 384px |
| `w-full` | 宽度 100% |
| `w-screen` | 宽度 100vw |
| `w-min` | 最小内容宽度 |
| `w-max` | 最大内容宽度 |
| `w-fit` | 适应内容宽度 |
| `w-auto` | 自动宽度 |
| `w-1/2` ~ `w-11/12` | 宽度百分比 (1/2 到 11/12) |
| `h-0` ~ `h-96` | 高度 0 ~ 384px |
| `h-full` | 高度 100% |
| `h-screen` | 高度 100vh |
| `h-min` | 最小内容高度 |
| `h-max` | 最大内容高度 |
| `h-fit` | 适应内容高度 |
| `h-auto` | 自动高度 |
| `min-w-0` ~ `min-w-96` | 最小宽度 |
| `max-w-0` ~ `max-w-96` | 最大宽度 |
| `max-w-xs` | 最大宽度 20rem (320px) |
| `max-w-sm` | 最大宽度 24rem (384px) |
| `max-w-md` | 最大宽度 28rem (448px) |
| `max-w-lg` | 最大宽度 32rem (512px) |
| `max-w-xl` | 最大宽度 36rem (576px) |
| `max-w-2xl` | 最大宽度 42rem (672px) |
| `max-w-3xl` | 最大宽度 48rem (768px) |
| `max-w-4xl` | 最大宽度 56rem (896px) |
| `max-w-5xl` | 最大宽度 64rem (1024px) |
| `max-w-6xl` | 最大宽度 72rem (1152px) |
| `max-w-7xl` | 最大宽度 80rem (1280px) |
| `max-w-full` | 最大宽度 100% |
| `max-w-none` | 无最大宽度 |

---

## 三、文字排版

### 字体大小

| 属性 | 说明 |
|------|------|
| `text-xs` | 0.75rem (12px) |
| `text-sm` | 0.875rem (14px) |
| `text-base` | 1rem (16px) |
| `text-lg` | 1.125rem (18px) |
| `text-xl` | 1.25rem (20px) |
| `text-2xl` | 1.5rem (24px) |
| `text-3xl` | 1.875rem (30px) |
| `text-4xl` | 2.25rem (36px) |
| `text-5xl` | 3rem (48px) |
| `text-6xl` | 3.75rem (60px) |
| `text-7xl` | 4.5rem (72px) |
| `text-8xl` | 6rem (96px) |
| `text-9xl` | 8rem (128px) |

### 字体粗细

| 属性 | 说明 |
|------|------|
| `font-thin` | 字重 100 |
| `font-extralight` | 字重 200 |
| `font-light` | 字重 300 |
| `font-normal` | 字重 400 |
| `font-medium` | 字重 500 |
| `font-semibold` | 字重 600 |
| `font-bold` | 字重 700 |
| `font-extrabold` | 字重 800 |
| `font-black` | 字重 900 |

### 文本对齐

| 属性 | 说明 |
|------|------|
| `text-left` | 左对齐 |
| `text-center` | 居中对齐 |
| `text-right` | 右对齐 |
| `text-justify` | 两端对齐 |
| `text-start` | 起始对齐 |
| `text-end` | 结束对齐 |

### 文本装饰

| 属性 | 说明 |
|------|------|
| `underline` | 下划线 |
| `overline` | 上划线 |
| `line-through` | 删除线 |
| `no-underline` | 无下划线 |

### 文本转换

| 属性 | 说明 |
|------|------|
| `uppercase` | 大写 |
| `lowercase` | 小写 |
| `capitalize` | 首字母大写 |
| `normal-case` | 默认大小写 |

### 文字颜色

| 属性 | 说明 |
|------|------|
| `text-white` | 白色 #ffffff |
| `text-black` | 黑色 #000000 |
| `text-gray-50` ~ `text-gray-900` | 灰色色阶 50~900 |
| `text-red-50` ~ `text-red-900` | 红色色阶 |
| `text-blue-50` ~ `text-blue-900` | 蓝色色阶 |
| `text-green-50` ~ `text-green-900` | 绿色色阶 |
| `text-yellow-50` ~ `text-yellow-900` | 黄色色阶 |
| `text-purple-50` ~ `text-purple-900` | 紫色色阶 |
| `text-pink-50` ~ `text-pink-900` | 粉色色阶 |
| `text-indigo-50` ~ `text-indigo-900` | 靛蓝色色阶 |
| `text-transparent` | 透明 |

### 行高

| 属性 | 说明 |
|------|------|
| `leading-none` | 行高 1 |
| `leading-tight` | 行高 1.25 |
| `leading-snug` | 行高 1.375 |
| `leading-normal` | 行高 1.5 |
| `leading-relaxed` | 行高 1.625 |
| `leading-loose` | 行高 2 |

### 字间距

| 属性 | 说明 |
|------|------|
| `tracking-tighter` | 字间距 -0.05em |
| `tracking-tight` | 字间距 -0.025em |
| `tracking-normal` | 字间距 0 |
| `tracking-wide` | 字间距 0.025em |
| `tracking-wider` | 字间距 0.05em |
| `tracking-widest` | 字间距 0.1em |

### 文本溢出

| 属性 | 说明 |
|------|------|
| `truncate` | 截断文本并添加省略号 |
| `overflow-ellipsis` | 省略号 |
| `overflow-clip` | 裁剪 |
| `text-ellipsis` | 文本省略号 |

---

## 四、背景与边框

### 背景颜色

| 属性 | 说明 |
|------|------|
| `bg-white` | 白色背景 |
| `bg-black` | 黑色背景 |
| `bg-gray-50` ~ `bg-gray-900` | 灰色色阶 |
| `bg-red-50` ~ `bg-red-900` | 红色色阶 |
| `bg-blue-50` ~ `bg-blue-900` | 蓝色色阶 |
| `bg-green-50` ~ `bg-green-900` | 绿色色阶 |
| `bg-yellow-50` ~ `bg-yellow-900` | 黄色色阶 |
| `bg-purple-50` ~ `bg-purple-900` | 紫色色阶 |
| `bg-pink-50` ~ `bg-pink-900` | 粉色色阶 |
| `bg-transparent` | 透明背景 |
| `bg-current` | 当前文字颜色 |

### 背景图片

| 属性 | 说明 |
|------|------|
| `bg-none` | 无背景图 |
| `bg-cover` | 覆盖整个容器 |
| `bg-contain` | 包含在容器内 |
| `bg-auto` | 自动大小 |

### 背景位置

| 属性 | 说明 |
|------|------|
| `bg-bottom` | 底部 |
| `bg-center` | 居中 |
| `bg-left` | 左侧 |
| `bg-left-bottom` | 左下 |
| `bg-left-top` | 左上 |
| `bg-right` | 右侧 |
| `bg-right-bottom` | 右下 |
| `bg-right-top` | 右上 |
| `bg-top` | 顶��� |

### 背景重复

| 属性 | 说明 |
|------|------|
| `bg-repeat` | 重复 |
| `bg-no-repeat` | 不重复 |
| `bg-repeat-x` | 水平重复 |
| `bg-repeat-y` | 垂直重复 |
| `bg-repeat-round` | 圆形重复 |
| `bg-repeat-space` | 间距重复 |

### 边框半径 (圆角)

| 属性 | 说明 |
|------|------|
| `rounded-none` | 无圆角 |
| `rounded-sm` | 小圆角 0.125rem |
| `rounded` | 默认圆角 0.25rem |
| `rounded-md` | 中圆角 0.375rem |
| `rounded-lg` | 大圆角 0.5rem |
| `rounded-xl` | 超大圆角 0.75rem |
| `rounded-2xl` | 2倍大圆角 1rem |
| `rounded-3xl` | 3倍大圆角 1.5rem |
| `rounded-full` | 完全圆形 |
| `rounded-t-*` | 顶部圆角 |
| `rounded-r-*` | 右侧圆角 |
| `rounded-b-*` | 底部圆角 |
| `rounded-l-*` | 左侧圆角 |
| `rounded-tl-*` | 左上圆角 |
| `rounded-tr-*` | 右上圆角 |
| `rounded-br-*` | 右下圆角 |
| `rounded-bl-*` | 左下圆角 |

### 边框宽度

| 属性 | 说明 |
|------|------|
| `border-0` | 无边框 |
| `border` | 1px 边框 |
| `border-2` | 2px 边框 |
| `border-4` | 4px 边框 |
| `border-8` | 8px 边框 |
| `border-t-*` | 上边框 |
| `border-r-*` | 右边框 |
| `border-b-*` | 下边框 |
| `border-l-*` | 左边框 |

### 边框颜色

| 属性 | 说明 |
|------|------|
| `border-white` | 白色边框 |
| `border-black` | 黑色边框 |
| `border-gray-50` ~ `border-gray-900` | 灰色色阶 |
| `border-red-*` | 红色边框 |
| `border-blue-*` | 蓝色边框 |
| `border-green-*` | 绿色边框 |
| `border-yellow-*` | 黄色边框 |
| `border-transparent` | 透明边框 |
| `border-current` | 当前颜色 |

### 边框样式

| 属性 | 说明 |
|------|------|
| `border-solid` | 实线 |
| `border-dashed` | 虚线 |
| `border-dotted` | 点线 |
| `border-double` | 双线 |
| `border-none` | 无边框 |

---

## 五、定位

### 定位类型

| 属性 | 说明 |
|------|------|
| `static` | 默认定位 |
| `fixed` | 固定定位 |
| `absolute` | 绝对定位 |
| `relative` | 相对定位 |
| `sticky` | 粘性定位 |

### 位置偏移

| 属性 | 说明 |
|------|------|
| `inset-0` ~ `inset-96` | 四周偏移 0 ~ 384px |
| `inset-x-*` | 水平偏移 (左右) |
| `inset-y-*` | 垂直偏移 (上下) |
| `top-*` | 顶部偏移 |
| `right-*` | 右侧偏移 |
| `bottom-*` | 底部偏移 |
| `left-*` | 左侧偏移 |
| `inset-auto` | 自动偏移 |

### 层级 (Z-Index)

| 属性 | 说明 |
|------|------|
| `z-0` ~ `z-50` | z-index 0 ~ 50 |
| `z-auto` | 自动 z-index |
| `z-negative` | 负 z-index |

---

## 六、Flexbox 与 Grid

### Justify Content (主轴对齐)

| 属性 | 说明 |
|------|------|
| `justify-start` | 起始对齐 |
| `justify-end` | 结束对齐 |
| `justify-center` | 居中对齐 |
| `justify-between` | 两端对齐 |
| `justify-around` | 环绕对齐 |
| `justify-evenly` | 均匀分布 |

### Justify Items (项目对齐)

| 属性 | 说明 |
|------|------|
| `justify-items-start` | 起始对齐 |
| `justify-items-end` | 结束对齐 |
| `justify-items-center` | 居中对齐 |
| `justify-items-stretch` | 拉伸填充 |

### Justify Self (自身对齐)

| 属性 | 说明 |
|------|------|
| `justify-self-auto` | 自动对齐 |
| `justify-self-start` | 起始对齐 |
| `justify-self-end` | 结束对齐 |
| `justify-self-center` | 居中对齐 |
| `justify-self-stretch` | 拉伸填充 |

### Align Content (多行对齐)

| 属性 | 说明 |
|------|------|
| `content-center` | 居中对齐 |
| `content-start` | 起始对齐 |
| `content-end` | 结束对齐 |
| `content-between` | 两端对齐 |
| `content-around` | 环绕对齐 |
| `content-evenly` | 均匀分布 |

### Align Items (交叉轴对齐)

| 属性 | 说明 |
|------|------|
| `items-start` | 起始对齐 |
| `items-end` | 结束对齐 |
| `items-center` | 居中对齐 |
| `items-baseline` | 基线对齐 |
| `items-stretch` | 拉伸填充 |

### Align Self (自身交叉轴对齐)

| 属性 | 说明 |
|------|------|
| `self-auto` | 自动对齐 |
| `self-start` | 起始对齐 |
| `self-end` | 结束对齐 |
| `self-center` | 居中对齐 |
| `self-stretch` | 拉伸填充 |

### Place Content (双向对齐)

| 属性 | 说明 |
|------|------|
| `place-content-center` | 居中对齐 |
| `place-content-start` | 起始对齐 |
| `place-content-end` | 结束对齐 |
| `place-content-between` | 两端对齐 |
| `place-content-around` | 环绕对齐 |
| `place-content-evenly` | 均匀分布 |
| `place-content-stretch` | 拉伸填充 |

### Place Items (双向项目对齐)

| 属性 | 说明 |
|------|------|
| `place-items-start` | 起始对齐 |
| `place-items-end` | 结束对齐 |
| `place-items-center` | 居中对齐 |
| `place-items-stretch` | 拉伸填充 |

### Place Self (双向自身对齐)

| 属性 | 说明 |
|------|------|
| `place-self-auto` | 自动对齐 |
| `place-self-start` | 起始对齐 |
| `place-self-end` | 结束对齐 |
| `place-self-center` | 居中对齐 |
| `place-self-stretch` | 拉伸填充 |

---

## 七、效果

### 阴影

| 属性 | 说明 |
|------|------|
| `shadow-none` | 无阴影 |
| `shadow-sm` | 小阴影 |
| `shadow` | 默认阴影 |
| `shadow-md` | 中阴影 |
| `shadow-lg` | 大阴影 |
| `shadow-xl` | 超大阴影 |
| `shadow-2xl` | 2倍超大阴影 |
| `shadow-inner` | 内阴影 |
| `shadow-*` | 颜色阴影 (如 shadow-red-500) |

### 透明度

| 属性 | 说明 |
|------|------|
| `opacity-0` | 完全透明 |
| `opacity-5` ~ `opacity-95` | 透明度 5% ~ 95% |
| `opacity-100` | 完全不透明 |

### 混合模式

| 属性 | 说明 |
|------|------|
| `mix-blend-normal` | 正常 |
| `mix-blend-multiply` | 正片叠底 |
| `mix-blend-screen` | 滤色 |
| `mix-blend-overlay` | 叠加 |
| `mix-blend-darken` | 变暗 |
| `mix-blend-lighten` | 变亮 |
| `mix-blend-color-dodge` | 颜色减淡 |
| `mix-blend-color-burn` | 颜色加深 |
| `mix-blend-hard-light` | 强光 |
| `mix-blend-soft-light` | 柔光 |
| `mix-blend-difference` | 差值 |
| `mix-blend-exclusion` | 排除 |
| `mix-blend-hue` | 色相 |
| `mix-blend-saturation` | 饱和度 |
| `mix-blend-color` | 颜色 |
| `mix-blend-luminosity` | 亮度 |

### 滤镜

| 属性 | 说明 |
|------|------|
| `blur-none` | 无模糊 |
| `blur-sm` | 小模糊 |
| `blur` | 默认模糊 |
| `blur-md` | 中模糊 |
| `blur-lg` | 大模糊 |
| `blur-xl` | 超大模糊 |
| `blur-2xl` | 2倍超大模糊 |
| `blur-3xl` | 3倍超大模糊 |
| `brightness-0` ~ `brightness-200` | 亮度 0% ~ 200% |
| `contrast-0` ~ `contrast-200` | 对比度 0% ~ 200% |
| `grayscale-0` ~ `grayscale` | 灰度 0% ~ 100% |
| `hue-rotate-0` ~ `hue-rotate-180` | 色相旋转 0deg ~ 180deg |
| `invert-0` ~ `invert` | 反转 0% ~ 100% |
| `saturate-0` ~ `saturate-200` | 饱和度 0% ~ 200% |
| `sepia-0` ~ `sepia` | 复古 0% ~ 100% |

### 变换

| 属性 | 说明 |
|------|------|
| `transform` | 启用变换 |
| `transform-gpu` | GPU 加速变换 |
| `transform-none` | 无变换 |
| `scale-0` ~ `scale-150` | 缩放 0 ~ 150% |
| `scale-x-*` | 水平缩放 |
| `scale-y-*` | 垂直缩放 |
| `rotate-0` ~ `rotate-180` | 旋转 0deg ~ 180deg |
| `rotate-1` ~ `rotate-12` | 旋转 1deg ~ 12deg |
| `translate-x-*` | 水平平移 |
| `translate-y-*` | 垂直平移 |

### 过渡

| 属性 | 说明 |
|------|------|
| `transition-none` | 无过渡 |
| `transition-all` | 所有属性过渡 |
| `transition` | 默认过渡属性 |
| `transition-colors` | 颜色过渡 |
| `transition-opacity` | 透明度过渡 |
| `transition-shadow` | 阴影过渡 |
| `transition-transform` | 变换过渡 |
| `duration-75` ~ `duration-700` | 过渡时间 75ms ~ 700ms |
| `ease-linear` | 线性缓动 |
| `ease-in` | 加速 |
| `ease-out` | 减速 |
| `ease-in-out` | 加速后减速 |
| `delay-75` ~ `delay-500` | 延迟 75ms ~ 500ms |

### 动画

| 属性 | 说明 |
|------|------|
| `animate-none` | 无动画 |
| `animate-spin` | 旋转���画 |
| `animate-ping` | 脉冲动画 |
| `animate-pulse` | 跳动动画 |
| `animate-bounce` | 弹跳动画 |

---

## 八、交互

### 光标

| 属性 | 说明 |
|------|------|
| `cursor-auto` | 自动光标 |
| `cursor-default` | 默认光标 |
| `cursor-pointer` | 指针光标 |
| `cursor-wait` | 等待光标 |
| `cursor-text` | 文本光标 |
| `cursor-move` | 移动光标 |
| `cursor-not-allowed` | 禁止光标 |
| `cursor-crosshair` | 十字光标 |
| `cursor-grab` | 抓取光标 |
| `cursor-grabbing` | 抓取中光标 |

### 用户选择

| 属性 | 说明 |
|------|------|
| `select-none` | 不可选择 |
| `select-text` | 文本可选择 |
| `select-all` | 全部可选择 |
| `select-auto` | 自动选择 |

### 指针事件

| 属性 | 说明 |
|------|------|
| `pointer-events-none` | 无指针事件 |
| `pointer-events-auto` | 自动指针事件 |

### 禁用状态

| 属性 | 说明 |
|------|------|
| `disabled:opacity-50` | 禁用时透明度 50% |
| `disabled:cursor-not-allowed` | 禁用时禁止光标 |

### 悬停状态

| 属性 | 说明 |
|------|------|
| `hover:bg-red-500` | 悬停时背景色 |
| `hover:text-white` | 悬停时文字颜色 |
| `hover:scale-105` | 悬停时缩放 105% |
| `hover:shadow-lg` | 悬停时阴影 |

### 焦点状态

| 属性 | 说明 |
|------|------|
| `focus:outline-none` | 焦点时无轮廓 |
| `focus:ring-2` | 焦点时 2px 环 |
| `focus:ring-blue-500` | 焦点时蓝色环 |
| `focus-visible:ring-2` | 可见焦点时环 |

### 激活状态

| 属性 | 说明 |
|------|------|
| `active:bg-red-600` | 激活时背景色 |
| `active:scale-95` | 激活时缩放 95% |

---

## 九、SVG 属性

### 填充与描边

| 属性 | 说明 |
|------|------|
| `fill-current` | 填充当前颜色 |
| `fill-none` | 无填充 |
| `fill-*` | 填充颜色 (如 fill-red-500) |
| `stroke-current` | 描边当前颜色 |
| `stroke-none` | 无描边 |
| `stroke-*` | 描边颜色 |
| `stroke-0` ~ `stroke-2` | 描边宽度 0 ~ 2px |

---

## 十、表格布局

| 属性 | 说明 |
|------|------|
| `table` | 表格布局 |
| `table-caption` | 表格标题 |
| `table-cell` | 表格单元格 |
| `table-column` | 表格列 |
| `table-column-group` | 表格列组 |
| `table-footer-group` | 表格页脚组 |
| `table-header-group` | 表格页眉组 |
| `table-row` | 表格行 |
| `table-row-group` | 表格行组 |
| `border-collapse` | 边框合并 |
| `border-separate` | 边框分离 |
| `caption-top` | 标题在顶部 |
| `caption-bottom` | 标题在底部 |
| `table-auto` | 自动表格布局 |
| `table-fixed` | 固定表格布局 |

---

## 十一、其他实用属性

### 溢出

| 属性 | 说明 |
|------|------|
| `overflow-auto` | 自动滚动 |
| `overflow-hidden` | 隐藏溢出 |
| `overflow-visible` | 显示溢出 |
| `overflow-scroll` | 始终显示滚动条 |
| `overflow-x-auto` | 水平滚动 |
| `overflow-y-auto` | 垂直滚动 |
| `overflow-x-hidden` | 隐藏水平溢出 |
| `overflow-y-hidden` | 隐藏垂直溢出 |

### 定位元素

| 属性 | 说明 |
|------|------|
| `isolation-auto` | 自动隔离 |
| `isolation-isolate` | 创建隔离上下文 |

### 对象适配

| 属性 | 说明 |
|------|------|
| `object-contain` | 包含在容器内 |
| `object-cover` | 覆盖容器 |
| `object-fill` | 填充容器 |
| `object-none` | 无适应 |
| `object-scale-down` | 缩小适应 |
| `object-bottom` | 底部对齐 |
| `object-center` | 居中对齐 |
| `object-left` | 左对齐 |
| `object-right` | 右对齐 |
| `object-top` | 顶部对齐 |

### 伪元素

| 属性 | 说明 |
|------|------|
| `before:content-['']` | before 伪元素内容 |
| `after:content-['']` | after 伪元素内容 |

### 列表样式

| 属性 | 说明 |
|------|------|
| `list-none` | 无列表样式 |
| `list-disc` | 实心圆点 |
| `list-decimal` | 数字编号 |

---

## 十二、响应式设计前缀

所有属性都可以添加响应式前缀：

| 前缀 | 断点 | 最小宽度 |
|------|------|----------|
| `sm:` | 小屏幕 | 640px |
| `md:` | 中等屏幕 | 768px |
| `lg:` | 大屏幕 | 1024px |
| `xl:` | 超大屏幕 | 1280px |
| `2xl:` | 2倍超大屏幕 | 1536px |

**示例：**
```html
<!-- 移动端: 红色背景，大屏幕: 蓝色背景 -->
<div class="bg-red-500 lg:bg-blue-500">响应式背景</div>

<!-- 移动端: 单列，中等屏幕: 双列，大屏幕: 三列 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

---

## 十三、状态变体前缀

| 前缀 | 说明 |
|------|------|
| `hover:` | 悬停状态 |
| `focus:` | 焦点状态 |
| `focus-within:` | 子元素获得焦点 |
| `focus-visible:` | 可见焦点 |
| `active:` | 激活状态 |
| `visited:` | 已访问链接 |
| `target:` | 目标元素 |
| `first:` | 第一个子元素 |
| `last:` | 最后一个子元素 |
| `odd:` | 奇数子元素 |
| `even:` | 偶数子元素 |
| `disabled:` | 禁用状态 |
| `checked:` | 选中状态 |
| `group-hover:` | 组悬停 |
| `group-focus:` | 组焦点 |

---

## 使用技巧

### 1. 组合使用
```html
<!-- 居中卡片 -->
<div class="flex items-center justify-center min-h-screen bg-gray-100">
  <div class="bg-white p-8 rounded-lg shadow-lg">
    内容
  </div>
</div>
```

### 2. 响应式布局
```html
<!-- 响应式网格 -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <div>项目 1</div>
  <div>项目 2</div>
</div>
```

### 3. 悬停效果
```html
<!-- 按钮悬停效果 -->
<button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors">
  按钮
</button>
```

### 4. 绝对定位居中
```html
<!-- 绝对定位居中 -->
<div class="relative">
  <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
    居中内容
  </div>
</div>
```

---

## 注意事项

1. **优先级**: Tailwind 使用 utility-first，优先级较高，可能需要 `!` 前缀强制应用
   ```html
   <div class="!text-red-500">强制红色文字</div>
   ```

2. **自定义值**: 使用方括号自定义任意值
   ```html
   <div class="w-[123px] h-[456px] bg-[#1da1f2]">自定义尺寸和颜色</div>
   ```

3. **动态类**: 使用 variant 修饰符
   ```html
   <div class="dark:bg-gray-800 dark:text-white">暗黑模式</div>
   ```

4. **性能**: 推荐使用 PurgeCSS 移除未使用的样式，减小文件大小
