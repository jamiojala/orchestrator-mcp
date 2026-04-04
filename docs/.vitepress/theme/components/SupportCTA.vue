<script setup lang="ts">
defineProps<{
  title: string
  body: string
  primaryLabel: string
  primaryHref: string
  secondaryLabel?: string
  secondaryHref?: string
}>()
</script>

<template>
  <aside class="sf-support-cta sf-support-cta--prominent">
    <div class="sf-support-cta__inner">
      <div class="sf-support-cta__badge">
        <span class="sf-support-cta__heart" aria-hidden="true">&#9829;</span>
        Open source needs support
      </div>
      <h2 class="sf-section-heading__title">{{ title }}</h2>
      <p class="sf-support-cta__body">{{ body }}</p>
      <div class="sf-inline-actions">
        <a class="sf-btn sf-btn--primary" :href="primaryHref">{{ primaryLabel }}</a>
        <a v-if="secondaryLabel && secondaryHref" class="sf-btn sf-btn--sponsor" :href="secondaryHref">
          <span class="sf-btn__heart" aria-hidden="true">&#9829;</span>
          {{ secondaryLabel }}
        </a>
      </div>
    </div>
  </aside>
</template>
