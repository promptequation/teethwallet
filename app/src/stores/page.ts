import { defineStore } from 'pinia';

export const usePageStore = defineStore('page', {
  state: () => ({
    loading: false,
  }),
  actions: {
    // toggle loading
    toggleLoading() {
      this.loading = !this.loading
    }
  },
});
