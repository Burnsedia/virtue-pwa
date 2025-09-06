<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Sign Up</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Email</span>
        </label>
        <input type="email" v-model="email" class="input input-bordered" required>
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Username</span>
        </label>
        <input type="text" v-model="username" class="input input-bordered">
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Password</span>
        </label>
        <input type="password" v-model="password" class="input input-bordered" required>
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Confirm Password</span>
        </label>
        <input type="password" v-model="confirmPassword" class="input input-bordered" required>
      </div>
      <button type="submit" class="btn btn-primary w-full">Sign Up</button>
    </form>
    <div class="mt-4 text-center">
      <p>
        Already have an account? <a href="/signin" class="link link-primary">Sign In</a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    async handleSubmit() {
      if (this.password !== this.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }

      const endpoint = 'users/';
      const body = { email: this.email, username: this.username, password: this.password };

      try {
        const res = await fetch(`http://localhost:8000/auth/${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });

        if (res.ok) {
          alert('Registration successful! Please sign in.');
          window.location.href = '/signin'; // Redirect to signin page
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Registration error:', error);
        alert('An error occurred during registration.');
      }
    },
  },
};
</script>
