<template>
  <div>
    <table class="table">
      <thead>
          <th>Task</th>
          <th>Done</th>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id">
          <td>{{ task.text }}</td>
          <td>{{ task.isCompleted }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
export default {
  props: {
    priorities: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      tasks: []
    };
  },
  computed: {
    filteredTasks() {
      return this.tasks.filter(task => this.priorities.includes(task.Priority));
    }
  },
  methods: {
    async getTasks() {
      try {
        const response = await fetch('http://localhost:3000/Issues');
        const data = await response.json();
        this.tasks = data;
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    }
  },
  created() {
    this.getTasks();
  }
}
</script>
