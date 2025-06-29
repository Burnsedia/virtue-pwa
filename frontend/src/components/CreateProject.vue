<template>
  <div>
    <!-- Trigger Button -->
    <button class="btn btn-primary mb-4" @click="open = true">
      + New Project
    </button>

    <!-- Modal -->
    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">Create New Project</h2>

        <form @submit.prevent="createProject">
          <input v-model="name" type="text" placeholder="Project name" class="input input-bordered w-full mb-3"
            required />
          <textarea v-model="description" placeholder="Description" class="textarea textarea-bordered w-full mb-3" />

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
export default {
  emits: ['created'],
  data() {
    return {
      open: false,
      name: '',
      description: ''
    };
  },
  methods: {
    async createProject() {
      const res = await fetch('http://localhost:8000/api/projects/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.name,
          description: this.description,
          org_owner: null
        })
      });

      if (res.ok) {
        this.name = '';
        this.description = '';
        this.open = false;
        this.$emit('created'); // Notify parent to refresh project list
      } else {
        const error = await res.json();
        console.error(error);
        alert('Error creating project.');
      }
    }
  }
};
</script>
