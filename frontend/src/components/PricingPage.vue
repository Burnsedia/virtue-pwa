<template>
  <div class="max-w-4xl mx-auto p-4">
    <h1 class="text-3xl font-bold text-center mb-8">Choose Your Plan</h1>

    <div v-if="isLoggedIn">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div v-for="product in products" :key="product.id" class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">{{ product.name }}</h2>
            <p>{{ product.description }}</p>
            <div class="mt-4">
              <div v-for="price in getPricesForProduct(product.id)" :key="price.id" class="mb-2">
                <span class="text-2xl font-bold">{{ formatPrice(price) }}</span> / {{ price.recurring.interval }}
                <button @click="subscribe(price.id)" class="btn btn-primary btn-sm ml-4">Subscribe</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center p-8">
      <h2 class="text-2xl font-bold mb-4">Please sign in to view pricing plans.</h2>
      <a href="/signin" class="btn btn-primary">Sign In</a>
    </div>
  </div>
</template>

<script>
import authStatus from "../mixins/authStatus";

export default {
  mixins: [authStatus],
  data() {
    return {
      products: [],
      prices: [],
    };
  },
  created() {},
  mounted() {
    if (this.isLoggedIn) {
      this.fetchProductsAndPrices();
    }
  },
  methods: {
    async fetchProductsAndPrices() {
      try {
        const productRes = await fetch('http://localhost:8000/api/products/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.products = await productRes.json();

        const priceRes = await fetch('http://localhost:8000/api/prices/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.prices = await priceRes.json();
      } catch (error) {
        console.error('Error fetching products and prices:', error);
        alert('Could not load pricing information.');
      }
    },
    getPricesForProduct(productId) {
      return this.prices.filter(price => price.product === productId);
    },
    formatPrice(price) {
      return `${(price.unit_amount / 100).toFixed(2)}`;
    },
    async subscribe(priceId) {
      try {
        const res = await fetch('http://localhost:8000/api/checkout/create_checkout_session/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ price_id: priceId }),
        });

        if (res.ok) {
          const data = await res.json();
          // Redirect to Stripe Checkout
          window.location.href = data.sessionId; // sessionId is actually the URL from Stripe
        } else {
          const errorData = await res.json();
          alert(`Error: ${JSON.stringify(errorData)}`);
        }
      } catch (error) {
        console.error('Error creating checkout session:', error);
        alert('An error occurred during subscription.');
      }
    },
  },
};
</script>
