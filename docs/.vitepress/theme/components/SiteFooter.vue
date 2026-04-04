<script setup lang="ts">
import NewsletterSignup from './NewsletterSignup.vue'
import { getPageUrl } from '../lib/catalog'

const columns = [
  {
    title: 'Product',
    links: [
      { label: 'Skills Catalog', href: getPageUrl('/skills/') },
      { label: 'Discover', href: getPageUrl('/discover') },
      { label: 'Advanced Packs', href: getPageUrl('/skills/?domain=advanced-packs') },
      { label: 'Support', href: getPageUrl('/support') }
    ]
  },
  {
    title: 'Resources',
    links: [
      { label: 'Quickstart', href: getPageUrl('/quickstart') },
      { label: 'One-Paste Installs', href: getPageUrl('/one-paste-installs') },
      { label: 'Safety', href: getPageUrl('/safety') },
      { label: 'Roadmap', href: getPageUrl('/roadmap') }
    ]
  },
  {
    title: 'Build',
    links: [
      { label: 'Contribute', href: getPageUrl('/contribute') },
      { label: 'Contribution Guide', href: getPageUrl('/contributing/') },
      { label: 'Review Process', href: getPageUrl('/contributing/review-process') },
      { label: 'Recognition', href: getPageUrl('/contributing/recognition') }
    ]
  },
  {
    title: 'Connect',
    links: [
      { label: 'GitHub', href: 'https://github.com/jamiojala/skillforge' },
      { label: 'GitHub Sponsors', href: 'https://github.com/sponsors/jamiojala' },
      { label: 'About', href: getPageUrl('/about') },
      { label: 'Community', href: getPageUrl('/community') }
    ]
  }
]
</script>

<template>
  <footer class="sf-site-footer">
    <div class="sf-site-footer__top">
      <div class="sf-site-footer__brand">
        <p class="sf-kicker">SkillForge</p>
        <h2>One skill library for every coding agent.</h2>
        <p>
          302 portable skill packs, maintained in public, designed to work across Codex,
          Claude Code, Kimi Code, and any MCP-capable client.
        </p>
        <NewsletterSignup />
      </div>

      <div class="sf-site-footer__grid">
        <nav v-for="column in columns" :key="column.title" class="sf-site-footer__column" :aria-label="column.title">
          <h3>{{ column.title }}</h3>
          <a v-for="link in column.links" :key="link.label" :href="link.href">{{ link.label }}</a>
        </nav>
      </div>
    </div>

    <div class="sf-site-footer__bottom">
      <p>© 2026 SkillForge. Open source under MIT License.</p>
      <div class="sf-site-footer__legal">
        <a :href="getPageUrl('/privacy')">Privacy</a>
        <a :href="getPageUrl('/terms')">Terms</a>
        <a :href="getPageUrl('/license')">License</a>
      </div>
    </div>
  </footer>
</template>
