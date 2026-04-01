import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SkillForge',
  titleTemplate: ':title | SkillForge',
  description:
    'Local-first MCP server and portable skill marketplace for Codex, Claude Code, Kimi Code, Ollama, Gemini, and NVIDIA-backed models.',
  lang: 'en-US',
  base: '/skillforge/',
  lastUpdated: true,
  cleanUrls: false,
  appearance: false,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/skillforge/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#0d1015' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'SkillForge' }],
    [
      'meta',
      {
        property: 'og:description',
        content:
          'Local-first MCP server and portable skill marketplace for serious multi-model coding workflows.'
      }
    ]
  ],
  themeConfig: {
    logo: {
      src: '/logo-mark.svg',
      alt: 'SkillForge'
    },
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Quickstart', link: '/quickstart' },
      { text: 'Installs', link: '/one-paste-installs' },
      { text: 'Marketplace', link: '/marketplace' },
      { text: 'Safety', link: '/safety' },
      { text: 'About', link: '/about' }
    ],
    sidebar: [
      {
        text: 'Start Here',
        items: [
          { text: 'Home', link: '/' },
          { text: 'Quickstart', link: '/quickstart' },
          { text: 'One-Paste Installs', link: '/one-paste-installs' },
          { text: 'Marketplace', link: '/marketplace' },
          { text: 'Safety', link: '/safety' },
          { text: 'About', link: '/about' }
        ]
      },
      {
        text: 'Skills Library',
        collapsed: true,
        items: [
          { text: 'Overview', link: '/skills' },
          { text: 'Persona Architecture', link: '/persona-architecture' },
          { text: 'Advanced Packs', link: '/skills-categories/advanced-packs' },
          { text: 'Architecture & System Design', link: '/skills-categories/architecture' },
          { text: 'Frontend Engineering', link: '/skills-categories/frontend' },
          { text: 'Backend & API Design', link: '/skills-categories/backend' },
          { text: 'Quality Assurance', link: '/skills-categories/qa' },
          { text: 'DevOps & Infrastructure', link: '/skills-categories/devops' },
          { text: 'Security & Compliance', link: '/skills-categories/security' },
          { text: 'Data & Analytics', link: '/skills-categories/data' },
          { text: 'Product & UX', link: '/skills-categories/product' },
          { text: 'Content & Communication', link: '/skills-categories/content' },
          { text: 'Business & Operations', link: '/skills-categories/business' },
          { text: 'AI/ML Engineering', link: '/skills-categories/ai-ml' }
        ]
      },
      {
        text: 'Reference',
        collapsed: true,
        items: [
          { text: 'Providers', link: '/providers' },
          { text: 'Cost Routing', link: '/cost-routing' },
          { text: 'Dashboard', link: '/dashboard' },
          { text: 'Benchmarks', link: '/benchmarks' },
          { text: 'Cinematic Upgrade', link: '/cinematic-upgrade' },
          { text: 'FAQ', link: '/faq' },
          { text: 'Roadmap', link: '/roadmap' }
        ]
      }
    ],
    socialLinks: [{ icon: 'github', link: 'https://github.com/jamiojala/skillforge' }],
    search: {
      provider: 'local'
    },
    outline: [2, 3],
    outlineTitle: 'On this page',
    editLink: {
      pattern: 'https://github.com/jamiojala/skillforge/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
    docFooter: {
      prev: 'Previous',
      next: 'Next'
    },
    footer: {
      message: 'Apache-2.0 licensed. Built for serious multi-model workflows.',
      copyright: 'Copyright © 2026 SkillForge contributors'
    }
  }
})
