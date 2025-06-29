<template>
  <div>
    <CreateIssueModal :project-id="projectId" :priority="priorities[0]" @created="getTasks" />

    <table class="table table-sm w-full mt-2">
      <thead>
        <tr>
          <th>Task</th>
          <th>Status</th>
          <th>Edit</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id">
          <td>{{ task.title }}</td>
          <td>{{ task.status }}</td>
          <td>
            <EditIssueModal :issue="task" @updated="getTasks" />

          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import CreateIssueModal from './CreateIssueModal.vue';
import EditIssueModal from './EditIssueModal.vue';

export default {
  components: { CreateIssueModal, EditIssueModal },
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
      const res = await fetch('http://localhost:8000/api/issues/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      this.tasks = await res.json();
    }
  },
  created() {
    this.getTasks();
  }
};
</script>
