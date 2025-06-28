// create a new task
<template>
  <div>
    <h1>Tasks</h1>
    <form @submit.prevent="addTask">
      <input v-model="newTask.text" placeholder="New Task" required />
      <select v-model="newTask.Priority">
        <option v-for="n in 4" :key="n" :value="n">{{ n }}</option>
      </select>
      <button type="submit">Add Task</button>
    </form>
    <table>
      <tr>
        <th>id</th>
        <th>text</th>
        <th>isCompleted</th>
        <th>Priority</th>
        <th>Actions</th>
      </tr>
      <tr v-for="task in tasks" :key="task.id">
        <td>{{ task.id }}</td>
        <td>{{ task.text }}</td>
        <td>{{ task.isCompleted }}</td>
        <td>{{ task.Priority }}</td>
        <td>
          <button @click="deleteTask(task.id)">Delete</button>
          <button @click="editTask(task)">Edit</button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tasks: [],
      newTask: {
        text: '',
        isCompleted: false,
        Priority: 1
      }
    };
  },
  methods: {
    async fetchTasks() {
      try {
        const response = await fetch('http://localhost:3000/Issues');
        this.tasks = await response.json();
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    },
    async addTask() {
      try {
        const response = await fetch('http://localhost:3000/Issues', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newTask)
        });
        const addedTask = await response.json();
        this.tasks.push(addedTask);
        this.newTask.text = '';
        this.newTask.Priority = 1;
      } catch (error) {
        console.error('Error adding task:', error);
      }
    },
    async deleteTask(id) {
      try {
        await fetch(`http://localhost:3000/Issues/${id}`, {
          method: 'DELETE'
        });
        this.tasks = this.tasks.filter(task => task.id !== id);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    },
    async editTask(task) {
      const updatedText = prompt('Update Task', task.text);
      if (updatedText !== null) {
        const updatedTask = { ...task, text: updatedText };
        try {
          await fetch(`http://localhost:3000/Issues/${task.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedTask)
          });
          this.tasks = this.tasks.map(t => (t.id === task.id ? updatedTask : t));
        } catch (error) {
          console.error('Error updating task:', error);
        }
      }
    }
  },
  created() {
    this.fetchTasks();
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background-color: #f2f2f2;
}
</style>

