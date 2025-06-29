<template>
  <div>
    <button class="btn btn-sm btn-outline" @click="open = true">✏️</button>

    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">Edit Task</h2>

        <form @submit.prevent="editIssue">
          <input v-model="form.title" type="text" placeholder="Title" class="input input-bordered w-full mb-3" />
          <textarea v-model="form.description" placeholder="Description"
            class="textarea textarea-bordered w-full mb-3" />
          <select v-model.number="form.priority" class="select select-bordered w-full mb-3">
            <option :value="1">🔥 Urgent & Important</option>
            <option :value="2">⚠️ Urgent & Not Important</option>
            <option :value="3">🌱 Not Urgent & Important</option>
            <option :value="4">🧘 Not Urgent & Not Important</option>
          </select>
          <select v-model="form.status" class="select select-bordered w-full mb-3">
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>

          <div class="flex justify-end gap-2">
            <button type="button" class="btn" @click="open = false">Cancel</button>
            <button type="submit" class="btn btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    issue: Object
  },
  emits: ['updated'],
  data() {
    return {
      open: false,
      form: {
        title: '',
        description: '',
        priority: 3,
        status: 'todo'
      }
    };
  },
  watch: {
    open(newVal) {
      if (newVal) {
        this.form = { ...this.issue };
      }
    }
  },
  methods: {
    async editIssue() {
      const res = await fetch(`http://localhost:8000/api/issues/${this.issue.id}/`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.form)
      });

      if (res.ok) {
        this.open = false;
        this.$emit('updated');
      } else {
        const err = await res.json();
        console.error(err);
        alert('Failed to update task.');
      }
    }
  }
};
</script>
