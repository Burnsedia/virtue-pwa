<template>
  <div>
    <!-- Trigger Button -->
    <button class="btn btn-primary mb-4" @click="open = true" :disabled="!canCreateOrganization">
      + New Organization
    </button>

    <p v-if="!canCreateOrganization" class="text-warning text-sm mb-4">
      Free users are limited to one organization. Upgrade to create more.
      <a href="/pricing" class="link link-primary">View Plans</a>
    </p>

    <!-- Modal -->
    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">Create New Organization</h2>

        <form @submit.prevent="createOrganization">
          <input v-model="name" type="text" placeholder="Organization name" class="input input-bordered w-full mb-3"
            required />

          <div class="flex justify-end gap-2">
            <button type="button" class="btn" @click="open = false">Cancel</button>
            <button type="submit" class="btn btn-primary">Create</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import authStatus from "../mixins/authStatus";

export default {
  emits: ['created'],
  mixins: [authStatus],
  data() {
    return {
      open: false,
      name: '',
      userOrganizationsCount: 0,
    };
  },
  computed: {
    canCreateOrganization() {
      return this.isPremium || this.userOrganizationsCount < 1;
    },
  },
  created() {
    this.fetchUserOrganizationsCount();
  },
  methods: {
    async fetchUserOrganizationsCount() {
      if (!this.isLoggedIn) return;
      const res = await fetch('http://localhost:8000/api/organizations/?owner__email=' + localStorage.getItem('email'), {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      const organizations = await res.json();
      this.userOrganizationsCount = organizations.length;
    },
    async createOrganization() {
      if (!this.canCreateOrganization) {
        alert('Free users are limited to one organization. Please upgrade to create more.');
        return;
      }

      const res = await fetch('http://localhost:8000/api/organizations/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.name,
          owner: null, // Django will set this based on the authenticated user
        })
      });

      if (res.ok) {
        this.name = '';
        this.open = false;
        this.fetchUserOrganizationsCount(); // Refresh count after creation
        this.$emit('created'); // Notify parent to refresh organization list
      } else {
        const error = await res.json();
        console.error(error);
        alert('Error creating organization.');
      }
    }
  }
};
</script>
