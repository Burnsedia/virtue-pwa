<template>
  <div class="card bg-base-100 shadow-xl p-6 mb-6">
    <h3 class="text-xl font-bold mb-4">Change Email</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">New Email</span>
        </label>
        <input type="email" v-model="newEmail" class="input input-bordered" required>
      </div>
      <button type="submit" class="btn btn-primary">Update Email</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newEmail: '',
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const res = await fetch(`http://localhost:8000/auth/users/me/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ email: this.newEmail }),
        });

        if (res.ok) {
          alert('Email updated successfully!');
          this.newEmail = '';
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Error updating email:', error);
        alert('An error occurred while updating email.');
      }
    },
  },
};
</script>
