<template>
  <v-container fluid class="down-top-padding">
    <v-card class="mb-7">
      <v-card-text class="pa-5">
        <v-row justify="space-between">
          <v-col cols="12" lg="4">
            <v-text-field append-icon="mdi-magnify" v-model="search" @keyup="searchDoctor" @paste="searchDoctor"
              :label="$t('doctors.Search Doctors')" filled background-color="transparent" hide-details>
            </v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-row v-if="doctors">
      <v-col class="pa-2" cols="12" sm="6" lg="3" v-for="(doctor, index) in doctors" :key="index">
        <v-card class="mb-7 tw-flex tw-flex-col tw-justify-between" height="100%">
          <v-card-text class="text-center pa-5 tw-flex-1">
            <div class="tw-h-28 tw-w-28 tw-mx-auto">
              <v-avatar v-if="doctor.user.avatar" size="40">
                <v-img :src="doctor.user.avatar" />
              </v-avatar>
              <span v-else class="white--text text-h5">
                <v-avatar class="profile" color="grey" size="120">
                  {{ avatar(doctor.user.name) }}
                </v-avatar>
              </span>
            </div>

            <h4 class="mt-3 mb-0 title">{{ doctor.user.name }}</h4>
            <small class="subtitle-2 font-weight-regular">{{
                doctor.user.email
            }}</small>
            <p class="mb-0">{{ doctor.user.phone }}</p>
            <p class="mb-0">Practice: {{ doctor.company.name }}</p>
            <address class="mt-3 subtitle-2 font-weight-regular">
              <span v-for=" spaci in doctor.user.userspecializationSet.edges">
                <v-chip class="ma-1" small color="primary"> {{ spaci && spaci.node.specialization &&
                    spaci.node.specialization.name
                }}
                </v-chip>
              </span>
            </address>
          </v-card-text>
          <div class="text-center">
            <v-btn @click="giveAccess(doctor)" block color="primary" class="mr-2">{{$t('doctors.Give Access')}}</v-btn>
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
import useManageClinic from "~/../composables/useManageClinic";

export default defineComponent({
  layout: "admin",
  name: "Doctors",
  middleware: "patient",
  setup() {
    const { $t } = useNuxtTranslator()
    const { app } = useContext();
    const { getters, commit } = useStore();
    const { $toast } = app;
    const {
      fetchRequestedDoctorListByAuthUser,
      fetchDoctorLists,
      createPatientTypeUserForCompany
    } = useManageClinic();

    const authUser = computed(() => getters["auth/getUserProfile"]);
    const approvedStatus = computed(() => getters['common/getApprovedStatus'])
    const doctors = computed(() => getters["clinic/doctors"]);


    const fetchAllDoctorsFromCompanyUsers = async () => {
      await fetchDoctorLists({
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value.id),
        companyName: null,
        userName: null,
        userEmail: null,
        langId: authUser.value?.lang?.id
      })

    }

    onMounted(async () => {
      await fetchRequestedDoctorListByAuthUser({
        userId: Number(authUser.value?.id)
      })
      fetchAllDoctorsFromCompanyUsers()
    })

    const search = ref("")

    const searchDoctor = debounce(async function () {

      commit('clinic/SET_EMPTY_CLINIC')

      await fetchDoctorLists({
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value.id),
        companyName: search.value,
        userName: null,
        userEmail: null,
        langId: authUser.value?.lang?.id
      })

      await fetchDoctorLists({
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value.id),
        companyName: null,
        userName: search.value,
        userEmail: null,
        langId: authUser.value?.lang?.id
      })

      await fetchDoctorLists({
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value.id),
        companyName: null,
        userName: null,
        userEmail: search.value,
        langId: authUser.value?.lang?.id
      })
    }, 500)


    const giveAccess = async (doctor) => {
      const companyId = doctor.company.id

      const allGroups = computed(() => getters["user/groups"]);
      const patientTypeGroup = allGroups.value.find((item) => {
        return item.name === 'Patient'
      })


      if (companyId) {
        try {
          const { createCompanyUser } = await createPatientTypeUserForCompany({
            companyId,
            userId: authUser.value?.id,
            doctorId: doctor.user.id,
            groupId: patientTypeGroup.id,
            status: 'Pending',
            isOwner: false,
            isActive: false,
            requestedBy: authUser.value?.id,
            requestType: "PATIENT_REQUEST_DOCTOR"
          })

          if (createCompanyUser) {
            const node = { node: { ...doctor } }
            $toast.success(`${ $t('toastMessage.Request successfully sent!') }`);
            commit('clinic/PUSH_REQUESTED_DOCTORS', node)
          }

        } catch (error) {
          console.log(error);
        }
      } else {
        $toast.error(`${ $t('toastMessage.Something is wrong!') }`)
      }

    }

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

    return {
      doctors,
      search,
      searchDoctor,
      giveAccess,
      avatar,
    };
  },
});
</script>
