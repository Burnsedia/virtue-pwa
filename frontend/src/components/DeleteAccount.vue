<template>
  <div class="card bg-base-100 shadow-xl p-6 mb-6">
    <h3 class="text-xl font-bold mb-4">Delete Account</h3>
    <p class="mb-4">Permanently delete your account. This action cannot be undone.</p>
    <button @click="handleDelete" class="btn btn-error">Delete Account</button>
  </div>
</template>

<script>
export default {
  methods: {
    async handleDelete() {
      if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        return;
      }

      try {
        const res = await fetch(`http://localhost:8000/auth/users/me/`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (res.ok) {
          alert('Account deleted successfully!');
          localStorage.removeItem('token');
          window.location.href = '/signin'; // Redirect to signin page
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Error deleting account:', error);
        alert('An error occurred while deleting account.');
      }
    },
  },
};
</script>
