<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">{{ isLogin ? 'Sign In' : 'Sign Up' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Email</span>
        </label>
        <input type="email" v-model="email" class="input input-bordered" required>
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Password</span>
        </label>
        <input type="password" v-model="password" class="input input-bordered" required>
      </div>
      <div v-if="!isLogin" class="form-control mb-4">
        <label class="label">
          <span class="label-text">Confirm Password</span>
        </label>
        <input type="password" v-model="confirmPassword" class="input input-bordered" required>
      </div>
      <button type="submit" class="btn btn-primary w-full">{{ isLogin ? 'Sign In' : 'Sign Up' }}</button>
    </form>
    <div class="mt-4 text-center">
      <p v-if="isLogin">
        Don't have an account? <a href="/signup" class="link link-primary">Sign Up</a>
        <br>
        <a href="/forgot-password" class="link link-primary">Forgot Password?</a>
      </p>
      <p v-else>
        Already have an account? <a href="/signin" class="link link-primary">Sign In</a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isLogin: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.isLogin && this.password !== this.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }

      const endpoint = this.isLogin ? 'token/login/' : 'users/';
      const body = this.isLogin
        ? { email: this.email, password: this.password }
        : { email: this.email, password: this.password };

      try {
        const res = await fetch(`http://localhost:8000/auth/${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });

        if (res.ok) {
          const data = await res.json();
          if (this.isLogin) {
            localStorage.setItem('token', data.auth_token);
            alert('Login successful!');
            window.location.href = '/'; // Redirect to home page
          } else {
            alert('Registration successful! Please sign in.');
            window.location.href = '/signin'; // Redirect to signin page
          }
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Authentication error:', error);
        alert('An error occurred during authentication.');
      }
    },
  },
};
</script>
