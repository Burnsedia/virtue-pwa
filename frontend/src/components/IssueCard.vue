<template>
  <div class="bg-base-300 p-3 mb-3 rounded shadow cursor-grab text-gray-800 hover:bg-gray-100 transition-colors duration-200">
    <h4 class="font-semibold text-lg">{{ issue.title }}</h4>
    <p class="text-sm text-gray-600">{{ issue.description }}</p>
  </div>
</template>

<script>
export default {
  props: {
    issue: Object,
  },
};
</script>
