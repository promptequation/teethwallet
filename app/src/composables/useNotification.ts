import { useNotificationStore } from 'src/stores/notification';

export function useNotification() {
  const notificationStore = useNotificationStore();

  const fetchNotifications = async (userId: number) => {
    try {
      const { notifications }: any = await notificationStore.fetchNotifications(
        userId
      );
      notificationStore.setNotifications(notifications);
    } catch (error: unknown) {
      console.log(error);
    }
  };

  const updateNotification = async (id: number, isRead: boolean) => {
    try {
      await notificationStore.updateNotification(id, isRead);
    } catch (error: unknown) {
      console.log(error);
    }
  };

  const pushNotification = async (
    name: string,
    user: string,
    registrationId: string,
    type: string,
    deviceId: string,
    active: boolean
  ) => {
    try {
      return notificationStore.pushNotification(
        name,
        user,
        registrationId,
        type,
        deviceId,
        active
      );
    } catch (error: unknown) {
      console.log(error);
    }
  };

  return {
    fetchNotifications,
    updateNotification,
    pushNotification,
  };
}
