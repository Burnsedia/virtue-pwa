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
                <button @click="selectedProject = project; showReportModal = true" class="btn btn-info btn-sm mr-2">
                  View Report
                </button>
                <button @click="deleteProject(project.id)" class="btn btn-error btn-sm">
                  🗑 Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Report Modal -->
    <div v-if="showReportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-2xl">
        <ProjectReport :project="selectedProject" />
        <div class="flex justify-end mt-4">
          <button @click="showReportModal = false" class="btn">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CreateProjectModal from './CreateProject.vue';
import CreateOrganizationModal from './CreateOrganizationModal.vue';
import ProjectReport from './ProjectReport.vue';
import authStatus from "../mixins/authStatus";
import { db } from '../lib/db';

export default {
  components: { CreateProjectModal, CreateOrganizationModal, ProjectReport },
  mixins: [authStatus],
  data() {
    return {
      projects: [],
      organizations: [],
      showReportModal: false,
      selectedProject: null,
    };
  },
  created() {},
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      // Load from IndexedDB first
      this.projects = await db.getAll('projects');
      this.organizations = await db.getAll('organizations');

      // Then fetch from network
      this.fetchProjects();
      this.fetchOrganizations();
    },
    async fetchProjects() {
      try {
        const res = await fetch('http://localhost:8000/api/projects/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const projects = await res.json();
        this.projects = projects;
        await db.setAll('projects', projects);
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    },
    async fetchOrganizations() {
      try {
        const res = await fetch('http://localhost:8000/api/organizations/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const organizations = await res.json();
        this.organizations = organizations;
        await db.setAll('organizations', organizations);
      } catch (error) {
        console.error('Error fetching organizations:', error);
      }
    },
    async deleteProject(projectId) {
      if (!confirm('Are you sure you want to delete this project?')) return;

      try {
        const res = await fetch(`http://localhost:8000/api/projects/${projectId}/`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (res.ok) {
          alert('Project deleted.');
          await db.delete('projects', projectId);
          this.projects = this.projects.filter(p => p.id !== projectId);
        } else {
          alert('Error deleting project.');
        }
      } catch (error) {
        console.error('Error deleting project:', error);
      }
    },
  },
};
</script>
