
import { ref, useContext, useStore } from "@nuxtjs/composition-api";


const useNotification = () => {
    const { $config } = useContext()
    const { dispatch, commit } = useStore()

    const fetchNotifications = async ({ userId }) => {
        try {
            const {notifications} = await dispatch('notification/fetchNotifications', { userId })
            commit('notification/SET_NOTIFICATIONS', notifications)
        } catch (error) {
            console.log(error);
        }
    }

    const deleteNotification = async ( id ) => {
        try {
            return await dispatch("notification/deleteNotification", {
                id,
            });
        } catch (error) {
            console.log(error);
        }
    };

    const updateNotification = async ( id, isRead ) => {
        try {
            return await dispatch("notification/updateNotification", {
                id,
                isRead,
            });
        } catch (error) {
            console.log(error);
        }
    };

    const socket = ref()

    const joinNotificationRoom = (userId) => {
        if (process.browser) {
            socket.value = new WebSocket(`${$config.baseUrlWs}/ws/notification/${userId}/`)
        }
    }

    const receiveNotification = () => {
        if (socket.value) {
            socket.value.onmessage = (e) => {
                const data = JSON.parse(e.data);
                if (data) {
                    const notifications = data.data.notifications
                    commit('notification/PUSH_NOTIFICATIONS', notifications)
                }
            }
        }
    }

    const closeSocket = () => {
        if (socket.value) {
            socket.value.close()
        }
    }

    return {
        fetchNotifications,
        deleteNotification,
        updateNotification,
        joinNotificationRoom,
        receiveNotification,
        closeSocket,
    };
}


export default useNotification