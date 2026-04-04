<script setup lang="ts">
defineProps<{
  eyebrow: string
  title: string
  lead: string
}>()

const terminalSkills = [
  { name: 'liquid-glass-enforcer',       fill: 100, tag: 'Featured',  featured: true  },
  { name: 'rust-async-patterns',         fill: 88,  tag: 'v2.0',      featured: false },
  { name: 'react-best-practices',        fill: 82,  tag: 'Popular',   featured: false },
  { name: 'graphql-federation-gateway',  fill: 74,  tag: '',          featured: false },
  { name: 'prompt-injection-defender',   fill: 68,  tag: 'Security',  featured: false },
]
</script>

<template>
  <section class="sf-hero" aria-label="Hero">
    <!-- Aurora background -->
    <div class="sf-hero__aurora" aria-hidden="true"></div>

    <!-- Dot grid texture -->
    <div class="sf-hero__grid-bg" aria-hidden="true"></div>

    <!-- Centered copy block -->
    <div class="sf-hero__center">
      <!-- Eyebrow -->
      <div class="sf-hero__eyebrow">
        <span class="sf-hero__live-dot" aria-hidden="true"></span>
        {{ eyebrow }}
      </div>

      <!-- Title (accepts rich #title slot or falls back to prop) -->
      <h1 class="sf-display sf-display--hero sf-hero__title">
        <slot name="title">{{ title }}</slot>
      </h1>

      <!-- Lead -->
      <p class="sf-hero__lead">{{ lead }}</p>

      <!-- Actions slot -->
      <div class="sf-hero__actions">
        <slot name="actions" />
      </div>
    </div>

    <!-- Terminal mockup -->
    <div class="sf-hero__terminal" aria-label="SkillForge CLI preview">
      <!-- macOS-style window chrome -->
      <div class="sf-hero__terminal-header">
        <div class="sf-hero__terminal-dots" aria-hidden="true">
          <span class="sf-hero__terminal-dot"></span>
          <span class="sf-hero__terminal-dot"></span>
          <span class="sf-hero__terminal-dot"></span>
        </div>
        <span class="sf-hero__terminal-title">skillforge — browse</span>
      </div>

      <!-- Terminal body -->
      <div class="sf-hero__terminal-body">
        <!-- Command line -->
        <div class="sf-hero__terminal-line">
          <span class="sf-hero__terminal-prompt">$</span>
          <span class="sf-hero__terminal-cmd"> skillforge browse --featured</span>
        </div>

        <!-- Blank line after command -->
        <div class="sf-hero__terminal-spacer"></div>

        <!-- Skill rows -->
        <div
          v-for="skill in terminalSkills"
          :key="skill.name"
          class="sf-hero__terminal-row"
        >
          <span class="sf-hero__terminal-arrow">↳</span>
          <span class="sf-hero__terminal-name">{{ skill.name }}</span>
          <span class="sf-hero__terminal-bar">
            <span
              class="sf-hero__terminal-fill"
              :style="{ width: skill.fill + '%' }"
            ></span>
          </span>
          <span
            class="sf-hero__terminal-tag"
            :class="skill.featured ? 'sf-hero__terminal-tag--featured' : 'sf-hero__terminal-tag--muted'"
          >{{ skill.tag }}</span>
        </div>

        <!-- Status line -->
        <div class="sf-hero__terminal-status">
          <span class="sf-hero__terminal-status-dot" aria-hidden="true"></span>
          302 skills loaded &nbsp;·&nbsp; 14 domains &nbsp;·&nbsp; v2.0.0 &nbsp;·&nbsp; Apache-2.0
        </div>
      </div>
    </div>
  </section>
</template>
