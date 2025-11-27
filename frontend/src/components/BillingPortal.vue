<template>
  <div class="card bg-base-100 shadow-xl p-6 mb-6">
    <h3 class="text-xl font-bold mb-4">Manage Your Subscription</h3>
    <p class="mb-4">Access your Stripe Customer Portal to update payment methods, view billing history, and manage your subscription.</p>
    <button @click="accessCustomerPortal" class="btn btn-primary">Access Customer Portal</button>
  </div>
</template>

<script>
export default {
  methods: {
    async accessCustomerPortal() {
      try {
        // You'll need to fetch the customer_id for the current user.
        // This typically comes from your backend, associated with the user's account.
        // For now, we'll use a placeholder. In a real app, you'd fetch this from your user's profile API.
        const customerId = 'cus_P0RtalExAmPlE'; // Replace with actual customer ID

        const res = await fetch('http://localhost:8000/api/checkout/create_customer_portal_session/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ customer_id: customerId }),
        });

        if (res.ok) {
          const data = await res.json();
          window.location.href = data.url; // Redirect to Stripe Customer Portal
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Error accessing customer portal:', error);
        alert('An error occurred while trying to access the customer portal.');
      }
    },
  },
};
</script>
