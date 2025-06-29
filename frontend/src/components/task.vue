<template>
  <div>
    <table class="table w-full table-sm">
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
        task => this.priorities.includes(task.priority) && task.project === this.projectId
      );
    }
  },
  async created() {
    const res = await fetch('http://localhost:8000/api/issues/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    this.tasks = await res.json();
  }
};
</script>
