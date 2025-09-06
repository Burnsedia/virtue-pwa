<template>
  <div class="max-w-5xl mx-auto p-4">
    <div>
      <CreateProjectModal @created="fetchProjects" />
      <CreateOrganizationModal @created="fetchOrganizations" />

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
  </div>
</template>

<script>
import CreateProjectModal from './CreateProject.vue';
import CreateOrganizationModal from './CreateOrganizationModal.vue';
import authStatus from "../mixins/authStatus";

export default {
  components: { CreateProjectModal, CreateOrganizationModal },
  mixins: [authStatus],
  data() {
    return {
      projects: [],
      organizations: [],
    };
  },
  created() {},
  mounted() {
    this.fetchProjects();
    this.fetchOrganizations();
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
    async fetchOrganizations() {
      const res = await fetch('http://localhost:8000/api/organizations/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.organizations = await res.json();
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
