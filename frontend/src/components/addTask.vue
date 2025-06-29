<template>
  <div>
    <!-- Add Task Button -->
    <button class="btn btn-primary" @click="open = true">
      + Add Task
    </button>

    <!-- Modal -->
    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">Create New Task</h2>

        <form @submit.prevent="submit">
          <input v-model="form.title" type="text" placeholder="Title" class="input input-bordered w-full mb-3"
            required />

          <textarea v-model="form.description" placeholder="Description"
            class="textarea textarea-bordered w-full mb-3" />

          <input v-model.number="form.estimate_minutes" type="number" placeholder="Estimate (minutes)"
            class="input input-bordered w-full mb-3" min="0" />

          <label class="block mb-1 font-bold">Priority</label>
          <select v-model.number="form.priority" class="select select-bordered w-full mb-3">
            <option :value="1">🔥 Urgent & Important</option>
            <option :value="2">⚠️ Urgent & Not Important</option>
            <option :value="3">🌱 Not Urgent & Important</option>
            <option :value="4">🧘 Not Urgent & Not Important</option>
          </select>

          <label class="block mb-1 font-bold">Status</label>
          <select v-model="form.status" class="select select-bordered w-full mb-3">
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>

          <div class="flex justify-end gap-2">
            <button class="btn" type="button" @click="open = false">Cancel</button>
            <button class="btn btn-primary" type="submit">Create</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['created']);

const open = ref(false);

const form = ref({
  title: '',
  description: '',
  estimate_minutes: 0,
  priority: 3,
  status: 'todo'
});

async function submit() {
  const response = await fetch('http://localhost:8000/api/issues/', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      ...form.value,
      project: props.projectId
    })
  });

  if (response.ok) {
    open.value = false;
    emit('created'); // let parent know to refresh
    form.value = {
      title: '',
      description: '',
      estimate_minutes: 0,
      priority: 3,
      status: 'todo'
    };
  } else {
    const err = await response.json();
    console.error(err);
    alert('Error creating task');
  }
}
</script>
