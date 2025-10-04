<template>
  <div>
    <!-- Trigger Button -->
    <button class="btn btn-primary" @click="open = true">+ New Client</button>

    <!-- Modal -->
    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">Create New Client</h2>

        <form @submit.prevent="createClient">
          <input v-model="name" type="text" placeholder="Client name" class="input input-bordered w-full mb-3" required />
          <input v-model="contact_person" type="text" placeholder="Contact person" class="input input-bordered w-full mb-3" />
          <input v-model="email" type="email" placeholder="Email" class="input input-bordered w-full mb-3" />
          <input v-model="phone_number" type="text" placeholder="Phone number" class="input input-bordered w-full mb-3" />
          <textarea v-model="notes" placeholder="Notes" class="textarea textarea-bordered w-full mb-3" />

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
      contact_person: '',
      email: '',
      phone_number: '',
      notes: '',
    };
  },
  methods: {
    async createClient() {
      const res = await fetch('http://localhost:8000/api/clients/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.name,
          contact_person: this.contact_person,
          email: this.email,
          phone_number: this.phone_number,
          notes: this.notes,
        })
      });

      if (res.ok) {
        this.name = '';
        this.contact_person = '';
        this.email = '';
        this.phone_number = '';
        this.notes = '';
        this.open = false;
        this.$emit('created'); // Notify parent to refresh client list
      } else {
        const error = await res.json();
        console.error(error);
        alert('Error creating client.');
      }
    }
  }
};
</script>
