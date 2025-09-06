<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Forgot Password</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Email</span>
        </label>
        <input type="email" v-model="email" class="input input-bordered" required>
      </div>
      <button type="submit" class="btn btn-primary w-full">Reset Password</button>
    </form>
    <div class="mt-4 text-center">
      <a href="/signin" class="link link-primary">Back to Sign In</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const res = await fetch(`http://localhost:8000/auth/users/reset_password/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email: this.email }),
        });

        if (res.ok) {
          alert('If an account with that email exists, you will receive a password reset email.');
          this.email = '';
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Password reset error:', error);
        alert('An error occurred during password reset.');
      }
    },
  },
};
</script>
