<template>
  <div>
    <!-- Trigger Button -->
    <button class="btn btn-primary" @click="open = true">+ New Invoice</button>

    <!-- Modal -->
    <div v-if="open" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-base-100 p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-lg font-bold mb-4">Create New Invoice</h2>

        <form @submit.prevent="createInvoice">
          <select v-model="clientId" class="select select-bordered w-full mb-3" required>
            <option disabled value="">Select a client</option>
            <option v-for="client in clients" :key="client.id" :value="client.id">{{ client.name }}</option>
          </select>
          <input v-model.number="amount" type="number" step="0.01" placeholder="Amount" class="input input-bordered w-full mb-3" required />
          <input v-model="due_date" type="date" class="input input-bordered w-full mb-3" required />

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
      clientId: '',
      amount: '',
      due_date: '',
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
    async createInvoice() {
      const res = await fetch('http://localhost:8000/api/invoices/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          client: this.clientId,
          amount: this.amount,
          due_date: this.due_date,
        })
      });

      if (res.ok) {
        this.clientId = '';
        this.amount = '';
        this.due_date = '';
        this.open = false;
        this.$emit('created'); // Notify parent to refresh invoice list
      } else {
        const error = await res.json();
        console.error(error);
        alert('Error creating invoice.');
      }
    }
  }
};
</script>
