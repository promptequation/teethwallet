<template>
  <v-app-bar app clipped-left clipped-right color="primary" dark>
    <!---Logo part -->
    <v-toolbar-title class="align-center d-flex">
      <span class="logo-text ml-2" :class="`${showLogo ? '' : 'hidelogo'}`">
        <logo />
      </span>
    </v-toolbar-title>
    <!---Logo part -->
    <!---/Toggle sidebar part -->
    <div @click="showhideLogo">
      <v-app-bar-nav-icon @click="
        $vuetify.breakpoint.smAndDown
          ? setSidebarDrawer(!Sidebar_drawer)
          : $emit('input', !value)
      " />
    </div>
    <!---/Toggle sidebar part -->
    <!---Search part -->
    <v-btn dark icon class="mr-1 d-sm-block d-none" @click="searchbox">
      <v-icon>mdi-magnify</v-icon>
    </v-btn>

    <div v-if="showSearch" class="searchinput white">
      <template>
        <v-text-field :placeholder="$t('Search Now')" :label="$t('Search')" class="mt-3 mb-3" hide-details light outlined dense
          append-outer-icon="mdi-close" @click:append-outer="searchbox"></v-text-field>
      </template>
    </div>
    <!---/Search part -->
    <v-spacer />
    <!---right part -->
    <!---Notification -->
    <v-menu bottom left offset-y origin="top right" transition="scale-transition">
      <template class="tw-relative" v-slot:activator="{ on }">
        <v-btn dark icon v-on="on" class="mr-1">
          <v-badge v-if="!notificationIsRead" class="tw-absolute tw-left-5 tw-bottom-3" color="warning" dot
            right></v-badge>
          <v-icon>mdi-bell</v-icon>
        </v-btn>
      </template>

      <v-list class="notification-body">
        <h4 class="px-5 py-3 pt-2 font-weight-medium title ">{{ $t('header.Notifications') }}</h4>
        <v-divider></v-divider>
        <div v-if="notifications.length === 0" class="black--text font-weight-medium no-notification-message">
          <h4>{{ $t('notification.No notification found') }}</h4>
        </div>
        <v-list-item class="px-0" v-for="(item, i) in notifications" :key="i">
          <v-list-item-title class="px-5" @click="updateSelectedNotification(item.id, true)"
            :class="item.isRead === false ? 'tw-bg-gray-200' : ''">
            <div class="d-flex align-center justify-space-between py-3">
              <div>
                <div class="tw-cursor-pointer" @click="redirectUser(item.notificationType, item.appointment !== null ? item.appointment.id : '')">
                  <h4 v-if="item.notificationType === 'OWNER_REQUEST'" class="black--text font-weight-medium ">
                    {{ $t('notification.Clinic') }}
                    {{ item.company.name }} {{ $t('notification.has sent you an invitation') }}
                  </h4>
                  <h4 v-if="item.notificationType === 'DOCTOR_REQUEST'" class="black--text font-weight-medium ">
                    {{ $t('notification.doctor') }} {{ item.createdBy.name }} {{ $t('notification.has sent you an invitation') }}
                    {{ item.company.name }}
                  </h4>
                  <h4 v-if="item.notificationType === 'DOCTOR_APPROVAL'" class="black--text font-weight-medium ">Dr.
                    {{ item.createdBy.name }} {{ $t('notification.accepted your invitation') }}</h4>
                  <h4 v-if="item.notificationType === 'OWNER_APPROVAL'" class="black--text font-weight-medium ">Clinic
                    {{ item.company.name }} {{ $t('notification.accepted your invitation') }}</h4>
                  <h4 v-if="item.notificationType === 'PATIENT_REQUEST_DOCTOR'" class="black--text font-weight-medium ">
                    {{ item.createdBy.name }} {{ $t('notification.wants to give you an access') }} </h4>
                  <h4 v-if="item.notificationType === 'DOCTOR_ACCEPT_PATIENT_REQUEST'"
                    class="black--text font-weight-medium ">Clinic
                    {{ item.createdBy.name }} {{ $t('notification.accepted your access request') }} </h4>
                  <h4 v-if="item.notificationType === 'DOCTOR_REVOKE_PATIENT_ACCESS'"
                    class="black--text font-weight-medium ">
                    {{ $t('notification.Your Dentist') }} {{ item.createdBy.name }} {{ $t('notification.has revoked your access to his history') }} </h4>
                  <h4 v-if="item.notificationType === 'PATIENT_REVOKE_DOCTOR_ACCESS'"
                    class="black--text font-weight-medium ">
                    {{ $t('notification.Your Patient') }} {{ item.createdBy.name }} {{ $t('notification.has revoked your access to his history') }} </h4>
                  <h4 v-if="item.notificationType === 'APPOINTMENT_CREATED'"
                    class="black--text font-weight-medium ">
                    {{ item.createdBy.name }} {{ $t('notification.has created an appointment for you') }} </h4>
                  <h4 v-if="item.notificationType === 'APPOINTMENT_FOLLOW_UP_CREATED' && isDoctor"
                    class="black--text font-weight-medium">
                    {{ $t('notification.A patient follow-up activity requires your attention in') }} {{FollowUpInterval(item)}} {{ $t('notification.days') }}  </h4>
                  <div v-if="item.notificationType === 'APPOINTMENT_FOLLOW_UP_CREATED' && !isDoctor">
                    <h4 class="black--text font-weight-medium">
                    {{ $t('notification.doctor') }} {{ item.createdBy.name }} {{ $t('notification.recommends you schedule an appointment in') }} {{FollowUpInterval(item)}}  {{ $t('notification.days') }} </h4>
                  </div>
                  <small class="text--secondary">{{ datetime(item.createdAt) }}</small>
                </div>
              </div>

              <div>
                <v-menu bottom left>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn class="ml-4" icon v-bind="attrs" v-on="on">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>

                  <v-card class="mx-auto" max-width="500">
                    <v-list>
                      <v-list-item-group>
                        <v-list-item @click="updateSelectedNotification(item.id, true)">
                          <v-list-item-content>
                            <v-list-item-title>{{ $t('header.Mark as read') }}</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item @click="deleteSelectedNotification(item.id)">
                          <v-list-item-content>
                            <v-list-item-title>{{ $t('header.Delete') }}</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list-item-group>
                    </v-list>
                  </v-card>
                </v-menu>
              </div>
            </div>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <!---Notification -->
    <!---User -->
    <v-menu bottom left offset-y origin="top right" transition="scale-transition">
      <template v-slot:activator="{ on }">
        <v-btn dark icon v-on="on" class="mr-1">
          <v-avatar v-if="authUser.avatar" size="40">
            <v-img :src="authUser.avatar" />
          </v-avatar>
          <span v-else class="white--text text-h6">
            <v-avatar class="profile" color="grey" size="40">
              {{ setAvatarLetter }}
            </v-avatar>
          </span>
        </v-btn>
      </template>

      <v-list class="min-with">
        <v-list-item active-class="active-color" nuxt to="/admin/profile/info">
          <v-list-item-title>{{ $t('header.Profile') }}</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isDoctor" @click="userSwitch">
          <v-list-item-title>{{ $t('header.Switch as patient') }}</v-list-item-title>
        </v-list-item>
        <v-list-item nuxt @click="logout">
          <v-list-item-title>{{ $t('header.Logout') }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <!---User -->
  </v-app-bar>
</template>
<script>
import { computed, onMounted, reactive, ref, SetupContext, useContext, useRouter, useStore, onBeforeUnmount } from "@nuxtjs/composition-api";
import useToast from "vue-toastification";
import { mapMutations, mapState } from "vuex";
import useJoinClinic from "~/../composables/useJoinClinic";
import useManageClinic from "~/../composables/useManageClinic";
import useMyInvitations from "~/../composables/useMyInvitations";
import useNotification from "~/../composables/useNotification";
import useUser from "~/../composables/useUser";
import useAuth from "../../../../../composables/useAuth";
import useUserData from "../../../../../composables/useUser";
import dayjs from "dayjs";

export default {
  name: "Header",
  components: {
    Logo: () => import("@common-components/Logo.vue"),
  },
  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
  setup({ }, context) {
    const { isDoctor, isSwitchToDoctor, fetchGroups } = useUser();
    const { getters, commit, dispatch } = useStore();
    const { createUserCompany, createCompanyUserForCompanyOwner } = useManageClinic();
    const { fetchUserLookup } = useMyInvitations()
    const { fetchNotifications, receiveNotification, joinNotificationRoom, closeSocket, deleteNotification, updateNotification } = useNotification()
    const { fetchAuthUserCompanies, fetchActiveCompanyForUser } = useJoinClinic();
    const { $dayjs } = useContext();
    const router = useRouter();

    fetchGroups()
    const { updateUserGroup } = useUserData();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const redirect = {
      logout: "/",
    };
    const { logout } = useAuth();

    fetchNotifications({
      userId: Number(authUser.value?.id)
    })

    const avatar = (name) => {
      let textAvatar = "";
      const array = name?.split(" ");
      if (array) {
        array.forEach((item) => {
          textAvatar += item.substring(0, 1);
        });
      }
      return textAvatar;
    };


    const allGroups = computed(() => getters["user/groups"]);


    const approvedStatus = computed(() => {
      return getters['common/getApprovedStatus']
    })


    const isExistActiveCompany = async () => {
      const { userCompany } = await fetchActiveCompanyForUser({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isActive: true
      })

      if (userCompany && userCompany.edges && userCompany.edges.length > 0) {
        return true
      } else {
        return false
      }
    }


    const userSwitch = async () => {
      commit('SET_OVERLAY', true)
      commit('SET_LOADING', true)

      const doctorTypeGroup = allGroups.value.find((item) => {
        return item.name === 'Doctor'
      })

      const groupName = isDoctor.value ? 'Patient' : 'Doctor'

      await updateUserGroup({
        userId: authUser?.value.id,
        group: groupName
      })

      const userdata = authUser.value

      const isCompanyEmpty = await checkCompaniesEmptyOrNot()


      if (isCompanyEmpty) {
        // user company
        const isActiveCompany = await isExistActiveCompany()

        const { createCompany } = await createUserCompany({
          name: userdata.firstName + ' ' + userdata.lastName,
          ...userdata,
          createdBy: authUser.value?.id,
          updatedBy: authUser.value?.id,
        })

        // create company user
        await createCompanyUserForCompanyOwner({
          companyId: createCompany?.company.id,
          userId: authUser?.value.id,
          doctorId: null,
          groupId: Number(doctorTypeGroup.id),
          status: 'Approve',
          isOwner: true,
          isActive: !isActiveCompany,
          joinedDatetime: new Date().toISOString(),
          approvalById: authUser?.value.id,
          approvalAt: new Date().toISOString(),
          requestedBy: authUser?.value.id,
        })
      }

      await dispatch('auth/reFatchUserprofile')

      commit('SET_OVERLAY', false)
      commit('SET_LOADING', false)

      location.reload()
    }


    const checkCompaniesEmptyOrNot = async () => {
      const response = await fetchAuthUserCompanies({
        userId: Number(authUser.value?.id),
        groupName: "Doctor",
        statusId: Number(approvedStatus.value?.id),
        isOwner: true,
        approvalById: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      });

      return response && response.length === 0 ? true : false
    }

    const redirectUser = (notificationType, appointmentId) => {
      if (notificationType === 'OWNER_REQUEST') {
        router.push('/admin/profile/clinic-management/clinic-invitations')
      } else if (notificationType === 'DOCTOR_REQUEST') {
        router.push('/admin/profile/clinic-management/doctor-invitations')
      } else if (notificationType === 'DOCTOR_APPROVAL') {
        router.push('/admin/profile/clinic-management')
      } else if (notificationType === 'OWNER_APPROVAL') {
        router.push('/admin/profile/clinic-management')
      } else if (notificationType === 'PATIENT_REQUEST_DOCTOR') {
        router.push('/admin/patient-invitations')
      } else if (notificationType === 'DOCTOR_ACCEPT_PATIENT_REQUEST') {
        router.push('/admin')
      } else if (notificationType === 'DOCTOR_REVOKE_PATIENT_ACCESS') {
        router.push('/admin/profile/access-management')
      } else if (notificationType === 'PATIENT_REVOKE_DOCTOR_ACCESS') {
        router.push('/admin/patients')
      } else if (notificationType === 'APPOINTMENT_CREATED') {
        router.push(`/admin/appointments/entry?editableId=${appointmentId}`)
      } else if (notificationType === 'APPOINTMENT_FOLLOW_UP_CREATED') {
        router.push(`/admin/appointments/entry?editableId=${appointmentId}&tab=follow-up`)
      }
    }

    const datetime = (date) => {
      return $dayjs(date).format("DD/MM/YY h:mm A");
    };

    const followUpFormat = (date) => {
      return $dayjs(date).format("DD/M/YYYY");
    };
  
    const notifications = computed(() => getters["notification/notifications"]);
    
    const FollowUpInterval = (item) => {
        let now = $dayjs();
        let followUpDates = item?.appointmentFollowUp?.followUpDate
        const followUpDate = $dayjs(followUpDates).diff(now, 'day')   
        return followUpDate.toString()
    }

    const notificationIsRead = computed(() => {
      return notifications.value.every((item) => item.isRead)
    })

    const showLogo = ref(true);

    const showSearch = ref(false);

    const showhideLogo = () => {
      showLogo.value = !showLogo.value;
    }
    const searchbox = () => {
      showSearch.value = !showSearch.value;
    }

    const deleteSelectedNotification = async (id) => {
      await deleteNotification(id)
      await fetchNotifications({
        userId: Number(authUser.value?.id)
      })
    }

    const updateSelectedNotification = async (id, isRead) => {
      await updateNotification(id, isRead)
      await fetchNotifications({
        userId: Number(authUser.value?.id)
      })
    }

    const setAvatarLetter = computed(() => {
      let firstName = avatar(authUser?.value?.firstName?.split(' ').map((word) => word[0]).join(''))
      let lastName = avatar(authUser?.value?.lastName?.split(' ').map((word) => word[0]).join(''))
      return (`${firstName}${lastName}`)
    })

    onMounted(() => {
      joinNotificationRoom(authUser.value.id);
      receiveNotification()
    })

    onBeforeUnmount(() => {
      closeSocket()
    })

    return {
      logout,
      authUser,
      avatar,
      setAvatarLetter,
      isDoctor,
      isSwitchToDoctor,
      userSwitch,
      notifications,
      notificationIsRead,
      datetime,
      redirectUser,
      followUpFormat,
      FollowUpInterval,
      showLogo,
      showSearch,
      showhideLogo,
      searchbox,
      deleteSelectedNotification,
      updateSelectedNotification,
    };
  },

  computed: {
    ...mapState(["Sidebar_drawer"]),
  },

  methods: {
    ...mapMutations({
      setSidebarDrawer: "SET_SIDEBAR_DRAWER",
    }),
  },
};
</script>

<style lang="scss">
.active-color {
  background-color: #1e88e5 !important;
  color: #fff !important;
}

.min-with {
  min-width: 160px;
}

.hidelogo {
  display: none;
}

.searchinput {
  position: absolute;
  width: 100%;
  margin: 0;
  left: 0;
  z-index: 10;
  padding: 0 15px;
}

.descpart {
  max-width: 220px;
}

.notification-body {
  overflow: auto;
  max-height: 500px;
  min-width: 475px;
}

.no-notification-message {
  height: 150px;
  min-width: 475px;
  display: flex;
  align-items: center;
  justify-content: center;
}</style>