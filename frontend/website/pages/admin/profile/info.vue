<template>
  <validation-observer v-slot="{ handleSubmit }">
    <v-form @submit.prevent="handleSubmit(updateTheUserProfileInfo)">
      <v-row>
        <v-col>
          <v-card>
            <v-card-title class="pa-6">
              <v-row>
                <v-col cols="auto" class="mr-auto">
                  <v-icon large left> mdi-account </v-icon>

                  <span class="text-h6 blue-grey--text text--darken-3">{{$t('info.Profile')}}</span>
                </v-col>
                <v-col cols="auto">
                  <v-btn @click="changeLocale" dark type="submit" color="green" class="mr-3 elevation-12">
                    {{$t('info.Save')}}
                  </v-btn>
                  <v-btn @click="reFatchUserprofile" color="warning"
                    class="elevation-12">
                    {{$t('info.Discard')}}
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-title>

            <v-card-text>
              <v-container fluid>
                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('First Name')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors, valid }" rules="required|alpha_spaces">
                      <v-text-field type="text" v-model="firstName" :error-messages="errors" :success="valid"
                        outlined />
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('Last Name')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors, valid }" rules="required|alpha_spaces">
                      <v-text-field v-model="lastName" :error-messages="errors" :success="valid" outlined />
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('Username')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors, valid }" rules="required|alpha_num" name="username">
                      <v-text-field v-model="username" :error-messages="errors" :success="valid" outlined />
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('Email')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors, valid }" rules="required|email">
                      <v-text-field v-model="email" :error-messages="errors" :success="valid" outlined />
                    </validation-provider>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('Birthday date')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors }" rules="required">
                      <v-menu ref="menu" v-model="menu" :close-on-content-click="false" transition="scale-transition"
                        offset-y min-width="auto">
                        <template v-slot:activator="{ on, attrs }">
                          <validation-provider v-slot="{ errors, valid }" rules="required">
                            <v-text-field outlined title="Birthday date" v-model="dateOfBirth" :error-messages="errors" :success="valid"
                              placeholder="Birthday date" readonly v-bind="attrs" v-on="on" />
                          </validation-provider>
                        </template>
                        <validation-provider v-slot="{ errors }" rules="required">
                          <v-date-picker v-model="dateOfBirth" :active-picker.sync="activePicker"
                            :max="(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
                            min="1910-01-01" />
                        </validation-provider>
                      </v-menu>
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('info.Street')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors, valid }" rules="required" name="street">
                      <v-text-field v-model="street" :error-messages="errors" :success="valid" outlined />
                    </validation-provider>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="4" />
                  <v-col cols="8">
                      <v-text-field v-model="street2" outlined />
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('info.City / Country')}}</v-subheader>
                  </v-col>
                  <v-col cols="3">
                      <validation-provider v-slot="{ errors, valid }" rules="required" name="city">
                        <v-text-field v-model="city" :error-messages="errors" :success="valid" outlined />
                      </validation-provider>
                  </v-col>
                  <v-col cols="5">
                    <validation-provider v-slot="{ errors, valid }" rules="required">
                      <v-select outlined v-model="country" :error-messages="errors" :success="valid"
                        :items="signupFieldsData.countryList" item-value="code" item-text="name" :label="$t('Country')"
                        name="country" type="text" color="primary" />
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('Language')}}</v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider v-slot="{ errors, valid }" rules="required">
                      <v-combobox v-model="lang" :error-messages="errors" :success="valid"
                        :items="signupFieldsData.multiLanguage" item-text="name" type="text"
                        outlined />
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row v-if="isSwitchToDoctor">
                  <v-col cols="4">
                    <v-subheader class="text-body-1">
                      {{$t('info.You are allowing the participation in university studies, sharing your answers to the surveys and your personal contacts for posterior contact')}}
                    </v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <validation-provider rules="required" vid="isDentist">
                      <v-checkbox v-model="accessSurvey" outlined color="green" :label="$t('info.Access to the surveys')" />
                    </validation-provider>
                  </v-col>
                </v-row>

                <v-row v-if="isSwitchToDoctor">
                  <v-col cols="4">
                    <v-subheader class="text-body-1">{{$t('info.Can act on behalf of:')}} </v-subheader>
                  </v-col>
                  <v-col cols="8">
                    <v-row>
                      <v-col v-for="(person, index) in patientsManaged" :key="index">
                        <v-sheet color="primary" class="white--text text-center pa-3" rounded elevation="6" height="50"
                          width="180">
                          <v-icon color="white"> mdi-account </v-icon>
                          <span class="subtitle-1">{{ person.name }}</span>
                        </v-sheet>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>

                <v-row v-if="isSwitchToDoctor">
                  <v-col cols="4" />
                  <v-col cols="8">
                    <v-row>
                      <v-col cols="4">
                        <validation-provider rules="required" vid="isDentist">
                          <v-checkbox v-model="isDentist" outlined color="green" :label="$t('info.I am Dentist')" />
                        </validation-provider>
                      </v-col>
                      <v-col cols="8" v-if="isDentist">
                        <validation-provider v-slot="{ errors, valid }" rules="required">
                          <v-autocomplete multiple v-model="speciality" :error-messages="errors" :success="valid"
                            :items="specialities" outlined :label="$t('info.Speciality')" item-value="id" item-text="name" />
                        </validation-provider>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </validation-observer>
