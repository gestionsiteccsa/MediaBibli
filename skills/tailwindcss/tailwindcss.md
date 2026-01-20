# Tailwind CSS

## Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configuration (tailwind.config.js)
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Import CSS
```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Layout

### Flexbox
```html
<div class="flex">...</div>
<div class="flex flex-col">...</div>
<div class="flex flex-row-reverse">...</div>

<!-- Alignement -->
<div class="flex items-center">...</div>
<div class="flex items-start">...</div>
<div class="flex items-end">...</div>

<!-- Justification -->
<div class="flex justify-center">...</div>
<div class="flex justify-between">...</div>
<div class="flex justify-around">...</div>
<div class="flex justify-evenly">...</div>

<!-- Gap -->
<div class="flex gap-4">...</div>
<div class="flex gap-x-4 gap-y-2">...</div>

<!-- Wrap -->
<div class="flex flex-wrap">...</div>
```

### Grid
```html
<div class="grid grid-cols-3 gap-4">...</div>
<div class="grid grid-cols-12 gap-4">
  <div class="col-span-4">...</div>
  <div class="col-span-8">...</div>
</div>

<!-- Responsive -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">...</div>

<!-- Auto -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))]">...</div>
```

### Container
```html
<div class="container mx-auto px-4">...</div>
```

## Spacing

### Padding
```html
<div class="p-4">All sides</div>
<div class="px-4">Horizontal</div>
<div class="py-4">Vertical</div>
<div class="pt-4 pb-2 pl-4 pr-2">Individual</div>
```

### Margin
```html
<div class="m-4">All sides</div>
<div class="mx-auto">Center horizontally</div>
<div class="mt-4 mb-2">Top and bottom</div>
<div class="-mt-4">Negative margin</div>
```

### Space between
```html
<div class="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

## Typographie

```html
<!-- Taille -->
<p class="text-xs">Extra small</p>
<p class="text-sm">Small</p>
<p class="text-base">Base</p>
<p class="text-lg">Large</p>
<p class="text-xl">Extra large</p>
<p class="text-2xl">2XL</p>

<!-- Poids -->
<p class="font-light">Light</p>
<p class="font-normal">Normal</p>
<p class="font-medium">Medium</p>
<p class="font-semibold">Semibold</p>
<p class="font-bold">Bold</p>

<!-- Alignement -->
<p class="text-left">Left</p>
<p class="text-center">Center</p>
<p class="text-right">Right</p>

<!-- Couleur -->
<p class="text-gray-500">Gray</p>
<p class="text-blue-600">Blue</p>
<p class="text-red-500">Red</p>

<!-- Style -->
<p class="italic">Italic</p>
<p class="underline">Underlined</p>
<p class="line-through">Strikethrough</p>
<p class="uppercase">Uppercase</p>
<p class="capitalize">Capitalize</p>

<!-- Line height -->
<p class="leading-tight">Tight</p>
<p class="leading-normal">Normal</p>
<p class="leading-relaxed">Relaxed</p>

<!-- Truncate -->
<p class="truncate">Text très long...</p>
<p class="line-clamp-2">Multi-line truncate...</p>
```

## Couleurs et backgrounds

```html
<!-- Background -->
<div class="bg-white">...</div>
<div class="bg-gray-100">...</div>
<div class="bg-blue-500">...</div>
<div class="bg-gradient-to-r from-blue-500 to-purple-500">...</div>

<!-- Opacité -->
<div class="bg-black/50">50% opacity</div>
<div class="bg-blue-500/75">75% opacity</div>
```

## Bordures et ombres

```html
<!-- Bordures -->
<div class="border">...</div>
<div class="border-2">...</div>
<div class="border-t border-b">Top and bottom</div>
<div class="border-gray-300">...</div>

<!-- Border radius -->
<div class="rounded">...</div>
<div class="rounded-lg">...</div>
<div class="rounded-full">...</div>
<div class="rounded-t-lg">Top only</div>

<!-- Ombres -->
<div class="shadow">...</div>
<div class="shadow-md">...</div>
<div class="shadow-lg">...</div>
<div class="shadow-xl">...</div>
```

## Sizing

```html
<!-- Width -->
<div class="w-full">100%</div>
<div class="w-1/2">50%</div>
<div class="w-64">16rem</div>
<div class="w-screen">100vw</div>
<div class="max-w-md">Max width medium</div>
<div class="min-w-0">Min width 0</div>

<!-- Height -->
<div class="h-full">100%</div>
<div class="h-screen">100vh</div>
<div class="h-64">16rem</div>
<div class="min-h-screen">Min 100vh</div>
```

## Position

```html
<div class="relative">
  <div class="absolute top-0 right-0">...</div>
</div>

<div class="fixed bottom-4 right-4">...</div>
<div class="sticky top-0">...</div>

<!-- Inset -->
<div class="absolute inset-0">Full overlay</div>
<div class="absolute inset-x-0 bottom-0">Bottom bar</div>
```

## États et interactivité

```html
<!-- Hover -->
<button class="bg-blue-500 hover:bg-blue-600">...</button>

<!-- Focus -->
<input class="focus:outline-none focus:ring-2 focus:ring-blue-500">

<!-- Active -->
<button class="active:bg-blue-700">...</button>

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed">...</button>

<!-- Group hover -->
<div class="group">
  <p class="group-hover:text-blue-500">...</p>
</div>
```

## Responsive

```html
<!-- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px) -->
<div class="text-sm md:text-base lg:text-lg">...</div>
<div class="hidden md:block">Visible on md+</div>
<div class="md:hidden">Hidden on md+</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">...</div>
```

## Dark mode

```html
<div class="bg-white dark:bg-gray-900">...</div>
<p class="text-gray-900 dark:text-white">...</p>
```

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class', // ou 'media'
}
```

## Animations et transitions

```html
<!-- Transitions -->
<button class="transition-colors duration-200">...</button>
<div class="transition-all duration-300 ease-in-out">...</div>

<!-- Transform -->
<div class="hover:scale-105 transition-transform">...</div>
<div class="hover:-translate-y-1">...</div>
<div class="rotate-45">...</div>

<!-- Animations -->
<div class="animate-spin">...</div>
<div class="animate-pulse">...</div>
<div class="animate-bounce">...</div>
```

## Classes utilitaires

```html
<!-- Cursor -->
<div class="cursor-pointer">...</div>
<div class="cursor-not-allowed">...</div>

<!-- Overflow -->
<div class="overflow-hidden">...</div>
<div class="overflow-auto">...</div>
<div class="overflow-x-scroll">...</div>

<!-- Z-index -->
<div class="z-10">...</div>
<div class="z-50">...</div>

<!-- Visibility -->
<div class="invisible">...</div>
<div class="visible">...</div>

<!-- Opacity -->
<div class="opacity-50">...</div>
<div class="opacity-0 hover:opacity-100">...</div>
```

## Personnalisation

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      spacing: {
        '128': '32rem',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

## Composants avec @apply

```css
/* Dans votre CSS */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
```
