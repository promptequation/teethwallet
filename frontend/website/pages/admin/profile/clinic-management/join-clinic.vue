<template>
  <v-container fluid class="down-top-padding">
    <v-card class="mb-7">
      <v-card-text class="pa-5">
        <v-row justify="space-between">
          <v-col cols="12" lg="4">
            <v-text-field append-icon="mdi-magnify" v-model="search" @keyup="searchClinics" @paste="searchClinics"
              :label="$t('joinClinic.Search Clinics')" filled background-color="transparent">
            </v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-row>
      <v-col class="pa-2" cols="12" sm="6" lg="3" v-for="(clinic, index) in clinics" :key="index">
        <v-card class="mb-7 tw-flex tw-flex-col tw-justify-between" height="100%">
          <v-card-text class="pa-5 text-center tw-flex-1">
            <div class="tw-h-28 tw-w-28 tw-mx-auto">

              <v-avatar v-if="clinic.image" size="40">
                <v-img :src="clinic.image" />
              </v-avatar>
              <span v-else class="white--text text-h5">
                <v-avatar class="profile" color="grey" size="120">
                  {{ avatar(clinic.name) }}
                </v-avatar>
              </span>
            </div>

            <h4 class="title mt-3 mb-0">{{ clinic.name }}</h4>
            <small class="subtitle-2 font-weight-regular">{{
              clinic.companyuserSet.edges.length ? clinic.companyuserSet.edges[0].node.user.name : ''
            }}</small>
            <p class="mb-0">{{ clinic.phone }}</p>
            <address class="subtitle-2 font-weight-regular mt-3">
              <span>
                {{ clinic.street }}, {{ clinic.street2 }}, {{ clinic.state }}, {{ clinic.city }}, {{ clinic.zipCode }},
                {{
                  clinic.country
                }}
              </span>
            </address>
          </v-card-text>
          <div class="text-center">
            <v-btn @click="sendAccessRequestEvent(clinic)" block color="primary"
              class="mr-2">{{ $t('joinClinic.Send Access Request') }}
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import { defineComponent, useStore, computed, ref, useContext, onMounted } from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import debounce from 'lodash.debounce'
import useJoinClinic from "~/../composables/useJoinClinic";
import useManageClinic from "~/../composables/useManageClinic";

export default defineComponent({
  layout: "admin",
  name: "JoinClinic",
  middleware: "doctor",
  setup() {
    const { $t } = useNuxtTranslator()
    const { app } = useContext();
    const { getters, commit } = useStore();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const { $toast } = app;

    const { fetchCompanies, fetchAuthUserCompanies, fetchRelatedCompaniesByAuthUser } = useJoinClinic();
    const { createDoctorTypeUserForCompany } = useManageClinic();

    const approvedStatus = computed(() => {
      return getters['common/getApprovedStatus']
    })


    const manageFetchAllCompanies = async () => {
      await fetchAuthUserCompanies({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isOwner: true,
        approvalById: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      })

      await fetchRelatedCompaniesByAuthUser({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isOwner: false,
        approvalById: null,
        langId: authUser.value?.lang?.id
      })
    }

    onMounted(async () => {
      await fetchCompanies({
        name: null,
        langId: authUser.value?.lang?.id
      })
      await manageFetchAllCompanies()
    })


    const clinics = computed(() => getters["clinic/getAllClinics"]);
    const search = ref("")

    const searchClinics = debounce(async function () {
      await fetchCompanies({
        name: search.value,
        langId: authUser.value?.lang?.id
      })
    }, 500)


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


    const sendAccessRequestEvent = async (clinic) => {

      const allGroups = computed(() => getters["user/groups"]);
      const doctorTypeGroup = allGroups.value.find((item) => {
        return item.name === 'Doctor'
      })

      try {
        const { createCompanyUser } = await createDoctorTypeUserForCompany({
          companyId: clinic.id,
          userId: Number(authUser.value?.id),
          groupId: Number(doctorTypeGroup.id),
          status: 'Pending',
          isOwner: false,
          isActive: false,
          requestedBy: authUser.value?.id,
          joinedDatetime: new Date().toISOString(),
          requestType: "DOCTOR_REQUEST"
        })
        if (createCompanyUser) {
          commit('clinic/REMOVE_CLINIC', clinic.id)
          $toast.success(`${ $t('toastMessage.Invitations Successfully Sent!') }`)
        }
      } catch (error) {
        console.log(error);
        $toast.error(error.response?.errors[0]?.message || `${ $t('toastMessage.Something is wrong!') }`)
      }

    }


    return {
      clinics,
      avatar,
      search,
      searchClinics,
      sendAccessRequestEvent,
    };
  },
});
</script>
