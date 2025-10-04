<template>
  <div class="max-w-5xl mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-3xl font-bold">Clients</h1>
      <CreateClientModal @created="fetchClients" />
    </div>

    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>Name</th>
            <th>Contact Person</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="client in clients" :key="client.id">
            <td>{{ client.name }}</td>
            <td>{{ client.contact_person }}</td>
            <td>{{ client.email }}</td>
            <td>{{ client.phone_number }}</td>
            <td>
              <button @click="deleteClient(client.id)" class="btn btn-error btn-sm">
                🗑 Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import CreateClientModal from './CreateClientModal.vue';

export default {
  components: { CreateClientModal },
  data() {
    return {
      clients: [],
    };
  },
  created() {},
  mounted() {
    this.fetchClients();
  },
  methods: {
    async fetchClients() {
      const res = await fetch('http://localhost:8000/api/clients/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.clients = await res.json();
    },
    async deleteClient(clientId) {
      if (!confirm('Are you sure you want to delete this client?')) return;

      const res = await fetch(`http://localhost:8000/api/clients/${clientId}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (res.ok) {
        alert('Client deleted.');
        this.fetchClients();
      } else {
        alert('Error deleting client.');
      }
    },
  },
};
</script>
