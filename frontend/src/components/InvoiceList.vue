<template>
  <div class="max-w-5xl mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-3xl font-bold">Invoices</h1>
      <CreateInvoiceModal @created="fetchInvoices" />
    </div>

    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>Client</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Due Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="invoice in invoices" :key="invoice.id">
            <td>{{ getClientName(invoice.client) }}</td>
            <td>{{ invoice.amount }}</td>
            <td>{{ invoice.status }}</td>
            <td>{{ invoice.due_date }}</td>
            <td>
              <button @click="deleteInvoice(invoice.id)" class="btn btn-error btn-sm">
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
import CreateInvoiceModal from './CreateInvoiceModal.vue';

export default {
  components: { CreateInvoiceModal },
  data() {
    return {
      invoices: [],
      clients: [],
    };
  },
  created() {},
  mounted() {
    this.fetchInvoices();
    this.fetchClients();
  },
  methods: {
    async fetchInvoices() {
      const res = await fetch('http://localhost:8000/api/invoices/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.invoices = await res.json();
    },
    async fetchClients() {
      const res = await fetch('http://localhost:8000/api/clients/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      this.clients = await res.json();
    },
    getClientName(clientId) {
      const client = this.clients.find(c => c.id === clientId);
      return client ? client.name : 'Unknown';
    },
    async deleteInvoice(invoiceId) {
      if (!confirm('Are you sure you want to delete this invoice?')) return;

      const res = await fetch(`http://localhost:8000/api/invoices/${invoiceId}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (res.ok) {
        alert('Invoice deleted.');
        this.fetchInvoices();
      } else {
        alert('Error deleting invoice.');
      }
    },
  },
};
</script>
