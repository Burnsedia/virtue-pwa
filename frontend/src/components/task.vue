<template>
  <div>
    <table class="table">
      <thead>
        <tr>
          <th>Task</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id">
          <td>{{ task.title }}</td>
          <td>
            <span :class="{
              'text-success': task.status === 'done',
              'text-warning': task.status === 'in_progress',
              'text-error': task.status === 'todo'
            }">
              {{ task.status }}
            </span>
          </td>
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
      return this.tasks.filter(task => this.priorities.includes(task.priority));
    }
  },
  methods: {
    async getTasks() {
      try {
        const response = await fetch('http://localhost:8000/api/issues/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
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
};
</script>
