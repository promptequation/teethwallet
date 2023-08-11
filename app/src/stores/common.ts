import { defineStore } from 'pinia';

export const useCommonStore = defineStore('common', {
  state: () => ({
    approvalStatuses: [],
  }),
  getters: {
    getApprovalStatuses(state) {
      return state.approvalStatuses;
    },
  },
  actions: {
    setApprovalStatus(approvalStatuses: any) {
      this.approvalStatuses = approvalStatuses;
    },
  },
});