</template>

<script>
import { mapFields } from "vuex-map-fields";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import { state } from "@common-store/auth";
import { useStore, computed, ref, onMounted, useContext, useRoute } from "@nuxtjs/composition-api";
import useUser from "@common-composables/useUser";
import useCountry from "@composables/useCountry";
import useManageClinic from "~/../composables/useManageClinic";
import useJoinClinic from "~/../composables/useJoinClinic";
import async from "~/middleware/authenticated";
import { locale } from "dayjs";

const userDataFields = Object.keys(state().profile);

export default {
  layout: "admin",
  setup({ }, { root }) {
    const { app } = useContext();
    const { i18n } = app;
    const { getters, dispatch, commit } = useStore();
    const {
      isSwitchToDoctor,
      updateUserProfile,
      fetchSpecialities,
      deleteUserSpecialization,
      createUserSpecialization,
      updateUserGroup,
    } = useUser();


    const menu = false;
    const activePicker = null;

    const {
      createUserCompany,
      createCompanyUserForCompanyOwner,
    } = useManageClinic();

    const { fetchAuthUserCompanies, fetchActiveCompanyForUser } = useJoinClinic();

    const { signupFieldsData, getSignupFieldsData } = useCountry();
    getSignupFieldsData()

    const specialities = computed(() => getters["user/specialities"])
    const authUser = computed(() => getters["auth/getUserProfile"])
    // get specialities and user  selected specialities
    fetchSpecialities({
        langId: authUser.value?.lang?.id
    })

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


    const updateTheUserProfileInfo = async () => {
      commit('SET_OVERLAY', true)
      commit('SET_LOADING', true)

      await updateUserProfile() // update user profile
      const userData = authUser.value

      const allGroups = computed(() => getters["user/groups"]);

      const doctorTypeGroup = allGroups.value.find((item) => {
        return item.name === 'Doctor'
      })

      const groupName = authUser.value.isDentist ? 'Doctor' : 'Patient'

      await updateUserGroup({
        userId: authUser?.value.id,
        group: groupName
      })

      if (authUser.value.isDentist) {

        const isCompanyEmpty = await checkCompaniesEmptyOrNot()

        if (isCompanyEmpty) {
          // user company
          const { createCompany } = await createUserCompany({
            name: userData.firstName + ' ' + userData.lastName,
            ...userData,
            createdBy: authUser.value?.id,
            updatedBy: authUser.value?.id,
          })

          const isActiveCompany = await isExistActiveCompany()

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

        await deleteUserSpecialization({ userId: authUser?.value.id })
        authUser.value?.speciality.forEach(async (id) => {
          await createUserSpecialization({ userId: authUser.value.id, specialitiesId: id })
        })
        await dispatch('auth/reFatchUserprofile')
      }

      await dispatch('auth/reFatchUserprofile')
      i18n.setLocale(authUser.value?.lang?.code)
      commit('auth/SET_NEW_LANG', authUser.value?.lang?.code)

      commit('SET_OVERLAY', false)
      commit('SET_LOADING', false)
    }

    const checkCompaniesEmptyOrNot = async () => {
      const response = await fetchAuthUserCompanies({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isOwner: true,
        approvalById: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      })

      return response && response.length === 0 ? true : false
    }

    const cities = ref([
      { text: "Dhaka", value: "bn" },
      { text: "Kolkata", value: "ar" },
      { text: "Islamabad", value: "pk" },
      { text: "Modina", value: "in" },
    ])

    const reFatchUserprofile = async () => {
      await dispatch('auth/reFatchUserprofile')
    }

    const availableLocales = computed(() => {
      return app.i18n.locales
    })

    onMounted(async () => {
      await dispatch('auth/reFatchUserprofile')
    })

    return {
      updateUserProfile,
      updateTheUserProfileInfo,
      specialities,
      availableLocales,
      signupFieldsData,
      cities,
      reFatchUserprofile,
      isSwitchToDoctor,
      menu,
      activePicker
    };
  },

  methods: {
    changeLocale(event) {
      this.$i18n.setLocale(event.code)
    }
  },
  computed: {
    ...mapFields(
      "auth",
      userDataFields.map((field) => `profile.${field}`)
    ),
  },
};
</script>
