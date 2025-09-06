<template>
  <div class="max-w-5xl mx-auto p-4">
    <CreateProjectModal @created="fetchProjects" />

    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>Project Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="project in projects" :key="project.id">
            <td>{{ project.name }}</td>
            <td>{{ project.description }}</td>
            <td>
              <button @click="deleteProject(project.id)" class="btn btn-error btn-sm">
                🗑 Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import CreateProjectModal from './CreateProject.vue';

export default {
  components: { CreateProjectModal },
  data() {
    return {
      projects: [],
    };
  },
  created() {},
  mounted() {
    this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      const res = await fetch('http://localhost:8000/api/projects/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.projects = await res.json();
    },
    async deleteProject(projectId) {
      if (!confirm('Are you sure you want to delete this project?')) return;

      const res = await fetch(`http://localhost:8000/api/projects/${projectId}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (res.ok) {
        alert('Project deleted.');
        this.fetchProjects();
      } else {
        alert('Error deleting project.');
      }
    },
  },
};
</script>
