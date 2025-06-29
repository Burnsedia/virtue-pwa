<template>
  <div>
    <table class="table table-sm w-full">
      <thead>
        <tr>
          <th>Task</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id">
          <td>{{ task.title }}</td>
          <td>{{ task.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    priorities: Array,
    projectId: Number
  },
  data() {
    return {
      tasks: []
    };
  },
  computed: {
    filteredTasks() {
      return this.tasks.filter(
        task =>
          this.priorities.includes(task.priority) &&
          task.project === this.projectId
      );
    }
  },
  methods: {
    async getTasks() {
      const res = await fetch('http://localhost:8000/api/issues/');
      const data = await res.json();
      this.tasks = data;
    }
  },
  created() {
    this.getTasks();
  }
};
</script>
