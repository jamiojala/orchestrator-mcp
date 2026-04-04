<script setup lang="ts">
import HeroSection from './HeroSection.vue'
import SponsorTier from './SponsorTier.vue'
import SupportCTA from './SupportCTA.vue'
import { getPageUrl } from '../lib/catalog'

const tiers = [
  {
    name: 'Supporter',
    price: '$10/mo',
    body: 'Help keep 302 skill packs maintained, tested, and free for everyone.',
    benefits: [
      'Name on the public sponsor wall',
      'Early visibility into roadmap updates',
      'The knowledge that this work continues because of you'
    ],
    cta: 'Start sponsoring',
    link: 'https://github.com/sponsors/jamiojala',
    featured: false
  },
  {
    name: 'Advocate',
    price: '$50/mo',
    body: 'For teams that depend on the packs daily and want them to get better faster.',
    benefits: [
      'Everything in Supporter',
      'Priority acknowledgement in docs and releases',
      'Input on which packs and domains ship next'
    ],
    cta: 'Become an Advocate',
    link: 'https://github.com/sponsors/jamiojala',
    featured: true
  },
  {
    name: 'Champion',
    price: '$250/mo',
    body: 'For organizations that want a portable, open skill layer to exist in the world.',
    benefits: [
      'Everything in Advocate',
      'Quarterly maintainer sync (async or call)',
      'Logo placement on the docs site and README',
      'Direct influence on the project roadmap'
    ],
    cta: 'Back SkillForge',
    link: 'https://github.com/sponsors/jamiojala',
    featured: false
  }
]

const whatMoneyFunds = [
  {
    title: 'New skill packs',
    body: 'Each pack takes 2–4 hours to research, write, validate, and document. 302 packs exist because someone sat down and did the work.',
    icon: '+'
  },
  {
    title: 'Maintenance',
    body: 'Frameworks change, models evolve, best practices shift. Without ongoing maintenance, packs rot within months.',
    icon: '↻'
  },
  {
    title: 'Docs and infrastructure',
    body: 'The catalog site, search, CLI tooling, safety checks, CI pipeline — none of it maintains itself.',
    icon: '◈'
  },
  {
    title: 'Independence',
    body: 'Sponsorship means SkillForge stays independent. No vendor deals, no gated tiers, no rug pulls.',
    icon: '◉'
  }
]
</script>

<template>
  <div class="sf-page">
    <HeroSection
      eyebrow="Support"
      title="This project survives on sponsorship."
      lead="SkillForge is free, open source, and maintained by one person. Sponsorship is the only reason it exists — and the only way it keeps going."
    >
      <template #title>
        This project survives on<br><span class="sf-gradient-text--primary">sponsorship.</span>
      </template>
      <template #actions>
        <a class="sf-btn sf-btn--sponsor sf-btn--lg" href="https://github.com/sponsors/jamiojala">
          <span class="sf-btn__heart" aria-hidden="true">&#9829;</span>
          Sponsor on GitHub
        </a>
        <a class="sf-btn sf-btn--secondary" href="https://github.com/jamiojala/skillforge">View the repo</a>
      </template>
    </HeroSection>

    <!-- Maintainer story -->
    <section class="sf-shell sf-section">
      <div class="sf-maintainer-story">
        <div class="sf-maintainer-story__content">
          <p class="sf-kicker">The maintainer</p>
          <h2 class="sf-section-heading__title">Built by one person. Used by many.</h2>
          <p>
            I'm Jami, and I build SkillForge because I got tired of re-writing the same skill prompts
            for every new coding agent that came out. The packs should be portable, the manifests
            should be readable, and the whole thing should be free.
          </p>
          <p>
            This is not a VC-funded product with a runway. It is an open-source project that runs on
            evenings, weekends, and the direct support of people who use it. Every sponsorship dollar
            goes toward making the catalog better — not toward office rent or marketing spend.
          </p>
        </div>
        <div class="sf-maintainer-story__numbers">
          <div class="sf-maintainer-story__stat">
            <strong>302</strong>
            <span>skill packs shipped</span>
          </div>
          <div class="sf-maintainer-story__stat">
            <strong>14</strong>
            <span>domain categories</span>
          </div>
          <div class="sf-maintainer-story__stat">
            <strong>20</strong>
            <span>advanced first-party packs</span>
          </div>
          <div class="sf-maintainer-story__stat">
            <strong>1</strong>
            <span>maintainer</span>
          </div>
        </div>
      </div>
    </section>

    <!-- What money funds -->
    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Where your money goes</p>
        <h2 class="sf-section-heading__title">Transparent, specific, and boring on purpose.</h2>
        <p class="sf-section-heading__lead">
          No "community events" or "marketing budget." Here is exactly what sponsorship pays for.
        </p>
      </div>

      <div class="sf-grid sf-grid--2">
        <article v-for="item in whatMoneyFunds" :key="item.title" class="sf-fund-card">
          <span class="sf-fund-card__icon" aria-hidden="true">{{ item.icon }}</span>
          <div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.body }}</p>
          </div>
        </article>
      </div>
    </section>

    <!-- Sponsor tiers -->
    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Sponsor tiers</p>
        <h2 class="sf-section-heading__title">Pick the level that matches what SkillForge is worth to you.</h2>
        <p class="sf-section-heading__lead">
          All tiers go through GitHub Sponsors. Cancel anytime. One-time donations are also welcome.
        </p>
      </div>

      <div class="sf-sponsor-grid sf-sponsor-grid--featured">
        <SponsorTier v-for="tier in tiers" :key="tier.name" :tier="tier" />
      </div>

      <p class="sf-support-note">
        Prefer a one-time donation? You can do that on
        <a href="https://github.com/sponsors/jamiojala">GitHub Sponsors</a> too —
        just pick "One-time" instead of "Monthly."
      </p>
    </section>

    <!-- Sponsor wall — invitational empty state -->
    <section class="sf-shell sf-section">
      <div class="sf-section-heading">
        <p class="sf-kicker">Sponsor wall</p>
        <h2 class="sf-section-heading__title">People who keep SkillForge alive.</h2>
      </div>

      <div class="sf-sponsor-wall-empty">
        <div class="sf-sponsor-wall-empty__placeholder" aria-hidden="true">
          <span class="sf-sponsor-wall-empty__slot" v-for="n in 6" :key="n">?</span>
        </div>
        <h3>Your name could be here.</h3>
        <p>
          No sponsors listed yet. If SkillForge saves your team even one hour a week, consider
          being the first visible supporter. It is a real signal — both to the maintainer and
          to every other developer deciding whether to depend on this project.
        </p>
        <a class="sf-btn sf-btn--sponsor" href="https://github.com/sponsors/jamiojala">
          <span class="sf-btn__heart" aria-hidden="true">&#9829;</span>
          Be the first sponsor
        </a>
      </div>
    </section>

    <!-- Non-monetary contribution -->
    <section class="sf-shell sf-section">
      <SupportCTA
        title="Not ready to sponsor? You can still help."
        body="Open a high-quality PR, improve the docs, file focused issues, or share SkillForge with teams already juggling multiple coding agents. Every contribution matters."
        primary-label="Contribute on GitHub"
        :primary-href="getPageUrl('/contribute')"
        secondary-label="Browse the Catalog"
        :secondary-href="getPageUrl('/skills/')"
      />
    </section>
  </div>
</template>
