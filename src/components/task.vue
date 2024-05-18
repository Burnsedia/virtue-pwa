<template>
  <div>
    <h1>Tasks</h1>
    <table>
      <tr>
        <th>id</th>
        <th>text</th>
        <th>isCompleted</th>
        <th>Priority</th>
      </tr>
      <tr v-for="task in filteredTasks" :key="task.id">
        <td>{{ task.id }}</td>
        <td>{{ task.text }}</td>
        <td>{{ task.isCompleted }}</td>
        <td>{{ task.Priority }}</td>
      </tr>
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
