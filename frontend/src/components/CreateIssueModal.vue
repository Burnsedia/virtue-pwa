<template>
  <div>
    <!-- Trigger Button -->
    <button class="btn btn-sm btn-outline w-full" @click="open = true">
      + Add Task
    </button>

    <!-- Modal -->
    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">New Task</h2>

        <form @submit.prevent="createIssue">
          <input v-model="title" type="text" placeholder="Task title" class="input input-bordered w-full mb-3"
            required />
          <textarea v-model="description" placeholder="Description" class="textarea textarea-bordered w-full mb-3" />
          <input v-model.number="estimate_minutes" type="number" placeholder="Estimate (minutes)"
            class="input input-bordered w-full mb-3" min="0" />

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
  props: {
    projectId: {
      type: Number,
      required: true
    },
    priority: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      open: false,
      title: '',
      description: '',
      estimate_minutes: 0
    };
  },
  methods: {
    async createIssue() {
      const res = await fetch('http://localhost:8000/api/issues/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: this.title,
          description: this.description,
          estimate_minutes: this.estimate_minutes,
          priority: this.priority,
          project: this.projectId
        })
      });

      if (res.ok) {
        this.open = false;
        this.title = '';
        this.description = '';
        this.estimate_minutes = 0;
        this.$emit('created'); // Notify parent to refresh
      } else {
        const err = await res.json();
        console.error(err);
        alert('Failed to create task.');
      }
    }
  }
};
</script>
