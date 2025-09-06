<template>
  <div
    draggable="true"
    @dragstart="onDragStart($event, issue)"
    class="bg-white p-3 mb-3 rounded shadow cursor-grab"
  >
    {{ issue.title }}
  </div>
</template>

<script>
export default {
  props: {
    issue: Object,
  },
  methods: {
    onDragStart(event, issue) {
      event.dataTransfer.setData("application/json", JSON.stringify(issue));
    },
  },
};
</script>
