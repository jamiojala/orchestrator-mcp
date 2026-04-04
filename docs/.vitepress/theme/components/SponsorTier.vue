<script setup lang="ts">
defineProps<{
  tier: {
    name: string
    price: string
    body: string
    benefits: string[]
    cta: string
    link: string
    featured?: boolean
  }
}>()
</script>

<template>
  <article class="sf-sponsor-tier" :class="{ 'sf-sponsor-tier--featured': tier.featured }">
    <div v-if="tier.featured" class="sf-sponsor-tier__badge">Most popular</div>
    <p class="sf-kicker">{{ tier.featured ? 'Recommended' : 'Sponsor tier' }}</p>
    <h3>{{ tier.name }}</h3>
    <div class="sf-sponsor-tier__price">
      {{ tier.price }}
      <span class="sf-sponsor-tier__period">/ month</span>
    </div>
    <p>{{ tier.body }}</p>
    <ul class="sf-sponsor-tier__benefits">
      <li v-for="benefit in tier.benefits" :key="benefit">
        <span class="sf-sponsor-tier__check" aria-hidden="true">&#10003;</span>
        {{ benefit }}
      </li>
    </ul>
    <a
      class="sf-btn"
      :class="tier.featured ? 'sf-btn--sponsor sf-btn--lg' : 'sf-btn--primary'"
      :href="tier.link"
    >
      <span v-if="tier.featured" class="sf-btn__heart" aria-hidden="true">&#9829;</span>
      {{ tier.cta }}
    </a>
  </article>
</template>
