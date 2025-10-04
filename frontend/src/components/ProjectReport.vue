<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">Project Report: {{ project.name }}</h2>

    <div v-if="report">
      <div class="mb-6">
        <h3 class="text-xl font-bold">Total Time Spent</h3>
        <p>{{ formatDuration(report.total_time_spent) }}</p>
      </div>

      <div>
        <h3 class="text-xl font-bold">Time Per Issue</h3>
        <ul>
          <li v-for="(item, index) in report.time_per_issue" :key="index">
            <strong>{{ item.issue__title }}:</strong> {{ formatDuration(item.total_duration) }}
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <p>Loading report...</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    project: Object,
  },
  data() {
    return {
      report: null,
    };
  },
  created() {
    this.fetchReport();
  },
  methods: {
    async fetchReport() {
      try {
        const res = await fetch(`http://localhost:8000/api/reports/${this.project.id}/get_report/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.report = await res.json();
      } catch (error) {
        console.error('Error fetching project report:', error);
        alert('Could not load project report.');
      }
    },
    formatDuration(duration) {
      if (!duration) return '0 minutes';
      const totalSeconds = duration.days * 86400 + duration.seconds;
      const minutes = Math.floor(totalSeconds / 60);
      return `${minutes} minutes`;
    },
  },
};
</script>
