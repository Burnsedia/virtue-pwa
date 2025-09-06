<template>
  <div class="max-w-md mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Sign In</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Username</span>
        </label>
        <input type="text" v-model="username" class="input input-bordered" required>
      </div>
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text">Password</span>
        </label>
        <input type="password" v-model="password" class="input input-bordered" required>
      </div>
      <button type="submit" class="btn btn-primary w-full">Sign In</button>
    </form>
    <div class="mt-4 text-center">
      <p>
        Don't have an account? <a href="/signup" class="link link-primary">Sign Up</a>
        <br>
        <a href="/forgot-password" class="link link-primary">Forgot Password?</a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async handleSubmit() {
      const endpoint = 'jwt/create/';
      const body = { username: this.username, password: this.password };

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
          localStorage.setItem('token', data.access);
          console.log('Token set in localStorage:', data.access);

          // Fetch user details to get user ID
          const userDetailsRes = await fetch('http://localhost:8000/auth/users/me/', {
            headers: {
              Authorization: `Bearer ${data.access}`,
            },
          });
          const userDetailsData = await userDetailsRes.json();
          const userId = userDetailsData.id;

          // Fetch and store user's premium status
          const userStatusRes = await fetch('http://localhost:8000/api/users/me/subscription_status/', {
            headers: {
              Authorization: `Bearer ${data.access}`,
            },
          });
          const userStatusData = await userStatusRes.json();
          localStorage.setItem('userStatus', JSON.stringify({
            isLoggedIn: true,
            isPremium: userStatusData.is_premium,
            userId: userId, // Store user ID
          }));
          console.log('User status set in localStorage:', localStorage.getItem('userStatus'));

          alert('Login successful!');
          window.location.assign('/'); // Redirect to home page
        } else {
          const errorData = await res.json();
          console.error('Login error:', errorData);
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
