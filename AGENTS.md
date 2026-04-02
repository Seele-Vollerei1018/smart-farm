# AGENTS.md - 智慧农业 (Smart Farm) 开发指南

## 项目概览

Vue 3 + Vite 前端项目，使用 Composition API (`<script setup>`)，状态管理用 Pinia，路由用 Vue Router。纯 JavaScript（无 TypeScript）。

## 包管理与命令

**包管理器**: pnpm（基于 pnpm-lock.yaml）

```bash
pnpm dev          # 启动开发服务器
pnpm build        # 生产环境构建
pnpm preview      # 预览构建产物
pnpm lint         # 运行所有 lint（oxlint + eslint，自动修复）
pnpm lint:oxlint  # 仅运行 oxlint（自动修复）
pnpm lint:eslint  # 仅运行 eslint（自动修复，带 cache）
pnpm format       # 运行 Prettier 格式化 src/ 目录
```

**测试**: 当前项目无测试框架。如需添加测试，优先使用 Vitest + Vue Test Utils（与 Vite 生态一致）。

## 代码风格

### 格式化 (Prettier)

- 无分号 (`semi: false`)
- 单引号 (`singleQuote: true`)
- 行宽 100 字符 (`printWidth: 100`)

### 缩进与编码 (EditorConfig)

- 2 空格缩进
- LF 换行符
- UTF-8 编码
- 文件末尾保留空行
- 去除行尾空格

### Linting

- **oxlint**: 核心正确性检查（`correctness: error`），包含 eslint/unicorn/oxc/vue 插件
- **eslint**: flat config，应用 `flat/essential` Vue 规则 + js recommended
- 先跑 oxlint 再跑 eslint，最后 prettier 格式化

## Vue 组件规范

### 组件结构

使用 `<script setup>` + Composition API：

```vue
<script setup>
import { ref, computed, watch } from 'vue'

// 1. imports
// 2. props/emit (if any)
// 3. reactive state (ref/reactive)
// 4. computed
// 5. watch/effects
// 6. methods/functions
</script>

<template>
  <!-- 模板 -->
</template>

<style scoped>
/* 样式，默认 scoped */
</style>
```

### 命名约定

- **组件文件**: PascalCase（如 `DashboardView.vue`、`IconDocumentation.vue`）
- **目录**: 小写或 PascalCase（`components/`、`views/`、`stores/`）
- **JS 变量**: camelCase
- **常量/配置对象**: camelCase（如 `pageTitles`）
- **CSS 类名**: kebab-case 或 BEM 风格（如 `nav-link--active`）
- **CSS 变量**: `--sf-` 前缀（如 `--sf-green`、`--sf-surface`）

### 路径别名

使用 `@/` 别名引用 `src/` 目录：

```js
import App from '@/App.vue'
import { logout } from '@/utils/auth'
```

## 项目结构

```
src/
├── api/          # API 请求封装（client.js）
├── assets/       # 静态资源（CSS、图片等）
├── components/   # 可复用组件（icons/ 子目录存放图标组件）
├── router/       # Vue Router 配置（index.js）
├── stores/       # Pinia 状态管理（counter.js）
├── utils/        # 工具函数（auth.js）
├── views/        # 页面级组件（*View.vue）
├── App.vue       # 根组件（布局、侧边栏、顶栏）
└── main.js       # 应用入口
```

## 类型与错误处理

- **无 TypeScript**: 纯 JavaScript 项目，使用 JSDoc 注释复杂函数
- **错误处理**: API 调用使用 try/catch，用户操作提供友好提示
- **可选链**: 大量使用 `?.` 和 `??` 处理空值（如 `currentUser.value?.displayName`）

## Git 提交规范

- 提交信息使用中文或英文均可，保持简洁
- 遵循 conventional commits 风格（如 `feat:`, `fix:`, `refactor:`）
- 提交前确保 `pnpm lint` 通过

## 注意事项

- Node.js 版本要求: `^20.19.0 || >=22.12.0`
- Vite 配置中 `base: './'` 使用相对路径，适配子目录部署
- 样式使用 scoped CSS，无预处理器（纯 CSS）
- 无后端集成时，数据可用模拟数据（原型阶段）
