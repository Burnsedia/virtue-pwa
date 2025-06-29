<template>
  <form @submit.prevent="createProject" class="max-w-md p-4 bg-base-100 rounded shadow">
    <h2 class="text-lg font-bold mb-4">Create New Project</h2>

    <input v-model="name" type="text" placeholder="Project name" class="input input-bordered w-full mb-3" required />
    <textarea v-model="description" placeholder="Description" class="textarea textarea-bordered w-full mb-3" />

    <button class="btn btn-primary w-full" type="submit">Create</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
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
        alert('Project created!');
      } else {
        const data = await res.json();
        console.error(data);
        alert('Error creating project.');
      }
    }
  }
};
</script>
