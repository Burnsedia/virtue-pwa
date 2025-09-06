<template>
  <div class="card bg-base-100 shadow-xl p-6 mb-6">
    <h3 class="text-xl font-bold mb-4">Change Password</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Current Password</span>
        </label>
        <input type="password" v-model="currentPassword" class="input input-bordered" required>
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">New Password</span>
        </label>
        <input type="password" v-model="newPassword" class="input input-bordered" required>
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Confirm New Password</span>
        </label>
        <input type="password" v-model="confirmNewPassword" class="input input-bordered" required>
      </div>
      <button type="submit" class="btn btn-primary">Update Password</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      confirmNewPassword: '',
    };
  },
  methods: {
    async handleSubmit() {
      if (this.newPassword !== this.confirmNewPassword) {
        alert('New passwords do not match!');
        return;
      }

      try {
        const res = await fetch(`http://localhost:8000/auth/users/set_password/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            current_password: this.currentPassword,
            new_password: this.newPassword,
          }),
        });

        if (res.ok) {
          alert('Password updated successfully!');
          this.currentPassword = '';
          this.newPassword = '';
          this.confirmNewPassword = '';
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Error updating password:', error);
        alert('An error occurred while updating password.');
      }
    },
  },
};
</script>
