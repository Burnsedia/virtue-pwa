export default {
  computed: {
    userStatus() {
      if (typeof window !== 'undefined') {
        const status = localStorage.getItem('userStatus');
        return status ? JSON.parse(status) : { isLoggedIn: false, isPremium: false, userId: null };
      }
      return { isLoggedIn: false, isPremium: false };
    },
    isLoggedIn() {
      return this.userStatus.isLoggedIn;
    },
    isPremium() {
      return this.userStatus.isPremium;
    },
  },
};
