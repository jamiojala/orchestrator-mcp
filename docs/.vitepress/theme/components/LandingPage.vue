<script setup lang="ts">
import ComparisonTable from './ComparisonTable.vue'
import HeroSection from './HeroSection.vue'
import OpenSourceBadges from './OpenSourceBadges.vue'
import ProcessSteps from './ProcessSteps.vue'
import SkillGrid from './SkillGrid.vue'
import SupportCTA from './SupportCTA.vue'
import TrustBar from './TrustBar.vue'
import {
  getCatalogFilterUrl,
  getFeaturedSkills,
  getPageUrl,
  homepageStats,
  siteCatalog
} from '../lib/catalog'

const featuredSkills = getFeaturedSkills(6)
const spotlightIds = featuredSkills.slice(0, 1).map((skill) => skill.slug)
const topCollections = [...siteCatalog.collections].sort((left, right) => right.count - left.count).slice(0, 6)

const processSteps = [
  {
    title: 'Browse',
    body: 'Pick from 302 skill packs across 14 domains. Every pack has a readable manifest — no hidden prompt blobs.'
  },
  {
    title: 'Install or export',
    body: 'Run the MCP runtime for full orchestration, or export individual packs into any markdown-first workflow.'
  },
  {
    title: 'Ship',
    body: 'Compose packs with explicit triggers, model preferences, and validation hooks. Version everything on GitHub.'
  }
]

const comparisonRows = [
  {
    label: 'Portability',
    other: 'Skills locked to one client or proprietary marketplace.',
    skillforge: 'SKILL.md + YAML packs that move freely between Codex, Claude Code, Kimi Code, and more.'
  },
  {
    label: 'Transparency',
    other: 'Opaque prompt blobs you cannot inspect or audit.',
    skillforge: 'Every pack has a readable manifest with role, voice, reasoning steps, and validation hooks.'
  },
  {
    label: 'Contributing',
    other: 'Closed catalogs or complex submission pipelines.',
    skillforge: 'Fork, add a pack, open a PR. GitHub is the entire workflow.'
  },
  {
    label: 'Cost',
    other: 'Paywalls, subscription tiers, or duplicated per-client setups.',
    skillforge: 'Free, open-source, MIT licensed. No gatekeeping.'
  }
]
</script>

<template>
  <div class="sf-page">
    <HeroSection
      eyebrow="Open-source · 302 skills · MIT licensed"
      title="One skill library for every coding agent."
      lead="Portable skill packs for Codex, Claude Code, Kimi Code, and any MCP-capable client. Browse, install, export. No vendor lock-in."
    >
      <template #title>
        One skill library for<br><span class="sf-gradient-text--primary">every coding agent.</span>
      </template>
      <template #actions>
        <a class="sf-btn sf-btn--primary" :href="getPageUrl('/skills/')">Browse 302 Skills</a>
        <a class="sf-btn sf-btn--secondary" href="https://github.com/jamiojala/skillforge">GitHub</a>
        <a class="sf-btn sf-btn--ghost" :href="getPageUrl('/support')">Support this project</a>
      </template>
    </HeroSection>

    <TrustBar :stats="homepageStats" />

    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Featured packs</p>
        <h2 class="sf-section-heading__title">Real skills you can inspect before you install.</h2>
        <p class="sf-section-heading__lead">
          Every pack ships with a readable manifest — role, voice, reasoning steps, validation hooks.
          No prompt blobs.
        </p>
      </div>

      <SkillGrid :skills="featuredSkills" :featured-ids="spotlightIds" />

      <a class="sf-inline-link" :href="getPageUrl('/skills/')">View all {{ siteCatalog.stats.totalSkills }}+ skills</a>
    </section>

    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">14 domains</p>
        <h2 class="sf-section-heading__title">Organized by what you actually build.</h2>
        <p class="sf-section-heading__lead">
          Not a flat list. Clear lanes from frontend to security to AI/ML so you find what you need fast.
        </p>
      </div>

      <div class="sf-bento-grid">
        <a
          v-for="collection in topCollections"
          :key="collection.slug"
          class="sf-collection-card"
          :href="getCatalogFilterUrl(collection.slug)"
        >
          <span class="sf-collection-card__count">{{ collection.count }}</span>
          <h3>{{ collection.collectionTitle }}</h3>
          <p>{{ collection.description }}</p>
          <span class="sf-card-link">Browse collection</span>
        </a>
      </div>
    </section>

    <!-- Mid-page support nudge -->
    <section class="sf-shell sf-section">
      <aside class="sf-support-nudge">
        <div class="sf-support-nudge__content">
          <p class="sf-support-nudge__eyebrow">Built by one maintainer, used by many</p>
          <h2 class="sf-support-nudge__title">This project runs on sponsorship, not VC money.</h2>
          <p class="sf-support-nudge__body">
            SkillForge is maintained in the open by a solo developer. Every skill pack, every docs page,
            every safety check — built and shipped without corporate backing. If this saves your team time,
            a sponsorship keeps it alive.
          </p>
          <div class="sf-inline-actions">
            <a class="sf-btn sf-btn--primary" href="https://github.com/sponsors/jamiojala">Sponsor on GitHub</a>
            <a class="sf-btn sf-btn--secondary" :href="getPageUrl('/support')">See what your money funds</a>
          </div>
        </div>
        <div class="sf-support-nudge__stats">
          <div class="sf-support-nudge__stat">
            <strong>302</strong>
            <span>skill packs maintained</span>
          </div>
          <div class="sf-support-nudge__stat">
            <strong>14</strong>
            <span>domain categories</span>
          </div>
          <div class="sf-support-nudge__stat">
            <strong>1</strong>
            <span>maintainer</span>
          </div>
        </div>
      </aside>
    </section>

    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Get started</p>
        <h2 class="sf-section-heading__title">Two ways in: run the runtime, or just grab the packs.</h2>
      </div>

      <ProcessSteps
        :steps="processSteps"
        code-example="pip install &quot;orchestrator-mcp[dashboard]&quot;
orchestrator-mcp skills list
orchestrator-mcp skills export liquid-glass-enforcer --to ./skillforge-packs"
      />
    </section>

    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Why SkillForge</p>
        <h2 class="sf-section-heading__title">Skills should be infrastructure, not disposable prompt scraps.</h2>
      </div>

      <ComparisonTable :rows="comparisonRows" />
    </section>

    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Open by default</p>
        <h2 class="sf-section-heading__title">MIT licensed, GitHub native, no hidden backend.</h2>
      </div>
      <OpenSourceBadges />
    </section>

    <section class="sf-shell sf-section">
      <SupportCTA
        title="Use it free. Fund it if it matters to you."
        body="The catalog is free forever. Sponsorship funds new packs, better docs, and the maintenance that keeps 302 skills from rotting."
        primary-label="Get Started Free"
        :primary-href="getPageUrl('/quickstart')"
        secondary-label="Become a Sponsor"
        :secondary-href="getPageUrl('/support')"
      />
    </section>
  </div>
</template>
