<template>
  <div class="max-w-5xl mx-auto p-4">
    <div class="flex items-center justify-between mb-4">
      <select v-model="selectedProjectId" class="select select-bordered w-full">
        <option disabled value="">-- Choose Project --</option>
        <option v-for="project in projects" :key="project.id" :value="project.id">
          {{ project.name }}
        </option>
      </select>
    </div>

    <div v-if="selectedProjectId" class="grid grid-cols-3 gap-4">
      <div class="bg-base-200 p-4 rounded-lg">
        <h2 class="text-xl font-bold mb-4">To Do</h2>
        <div
          class="min-h-[200px]"
          @dragover.prevent
          @drop="onDrop($event, 'todo')"
        >
          <div
            v-for="issue in getIssuesByStatus('todo')"
            :key="issue.id"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
            class="bg-white p-3 mb-3 rounded shadow cursor-grab"
          >
            {{ issue.title }}
          </div>
        </div>
      </div>

      <div class="bg-base-200 p-4 rounded-lg">
        <h2 class="text-xl font-bold mb-4">In Progress</h2>
        <div
          class="min-h-[200px]"
          @dragover.prevent
          @drop="onDrop($event, 'in_progress')"
        >
          <div
            v-for="issue in getIssuesByStatus('in_progress')"
            :key="issue.id"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
            class="bg-white p-3 mb-3 rounded shadow cursor-grab"
          >
            {{ issue.title }}
          </div>
        </div>
      </div>

      <div class="bg-base-200 p-4 rounded-lg">
        <h2 class="text-xl font-bold mb-4">Done</h2>
        <div
          class="min-h-[200px]"
          @dragover.prevent
          @drop="onDrop($event, 'done')"
        >
          <div
            v-for="issue in getIssuesByStatus('done')"
            :key="issue.id"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
            class="bg-white p-3 mb-3 rounded shadow cursor-grab"
          >
            {{ issue.title }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      projects: [],
      selectedProjectId: '',
      issues: [],
    };
  },
  created() {
    this.fetchProjects();
  },
  watch: {
    selectedProjectId() {
      this.fetchIssues();
    },
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
    async fetchIssues() {
      if (!this.selectedProjectId) return;
      const res = await fetch(
        `http://localhost:8000/api/issues/?project=${this.selectedProjectId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      );
      this.issues = await res.json();
    },
    getIssuesByStatus(status) {
      return this.issues.filter((issue) => issue.status === status);
    },
    onDragStart(event, issue) {
      event.dataTransfer.setData('application/json', JSON.stringify(issue));
    },
    async onDrop(event, status) {
      const issueData = JSON.parse(
        event.dataTransfer.getData('application/json')
      );
      const issue = this.issues.find((i) => i.id === issueData.id);
      if (issue) {
        issue.status = status;
        // Update the issue status in the backend
        await fetch(`http://localhost:8000/api/issues/${issue.id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ status: status }),
        });
      }
    },
  },
};
</script>
