<script setup lang="ts">
defineProps<{
  sponsors: Array<{
    name: string
    href: string
    description: string
  }>
}>()
</script>

<template>
  <div v-if="sponsors.length" class="sf-sponsor-grid">
    <a v-for="sponsor in sponsors" :key="sponsor.name" class="sf-resource-card" :href="sponsor.href">
      <p class="sf-resource-card__eyebrow">Supporter</p>
      <h3>{{ sponsor.name }}</h3>
      <p>{{ sponsor.description }}</p>
    </a>
  </div>
</template>
