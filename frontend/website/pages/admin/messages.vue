<template>
  <div id="chat" class="chat-app common-left-right">
    <v-row>
      <v-col cols="12" sm="12">
        <v-card class="d-flex flex-row" :loading="loading">
          <div>
            <v-navigation-drawer v-model="drawer" left class="flex-shrink-0">
              <div class="px-3 border-bottom">
                <v-text-field
                  :placeholder="$t('messages.Search contact')"
                  class="mb-0 mt-0"
                  v-model="searchUser"
                >
                </v-text-field>
              </div>
              <base-scrollbar class="tw-relative">
                <v-list nav class="heightAuto">
                  <v-list-item
                    v-for="(user, i) in searchResult"
                    :key="i"
                    @click="checkChatConnection(user)"
                    :class="
                      selectedUser && selectedUser.id === user.id
                        ? 'active'
                        : 's'
                    "
                  >
                    <v-avatar size="42" class="mr-3 primary">
                      <img v-if="user.avatar" :src="user.avatar" />
                      <span v-else class="white--text text-h5">
                        {{ avatar(user.name) }}
                      </span>
                    </v-avatar>
                    <v-list-item-content>
                      <v-list-item-title>
                        <h4>{{ user.name }}</h4>
                        <span class="caption">{{
                          user.lastConversation
                            ? user.lastConversation.message
                            : ""
                        }}</span>
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </base-scrollbar>
            </v-navigation-drawer>
          </div>
          <div class="chat-right-part">
            <!---conversation header-->
            <div class="chat-topbar d-flex px-3 py-3 align-center">
              <div>
                <v-app-bar-nav-icon
                  @click.stop="drawer = !drawer"
                  class="d-block d-lg-none mr-2 tw-z-0"
                >
                </v-app-bar-nav-icon>
              </div>
              <template v-if="selectedUser">
                <v-avatar size="42" class="mr-3 primary">
                  <img
                    v-if="selectedUser.avatar"
                    :src="selectedUser.avatar"
                    width="37"
                  />
                  <span v-else class="white--text text-h5">
                    {{ avatar(selectedUser.name) }}
                  </span>
                </v-avatar>
                <div class="user-about">
                  <h6>{{ selectedUser.name }}</h6>
                </div>
              </template>
              <template v-else>
                <div class="tw-h-[42px]"></div>
              </template>
            </div>
            <!---conversation header-->
            <base-scrollbar ref="el" class="tw-relative">
              <v-list class="heightAuto">
                <template v-for="(items, key) in conversations">
                  <div :key="key" class="chat-date-divider">
                    <v-subheader class="chat-date">
                      {{ date(key) }}
                    </v-subheader>

                    <v-divider inset> </v-divider>
                  </div>
                  <v-hover
                    v-slot="{ hover }"
                    :disabled="disableHover"
                    v-for="(item, index) in items"
                    :key="`${index}-${key}`"
                  >
                    <v-list-item :color="hover ? 'grey lighten-1' : ''">
                      <v-list-item-avatar
                        v-if="item.sender"
                        color="primary"
                        class="justify-center"
                      >
                        <v-img
                          v-if="item.sender.avatar"
                          :src="item.sender.avatar"
                        >
                        </v-img>
                        <span v-else class="white--text text-h5">
                          {{
                            avatar(
                              item.sender.firstName || item.sender.username
                            )
                          }}
                        </span>
                      </v-list-item-avatar>

                      <v-list-item-content>
                        <v-list-item-title v-if="item.sender">
                          {{ item.sender.firstName || item.sender.username }}
                          <span class="tw-text-xs tw-font-normal">
                            {{ datetime(item.datetime) }}
                          </span>
                          <v-icon v-if="item.isEdited" x-small right>
                            mdi-pencil
                          </v-icon>
                        </v-list-item-title>
                        <v-chip
                          class="mxw-ftc"
                          :color="item.isAutoMessage ? 'red' : ''"
                          :text-color="item.isAutoMessage ? 'white' : ''"
                          v-html="item.message"
                        >
                        </v-chip>
                      </v-list-item-content>
                      <v-list-item-action v-if="!item.isAutoMessage">
                        <v-menu
                          v-if="hover && item.sender.id === authUser.id"
                          transition="slide-x-transition"
                          :left="item.sender.id !== authUser.id"
                          :right="item.sender.id === authUser.id"
                          :max-width="170"
                          :allow-overflow="true"
                          :close-on-click="true"
                          :close-on-content-click="true"
                          :z-index="1000"
                          offset-y
                          @input="disableHover = $event"
                        >
                          <template #activator="{ on, attrs }">
                            <v-btn x-small icon v-bind="attrs" v-on="on">
                              <v-icon>mdi-dots-vertical</v-icon>
                            </v-btn>
                          </template>

                          <v-list class="pa-0" dense>
                            <v-list-item
                              v-if="item.sender.id === authUser.id"
                              ripple
                              @click="editConversation(index, item)"
                            >
                              <v-list-item-action class="mr-3">
                                <v-icon size="20"> mdi-pencil-outline </v-icon>
                              </v-list-item-action>
                              <v-list-item-content>
                                <v-list-item-title class="font-14">
                                  Edit
                                </v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list>
                        </v-menu>
                        <!-- <v-icon
                        :color="
                          item.isSeen ? 'green lighten1' : 'grey lighten-1'
                        "
                      >
                        mdi-check
                      </v-icon> -->
                      </v-list-item-action>
                    </v-list-item>
                  </v-hover>
                </template>
              </v-list>
            </base-scrollbar>

            <div class="pa-3 border-top">
              <v-textarea
                ref="messageBox"
                v-model.trim="message"
                name="input-4-1"
                rows="2"
                :placeholder="$t('messages.Type and hit Enter')"
                @focus="markAsSeen"
                @keydown.enter="sendMessage('')"
              >
              </v-textarea>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import {
  ref,
  defineComponent,
  useStore,
  computed,
  useContext,
  onBeforeUnmount,
  useRoute,
  onMounted,
  watch,
  useRouter,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useUser from "~/../composables/useUser";
import useChat from "~/../composables/useChat";
import { Patient } from "~/../../types/user";
import useMyInvitations from "~/../composables/useMyInvitations";
import useJoinClinic from "~/../composables/useJoinClinic";

export default defineComponent({
  name: "AdminMessage",
  layout: "admin",

  setup() {
    const { $t } = useNuxtTranslator()
    const route = useRoute()
    const router = useRouter()
    const { getters, commit } = useStore();
    const { $dayjs, app } = useContext();
    const { $toast } = app;
    const el = ref<HTMLElement | null>(null);
    const {
      fetchConversations,
      checkConnection,
      createConnection,
      scrollToBottom,
      joinChatRoom,
      sendMessage: sendChatMessage,
      sendMessageWhenOpen,
      receiveMessage,
      closeSocket,
      fetchConnectedUser,
    } = useChat();
    const { fetchDoctors, isDoctor } = useUser();
    const { fetchPatienstByDoctor, fetchDoctorsByPatient } = useMyInvitations()
    const { fetchActiveCompanyForUser } = useJoinClinic();
    fetchDoctors();

    const authUser = computed(() => getters["auth/getUserProfile"]);
    const approvedStatus = computed(() => getters['common/getApprovedStatus'])
    const loading = computed(() => getters["chat/loading"]);
    const conversations = computed(() => getters["chat/conversations"]);
    const getConnectedUsers = computed(() => getters["chat/getConnectedUsers"]);


    commit("chat/SET_AUTH_USER", {
      id: authUser.value?.id,
      name: authUser.value?.name,
      username: authUser.value?.username,
      avatar: authUser.value?.avatar,
    });

    const connectionId = ref();
    const selectedUser = ref();
    const disableHover = ref(false);
    const message = ref("");
    const searchUser = ref("");
    const messageBox = ref<HTMLElement | null>(null);
    const isEditing = ref(false);
    const editableItem = ref();
    const searchResult = ref<any[]>();
    const drawer = ref(true);
    const activeCompany = ref<any>()


    const checkChatConnection = async (user: any) => {
      selectedUser.value = user;
      commit("chat/SET_USER", user);
      const sender = parseInt(authUser.value?.id);
      const receiver = parseInt(user.id);
      const connectionData = await checkConnection(sender, receiver);
      connectionId.value = connectionData?.id;
      if (!connectionId.value) {
        const { connection } = await createConnection(sender, receiver);
        connectionId.value = connection?.id;
        await fetchConversations(parseInt(connectionId.value));
        joinChatRoom(connectionId.value);
        receiveMessage()
      } else {
        await fetchConversations(parseInt(connectionId.value));
        joinChatRoom(connectionId.value);
        receiveMessage()
      }
      scrollToBottom(el.value);
    };

    const setDefaultMessage = (appointmentDetails: any, startDate: any) => {
      let tooth: any = ''
      let diagnosis: any = ''
      let treatment: any = ''
      appointmentDetails.forEach((detail: any) => {
        if (detail && detail.node && detail.node.tooth) {
          tooth += tooth ? ', ' + detail.node.tooth.number : detail.node.tooth.number
        }

        if (detail && detail.node && detail.node.diagnosis) {
          diagnosis += diagnosis ? ', ' + detail.node?.diagnosis?.diagnosticlangSet?.edges[0]?.node?.name : detail.node?.diagnosis?.diagnosticlangSet?.edges[0]?.node?.name
        }

        if (detail && detail.node && detail.node.treatment) {
          treatment += treatment ? ', ' + detail.node?.treatment?.treatmentlangSet?.edges[0]?.node?.name : detail.node?.treatment?.treatmentlangSet?.edges[0]?.node?.name
        }

      })
      const defaultMessage = `${startDate} Tooth: ${tooth}; Diagnostic: ${diagnosis}; Treatment: ${treatment}`
      return defaultMessage
    }


    const getActiveCompany = async () => {
      const { userCompany } = await fetchActiveCompanyForUser({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isActive: true
      })

      if (userCompany && userCompany.edges && userCompany.edges.length > 0) {
        activeCompany.value = userCompany.edges[0].node.company
      }
    }

    watch(conversations, () => {
      scrollToBottom(el.value);
    })

    onMounted(async () => {
      let newMessage: string = ''
      let appointmentDetails: any = route.value.query && route.value.query.history
      let startDate: any = route.value.query && route.value.query.startDate
      if (appointmentDetails) {
        appointmentDetails = JSON.parse(appointmentDetails);
        if (appointmentDetails && appointmentDetails.length > 0 && startDate) {
          newMessage = setDefaultMessage(appointmentDetails, startDate)
        }
      }

      await fetchConnectedUser({
        authUserId: authUser.value?.id
      })

      if (isDoctor.value) {
        await getActiveCompany()
        const { userCompany } = await fetchPatienstByDoctor({
          companyId: Number(activeCompany.value?.id),
          groupName: 'Patient',
          doctorId: Number(authUser.value?.id),
          statusName: "Approve",
          statusId: Number(approvedStatus.value?.id),
        })
        const patients = userCompany.edges.map((user: any) => {
          return {
            id: user.node.user.id,
            firstName: user.node.user.firstName,
            lastName: user.node.user.lastName,
            name: user.node.user.name,
            email: user.node.user.email,
            username: user.node.user.username,
            avatar: user.node.user.avatar,
            lastConversation: null,
          }
        })
        commit('chat/SET_PATIENT_OR_DOCTOR__USERS', patients)
      } else {
        const { userCompany } = await fetchDoctorsByPatient({
          userId: Number(authUser.value?.id),
          groupName: 'Patient',
          statusId: Number(approvedStatus.value?.id),
        })
        const doctors = userCompany.edges.map((doctor: any) => {
          return {
            id: doctor.node.doctor.id,
            firstName: doctor.node.doctor.firstName,
            lastName: doctor.node.doctor.lastName,
            name: doctor.node.doctor.name,
            email: doctor.node.doctor.email,
            username: doctor.node.doctor.username,
            avatar: doctor.node.doctor.avatar,
            lastConversation: null,
          }
        })
        commit('chat/SET_PATIENT_OR_DOCTOR__USERS', doctors)
      }

      if (getConnectedUsers.value && getConnectedUsers.value.length > 0) {
        searchResult.value = getConnectedUsers.value
        const patientId = computed(() => route.value.query.patient)
        let user = getConnectedUsers.value[0]
        if (patientId.value) {
          const newUser = getConnectedUsers.value.find((item: Patient) => item.id == patientId.value)
          if (newUser) {
            user = newUser
          }
        }
        checkChatConnection(user).finally(() => {
          if (newMessage) {
            sendMessage(newMessage)
          }
        })
      }
    })

    onBeforeUnmount(() => {
      closeSocket()
    })

    const markAsSeen = () => {
      commit("chat/MARK_AS_SEEN_CONVERSATION");
    };

    watch(searchUser, () => {
      if (searchUser.value.length > 0) {
        searchResult.value = getConnectedUsers.value.filter((item: any) => {
          return Object.keys(item).some((key) => {
            let string = String(item[key])
            return string.toLowerCase().indexOf(searchUser.value.toLowerCase()) > -1
          })
        });
      } else {
        searchResult.value = getConnectedUsers.value
      }
    })

    const editConversation = (index: number, conversation: any) => {
      editableItem.value = conversation;
      isEditing.value = true;
      message.value = conversation.message;
      focusMessageBox();
    };

    const reset = () => {
      isEditing.value = false;
      editableItem.value = undefined;
      message.value = "";
      focusMessageBox();
    };

    const focusMessageBox = () => {
      messageBox.value?.focus();
    };

    const messageButton = computed(() => {
      if (isEditing.value) return "Update";
      else return "Send";
    });

    const setFirstPosition = () => {
      const users = JSON.parse(JSON.stringify(searchResult.value))
      if (Number(users[0].id) !== Number(selectedUser.value.id)) {
        const index = users.findIndex((user: any) => {
          return Number(user.id) === Number(selectedUser.value.id)
        })
        users.splice(index, 1)
        users.splice(0, 0, selectedUser.value)
        searchResult.value = users
      }
    }

    const sendMessage = async (defaultMessage: string) => {
      let newMessage: string = defaultMessage.length > 0 ? defaultMessage : message.value

      if (newMessage.length === 0) {
        $toast.error(`${ $t('toastMessage.Message field is required!') }`);
        return
      }

      if (selectedUser.value.id) {
        setFirstPosition()
      }


      const connectId = parseInt(connectionId.value);
      const sender = parseInt(authUser.value?.id);
      const receiver = parseInt(selectedUser.value?.id);
      if (isEditing.value) {
        const id = parseInt(editableItem.value?.id || 0);
        // await updateConversation(id, {
        //   message: message.value,
        //   isEdited: true,
        // });
        const data = {
          id,
          connection: connectId,
          sender: sender,
          receiver: receiver,
          message: newMessage,
          is_seen: false,
          is_edited: true,
          is_auto_message: !!defaultMessage.length,
          created_by: authUser.value?.id,
          updated_by: authUser.value?.id,
        }
        sendChatMessage(data)
      } else {
        // await createConversation(
        //   connectId,
        //   sender,
        //   receiver,
        //   message.value
        // );
        const data = {
          connection: connectId,
          sender: sender,
          receiver: receiver,
          message: newMessage,
          is_seen: false,
          is_edited: false,
          is_auto_message: !!defaultMessage.length,
          created_by: authUser.value?.id,
          updated_by: authUser.value?.id,
        }
        if (defaultMessage.length) {
            sendMessageWhenOpen(data)
            router.push('/admin/messages')
        } else {
            sendChatMessage(data)
        }
      }
      reset();
      setTimeout(() => {
        scrollToBottom(el.value);
      }, 500)
    };

    const avatar = (name: string) => {
      let TextAvatar = "";
      const array = name?.split(" ");
      array?.forEach((item) => {
        TextAvatar += item.substring(0, 1);
      });
      return TextAvatar;
    };

    const datetime = (date: string) => {
      return $dayjs(date).calendar();
    };

    const date = (date: string) => {
      return $dayjs(date).calendar(null, {
        sameDay: "[Today]",
        nextDay: "[Tomorrow]",
        nextWeek: "dddd",
        lastDay: "[Yesterday]",
        lastWeek: "[Last] dddd",
        sameElse: "DD/MM/YYYY",
      });
    };

    return {
      el,
      loading,
      messageBox,
      message,
      sendMessage,
      checkChatConnection,
      connectionId,
      conversations,
      avatar,
      datetime,
      date,
      isDoctor,
      markAsSeen,
      authUser,
      disableHover,
      editConversation,
      isEditing,
      messageButton,
      selectedUser,
      drawer,
      searchUser,
      searchResult,
      getConnectedUsers,
    };
  },
});
</script>

<style scoped>
.v-text-field {
  padding-top: 12px;
  margin-top: 3px;
}

.active {
  background: #dbdbdb;
}

.mxw-ftc {
  max-width: fit-content !important;
}
</style>
