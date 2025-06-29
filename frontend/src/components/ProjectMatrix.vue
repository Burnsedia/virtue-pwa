<template>
  <div class="max-w-5xl mx-auto p-4">
    <CreateProjectModal @created="fetchProjects" />

    <select v-model="selectedProjectId" class="select select-bordered mb-6 w-full">
      <option disabled value="">-- Choose Project --</option>
      <option v-for="project in projects" :key="project.id" :value="project.id">
        {{ project.name }}
      </option>
    </select>

    <div v-if="selectedProjectId" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
      <div class="bg-base-200 border border-secondary h-96 p-2">
        <Task :priorities="[1]" :project-id="selectedProjectId" />
      </div>
      <div class="bg-base-200 border border-primary h-96 p-2">
        <Task :priorities="[2]" :project-id="selectedProjectId" />
      </div>
      <div class="bg-base-200 border border-success h-96 p-2">
        <Task :priorities="[3]" :project-id="selectedProjectId" />
      </div>
      <div class="bg-base-200 border border-alert h-96 p-2">
        <Task :priorities="[4]" :project-id="selectedProjectId" />
      </div>
    </div>
  </div>
</template>

<script>
import Task from './task.vue';
import CreateProjectModal from './CreateProject.vue';

export default {
  components: { Task, CreateProjectModal },
  data() {
    return {
      projects: [],
      selectedProjectId: ''
    };
  },
  created() {
    this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      const res = await fetch('http://localhost:8000/api/projects/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      this.projects = await res.json();
    }
  }
};
</script>
