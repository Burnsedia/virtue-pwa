<template>
  <div>
    <select v-model="selectedProjectId" class="select select-bordered mb-6">
      <option disabled value="">Select a project</option>
      <option v-for="project in projects" :key="project.id" :value="project.id">
        {{ project.name }}
      </option>
    </select>

    <div v-if="selectedProjectId" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
      <div class="bg-base-200 border border-secondary h-96">
        <Task :priorities="[1]" :project-id="selectedProjectId" />
      </div>
      <div class="bg-base-200 border border-primary h-96">
        <Task :priorities="[2]" :project-id="selectedProjectId" />
      </div>
      <div class="bg-base-200 border border-success h-96">
        <Task :priorities="[3]" :project-id="selectedProjectId" />
      </div>
      <div class="bg-base-200 border border-alert h-96">
        <Task :priorities="[4]" :project-id="selectedProjectId" />
      </div>
    </div>
  </div>
</template>

<script>
import Task from './task.vue';

export default {
  components: { Task },
  data() {
    return {
      projects: [],
      selectedProjectId: ''
    };
  },
  async created() {
    const res = await fetch('http://localhost:8000/api/projects/');
    const data = await res.json();
    this.projects = data;
  }
};
</script>
