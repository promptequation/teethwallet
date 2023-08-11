import { computed, useContext, useStore, ref } from '@nuxtjs/composition-api'

const useChat = () => {
  const { dispatch, commit } = useStore()
  const { $config } = useContext()

  const socket = ref()

  const checkConnection = async (sender, receiver) => {
    try {
      const { checkConnection } = await dispatch('chat/checkConnection', { sender, receiver })

      return checkConnection
    } catch (error) {
      console.log(error);
      return null
    }
  }

  const createConnection = async (sender, receiver) => {
    try {
      const { createConnection } = await dispatch('chat/createConnection', { sender, receiver })

      return createConnection
    } catch (error) {
      console.log(error);
      return { connection: null }
    }
  }

  const createConversation = async (connection, sender, receiver, message) => {
    try {
      const { createConversation } = await dispatch('chat/createConversation', { connection, sender, receiver, message })
      const { conversation } = createConversation;
      commit('chat/PUSH_CONVERSATION', conversation);
    } catch (error) {
      console.log(error);
    }
  }

  const updateConversation = async (id, { ...arg }) => {
    try {
      const { updateConversation } = await dispatch('chat/updateConversation', { id, ...arg })
      const { conversation } = updateConversation;
      commit('chat/UPDATE_CONVERSATION', conversation);
    } catch (error) {
      console.log(error);
    }
  }

  const fetchConversations = async (connection) => {
    commit('chat/SET_LOADING', true)
    try {
      const { conversations } = await dispatch('chat/fetchConversations', { connectionId: connection })
      commit('chat/SET_CONVERSATIONS', conversations)
    } catch (error) {
      console.log(error);
    } finally {
      commit('chat/SET_LOADING', false)
    }
  }

  const fetchConnectedUser = async ({ authUserId }) => {
    commit('chat/SET_LOADING', true)
    try {
      const { connections } = await dispatch('chat/fetchConnectedUser', { userId: authUserId })
      commit('chat/SET_CONNECTED_USERS', { connections, authUserId })
    } catch (error) {
      console.log(error);
    } finally {
      commit('chat/SET_LOADING', false)
    }
  }

  const joinChatRoom = (connection) => {
    if (process.browser) {
      socket.value = new WebSocket(`${$config.baseUrlWs}/ws/chat/${connection}/`)
    }
  }

  const sendMessage = (message) => {
    if (socket.value) {
      socket.value.send(JSON.stringify(message))
    }
  }

  const receiveMessage = () => {
    if (socket.value) {
      socket.value.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data) {
          const { conversation } = data
          commit('chat/PUSH_SOCKET_CONVERSATION', conversation)
        }
      }
    }
  }

  const sendMessageWhenOpen = (message) => {
    if (socket.value) {
      socket.value.onopen = (e) => {
        socket.value.send(JSON.stringify(message))
      }
    }
  }

  const closeSocket = () => {
    if (socket.value) {
      socket.value.close()
    }
  }

  const scrollToBottom = (el) => {
    const ps = el.ps;
    if (ps) {
      if (el.$el instanceof HTMLElement) {
        el.$el.scrollTop = el.$el.scrollHeight;
        ps.update();
      }
    }
  }

  return {
    createConversation,
    updateConversation,
    fetchConversations,
    checkConnection,
    createConnection,
    scrollToBottom,
    socket,
    joinChatRoom,
    sendMessage,
    receiveMessage,
    sendMessageWhenOpen,
    closeSocket,
    fetchConnectedUser,
  }
}

export default useChat
