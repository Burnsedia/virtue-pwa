<template>
  <div class="bg-white p-3 mb-3 rounded shadow cursor-grab">
    {{ issue.title }}
  </div>
</template>

<script>
export default {
  props: {
    issue: Object,
  },
};
</script>
