<template>
  <div class="max-w-5xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6">Organizations</h1>

    <div v-if="isLoggedIn">
      <CreateOrganizationModal @created="fetchOrganizations" />

      <div v-for="org in organizations" :key="org.id" class="card bg-base-100 shadow-xl mb-6">
        <div class="card-body">
          <h2 class="card-title">{{ org.name }}</h2>
          <div v-if="org.projects && org.projects.length > 0">
            <h3 class="text-lg font-bold mt-4">Projects:</h3>
            <ul class="list-disc list-inside">
              <li v-for="project in org.projects" :key="project.id">
                {{ project.name }}
              </li>
            </ul>
          </div>
          <p v-else class="mt-4">No projects in this organization yet.</p>
        </div>
      </div>
    </div>
    <div v-else class="text-center p-8">
      <h2 class="text-2xl font-bold mb-4">Please sign in to view your organizations.</h2>
      <a href="/signin" class="btn btn-primary">Sign In</a>
    </div>
  </div>
</template>

<script>
import CreateOrganizationModal from './CreateOrganizationModal.vue';
import authStatus from "../mixins/authStatus";

export default {
  components: { CreateOrganizationModal },
  mixins: [authStatus],
  data() {
    return {
      organizations: [],
    };
  },
  created() {},
  mounted() {
    if (this.isLoggedIn) {
      this.fetchOrganizations();
    }
  },
  methods: {
    async fetchOrganizations() {
      try {
        const res = await fetch('http://localhost:8000/api/organizations/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const organizations = await res.json();
        // For each organization, fetch its projects
        for (const org of organizations) {
          const projectRes = await fetch(`http://localhost:8000/api/projects/?org_owner=${org.id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          org.projects = await projectRes.json();
        }
        this.organizations = organizations;
      } catch (error) {
        console.error('Error fetching organizations:', error);
      }
    },
  },
};
</script>
