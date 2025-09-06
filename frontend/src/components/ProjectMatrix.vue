<template>
  <div class="max-w-5xl mx-auto p-4">
    <div >
      <div class="flex justify-between">
        <CreateProjectModal @created="fetchProjects" />
        <AddTask
          v-if="selectedProjectId"
          :project-id="selectedProjectId"
          @created="refreshTasks"
        />
      </div>

      <div class="flex items-center justify-between mb-4">
        <select
          v-model="selectedProjectId"
          class="select select-bordered w-full"
        >
          <option disabled value="">-- Choose Project --</option>
          <option
            v-for="project in projects"
            :key="project.id"
            :value="project.id"
          >
            {{ project.name }}
          </option>
        </select>

        <button
          v-if="selectedProjectId"
          class="btn btn-error btn-sm ml-4"
          @click="deleteProject"
        >
          🗑 Delete
        </button>
      </div>

      <div
        v-if="selectedProjectId"
        class="grid grid-cols-1 sm:grid-cols-2 gap-6"
      >
        <div
          class="bg-base-200 border border-secondary h-96 p-2"
          @dragover.prevent
          @drop="onDrop($event, 1)"
        >
          <h2 class="text-lg font-bold text-center">🔥 Urgent & Important</h2>
          <IssueCard
            v-for="issue in getIssuesByPriority(1)"
            :key="issue.id"
            :issue="issue"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
          />
        </div>
        <div
          class="bg-base-200 border border-primary h-96 p-2"
          @dragover.prevent
          @drop="onDrop($event, 2)"
        >
          <h2 class="text-lg font-bold text-center">
            ⚠️ Urgent & Not Important
          </h2>
          <IssueCard
            v-for="issue in getIssuesByPriority(2)"
            :key="issue.id"
            :issue="issue"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
          />
        </div>
        <div
          class="bg-base-200 border border-success h-96 p-2"
          @dragover.prevent
          @drop="onDrop($event, 3)"
        >
          <h2 class="text-lg font-bold text-center">
            🌱 Not Urgent & Important
          </h2>
          <IssueCard
            v-for="issue in getIssuesByPriority(3)"
            :key="issue.id"
            :issue="issue"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
          />
        </div>
        <div
          class="bg-base-200 border border-alert h-96 p-2"
          @dragover.prevent
          @drop="onDrop($event, 4)"
        >
          <h2 class="text-lg font-bold text-center">
            🧘 Not Urgent & Not Important
          </h2>
          <IssueCard
            v-for="issue in getIssuesByPriority(4)"
            :key="issue.id"
            :issue="issue"
            draggable="true"
            @dragstart="onDragStart($event, issue)"
          />
        </div>
      </div>
    </div>
    <div  class="text-center p-8">
      <h2 class="text-2xl font-bold mb-4">Upgrade to Premium to access the Eisenhower Matrix</h2>
      <p class="mb-4">This feature is available to premium subscribers only.</p>
      <a href="/pricing" class="btn btn-primary">View Plans</a>
    </div>
  </div>
</template>

<script>
import AddTask from "./addTask.vue";
import CreateProjectModal from "./CreateProject.vue";
import IssueCard from "./IssueCard.vue";
import authStatus from "../mixins/authStatus";

export default {
  components: { CreateProjectModal, AddTask, IssueCard },
  mixins: [authStatus],
  data() {
    return {
      projects: [],
      selectedProjectId: "",
      issues: [],
    };
  },
  created() {},
  mounted() {
    if (this.isPremium) {
      this.fetchProjects();
      this.fetchIssues();
    }
  },
  watch: {
    selectedProjectId() {
      if (this.isPremium) {
        this.fetchIssues();
      }
    },
  },
  methods: {
    refreshTasks() {
      if (this.isPremium) {
        this.fetchIssues();
      }
    },
    async fetchProjects() {
      const res = await fetch("http://localhost:8000/api/projects/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      this.projects = await res.json();
    },
    async deleteProject() {
      if (!confirm("Are you sure you want to delete this project?")) return;

      const res = await fetch(
        `http://localhost:8000/api/projects/${this.selectedProjectId}/`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (res.ok) {
        alert("Project deleted.");
        this.selectedProjectId = "";
        this.fetchProjects();
      } else {
        alert("Error deleting project.");
      }
    },
    async fetchIssues() {
      if (!this.selectedProjectId) return;
      const res = await fetch(
        `http://localhost:8000/api/issues/?project=${this.selectedProjectId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      this.issues = await res.json();
    },
    getIssuesByPriority(priority) {
      return this.issues.filter((issue) => issue.priority === priority);
    },
    onDragStart(event, issue) {
      event.dataTransfer.setData("application/json", JSON.stringify(issue));
    },
    async onDrop(event, newPriority) {
      const issueData = JSON.parse(
        event.dataTransfer.getData("application/json")
      );
      const issue = this.issues.find((i) => i.id === issueData.id);
      if (issue) {
        issue.priority = newPriority;
        // Update the issue priority in the backend
        await fetch(`http://localhost:8000/api/issues/${issue.id}/`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({ priority: newPriority }),
        });
      }
    },
  },
};
</script>
