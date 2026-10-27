<template>
  <div
    class="bg-gray-300 p-3 mb-3 rounded shadow cursor-grab text-gray-800 hover:bg-gray-100 transition-colors duration-200">
    <h4 class="font-semibold text-lg">{{ issue.title }}</h4>
    <p class="text-sm text-gray-600">{{ issue.description }}</p>
    <div v-if="priorityLabel" class="mt-1 text-xs font-medium text-gray-700">{{ priorityLabel }}</div>
    <div v-if="estimate" class="text-xs text-gray-500">{{ estimate }}</div>
  </div>
</template>

<script>
// Eisenhower-matrix priority labels. Kept consistent with the priority
// constants defined in src/test/utils.test.ts (1=Urgent&Important ... 4=Not
// Urgent&Not Important).
const PRIORITY_LABELS = {
  1: '🔥 Urgent & Important',
  2: '⚠️ Urgent & Not Important',
  3: '🌱 Not Urgent & Important',
  4: '🧘 Not Urgent & Not Important',
}

export default {
  props: {
    issue: Object,
  },
  computed: {
    priorityLabel() {
      if (!this.issue || !PRIORITY_LABELS[this.issue.priority]) return ''
      return PRIORITY_LABELS[this.issue.priority]
    },
    estimate() {
      if (this.issue && this.issue.estimate_minutes != null) {
        return `${this.issue.estimate_minutes} min`
      }
      return ''
    },
  },
};
</script>
