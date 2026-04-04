<script setup lang="ts">
import { getPageUrl } from '../lib/catalog'
</script>

<template>
  <div class="sf-open-source-badges">
    <a :href="getPageUrl('/license')">
      <strong>Apache-2.0 licensed</strong>
      <span>Portable by default, permissive by design.</span>
    </a>
    <a :href="getPageUrl('/safety')">
      <strong>Open source safety</strong>
      <span>Public hygiene guidance, release scanning, and transparent constraints.</span>
    </a>
    <a href="https://github.com/jamiojala/skillforge">
      <strong>GitHub native</strong>
      <span>Fork, add a pack, and submit a pull request without a hidden backend.</span>
    </a>
  </div>
</template>
