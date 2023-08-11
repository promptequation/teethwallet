import { defineStore } from 'pinia';
import { gql } from 'graphql-request';
import { graphQLClient } from 'src/boot/graphql';
import { Notifications } from 'src/types/notifications';

interface State {
  notifications: Notifications[] | null;
}

export const useNotificationStore = defineStore('notification', {
  state: (): State => ({
    notifications: [],
  }),
  getters: {
    getNotifications: (state) => state.notifications,
  },
  actions: {
    setNotifications(notifications: Notifications[]) {
      this.notifications = notifications;
    },

    async fetchNotifications(userId: number) {
      const query = gql`
        query ($userId: Int) {
          notifications(userId: $userId) {
            id
            isRead
            createdBy {
              name
            }
            createdFor {
              name
            }
            company {
              name
            }
            notificationType
            createdAt
          }
        }
      `;
      const variables = { userId };

      return await graphQLClient.request(query, variables);
    },

    async updateNotification(id: number, isRead: boolean) {
      const mutation = gql`
        mutation ($id: ID, $isRead: Boolean) {
          updateNotification(input: { id: $id, isRead: $isRead }) {
            notification {
              isRead
            }
          }
        }
      `;
      const variables = { id, isRead };

      return await graphQLClient.request(mutation, variables);
    },

    async pushNotification(
      name: string,
      user: string,
      registrationId: string,
      type: string,
      deviceId: string,
      active: boolean
    ) {
      const mutation = gql`
        mutation (
          $name: String!
          $user: ID!
          $registrationId: String!
          $type: String!
          $deviceId: String!
          $active: Boolean
        ) {
          createFcmDevice(
            input: {
              name: $name
              user: $user
              registrationId: $registrationId
              type: $type
              deviceId: $deviceId
              active: $active
            }
          ) {
            fcmDevice {
              id
              name
              registrationId
              type
              deviceId
              active
            }
          }
        }
      `;
      const variables = { name, user, registrationId, type, deviceId, active };

      return await graphQLClient.request(mutation, variables);
    },
  },
});
