<template>
  <div class="max-w-3xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6">Settings</h1>

    <div class="flex flex-col md:flex-row gap-6">
      <aside class="md:w-1/4">
        <ul class="menu bg-base-200 rounded-box">
          <li><a :class="{ 'active': currentSection === 'account' }" @click="currentSection = 'account'">Account</a></li>
          <li><a :class="{ 'active': currentSection === 'preferences' }" @click="currentSection = 'preferences'">Preferences</a></li>
          <li><a :class="{ 'active': currentSection === 'subscription' }" @click="currentSection = 'subscription'">Subscription</a></li>
        </ul>
      </aside>

      <section class="md:w-3/4 bg-base-200 p-6 rounded-box">
        <div v-if="currentSection === 'account'">
          <h2 class="text-2xl font-bold mb-4">Account Management</h2>
          <ChangeEmail />
          <ChangePassword />
          <DeleteAccount />
        </div>

        <div v-if="currentSection === 'preferences'">
          <h2 class="text-2xl font-bold mb-4">Application Preferences</h2>
          <ApplicationPreferences />
        </div>

        <div v-if="currentSection === 'subscription'">
          <h2 class="text-2xl font-bold mb-4">Subscription & Billing</h2>
          <!-- Subscription & Billing Components will go here -->
          <p>Manage your subscription plan and billing information.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import ChangeEmail from './ChangeEmail.vue';
import ChangePassword from './ChangePassword.vue';
import DeleteAccount from './DeleteAccount.vue';
import ApplicationPreferences from './ApplicationPreferences.vue';

export default {
  components: { ChangeEmail, ChangePassword, DeleteAccount, ApplicationPreferences },
  data() {
    return {
      currentSection: 'account',
    };
  },
};
</script>
