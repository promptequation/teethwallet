<template>
    <div>
        <v-row>
            <v-col>
                <validation-observer ref="errorReset" v-slot="{ handleSubmit }">
                    <v-form ref="addClinicForm" @submit.prevent="handleSubmit(submitAddClinic)">
                        <v-card outlined>
                            <v-card-title>
                                <ActionButton :deleteBtn="false" @click:discard="discardAll">
                                </ActionButton>
                            </v-card-title>
                            <v-card-text>
                                <v-container>
                                    <v-row>
                                        <v-col cols="6">
                                            <validation-provider v-slot="{ errors, valid }" rules="required">
                                                <v-text-field v-model="clinicName" :label="$t('Clinic Name')"
                                                    :error-messages="errors" :success="valid" outlined dense>
                                                </v-text-field>
                                            </validation-provider>
                                            <validation-provider v-slot="{ errors, valid }" rules="required">
                                                <v-text-field v-model="street" :label="$t('addClinic.Street')" :error-messages="errors" :success="valid" outlined dense></v-text-field>
                                            </validation-provider>
                                            <v-text-field v-model="streetTwo" :label="$t('addClinic.Street:2')" :success="valid"  outlined dense>
                                            </v-text-field>
                                            <v-text-field v-model="state" :label="$t('addClinic.State')" :success="valid"  outlined dense>
                                            </v-text-field>
                                            <v-text-field v-model="zipcode" :label="$t('addClinic.Zip code')" :success="valid"  outlined dense>
                                            </v-text-field>
                                            <validation-provider v-slot="{ errors, valid }" rules="required">
                                                <v-text-field v-model="city" :label="$t('addClinic.City')" :error-messages="errors"
                                                    :success="valid" outlined dense></v-text-field>
                                            </validation-provider>
                                            <validation-provider v-slot="{ errors, valid }" rules="required">
                                                <v-autocomplete v-model="country" :error-messages="errors"
                                                    :success="valid" :items="signupFieldsData.countryList"
                                                    item-value="code" item-text="name" type="string" outlined
                                                    :label="$t('Country')" dense>
                                                </v-autocomplete>
                                            </validation-provider>
                                        </v-col>
                                        <v-col cols="6">
                                            <v-card outlined class="tw-p-4">
                                                <v-data-table :headers="associateHeader" :no-data-text="$t('No data found')" :items="selectedDoctors" :footer-props="{
                                                    'items-per-page-text': $t('Rows per page'),
                                                    'items-per-page-all-text': $t('All')}" 
                                                    sort-by="id" :disable-pagination="true" class="header-text" dense hide-default-footer>
                                                    <template #item.doctorName="{ item }">
                                                        {{ item.name }}
                                                    </template>

                                                    <template #item.action="{ item }">
                                                        <v-btn depressed icon dark color="error" small title="Delete"
                                                            @click="removeDoctor(item)">
                                                            <v-icon>mdi-close</v-icon>
                                                        </v-btn>
                                                    </template>
                                                    <template v-slot:footer>
                                                        <v-combobox class="tw-mt-6" v-model="selectedDoctors"
                                                            :items="doctors" :placeholder="$t('addClinic.Type to add new doctor')"
                                                            item-text="name" dense multiple chips clearable
                                                            deletable-chips>
                                                        </v-combobox>
                                                    </template>
                                                </v-data-table>
                                            </v-card>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>
                        </v-card>
                    </v-form>
                </validation-observer>
            </v-col>
        </v-row>
    </div>
</template>
<script lang="ts">
interface associateHeaderType {
    text?: string
    value?: string
    sortable?: boolean
    align?: string
    width?: number
}

interface citiesType {
    text?: string,
    value?: string
}

interface doctorType {
    id?: string | number,
    doctorId?: string | number,
    username?: string,
    isActive?: boolean,
    email?: string,
    name?: string,
    dateOfBirth?: string,
    avatar?: string,
    groups?: any,
    companyUserid?: string | number
    joinedDatetime?: string | number
}
import { ref, defineComponent, onMounted, computed, useStore, useContext, useRouter, useRoute } from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useManageClinic from "~/../composables/useManageClinic";
import useUser from "~/../composables/useUser";
import useCountry from "@composables/useCountry";
import ActionButton from "~/components/buttons/ActionButton.vue";
import { groupType } from '~/types/companyUser'
import useJoinClinic from "~/../composables/useJoinClinic";

export default defineComponent({
    name: "AddClinic",
    middleware: "doctor",
    components: { ActionButton },
    setup() {
        const { $t } = useNuxtTranslator()
        const { app } = useContext();
        const route = useRoute()
        const { getters } = useStore();
        const router = useRouter();
        const { $toast } = app;
        const authUser = computed(() => getters["auth/getUserProfile"]);


        const {
            createUserCompany,
            updateUserCompany,
            fetchSingleCompany,
            fetchCities,
            createCompanyUserForCompanyOwner,
            createDoctorTypeUserForCompany,
            deleteCompanyUser
        } = useManageClinic();
        const { fetchActiveCompanyForUser } = useJoinClinic();

        const { fetchDoctors } = useUser();
        const { signupFieldsData, getSignupFieldsData } = useCountry();
        getSignupFieldsData()
        fetchDoctors()

        const doctors = computed(() => getters["user/getAllDoctorWithOutAuthUser"]);

        const associateHeader = ref<associateHeaderType[]>();
        const associateHeaders = () => {
            return [
                { text: `${$t('addClinic.Doctor Name')}`, value: "doctorName" },
                { text: `${$t('Actions')}`, value: "action", sortable: false, align: "center" },
            ]
        };
        const showAssociateHeaders = () => {
            associateHeader.value = associateHeaders()
        }

        const selectedDoctors = ref<doctorType[]>([]);

        const clinicName = ref<string>("");
        const street = ref<string>("");
        const streetTwo = ref<string>("");
        const zipcode = ref<string>("");
        const country = ref<string>("");
        const city = ref<string>("");
        const cities = ref<citiesType[]>();
        const state = ref<string>("");
        const addClinicForm = ref(null)
        const errorReset = ref()
        const isEditAbleMode = ref(false)
        const existingDoctor = ref<doctorType[]>([])

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

        const submitAddClinic = async () => {


            if (isEditAbleMode.value) {
                updateCompany()
            } else {

                const isActiveCompany = await isExistActiveCompany()

                const { createCompany } = await createUserCompany({
                    name: clinicName.value,
                    state: state.value,
                    street: street.value,
                    street2: streetTwo.value,
                    city: city.value,
                    zipcode: zipcode.value,
                    country: country.value,
                    createdBy: authUser.value?.id,
                    updatedBy: authUser.value?.id,
                });


                if (createCompany && createCompany.company.id) {
                    // create company user for auth user

                    const allGroups = computed(() => getters["user/groups"]);
                    const doctorTypeGroup = allGroups.value.find((item: groupType) => {
                        return item.name === 'Doctor'
                    })

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

                    // create a company user for every selected doctor
                    selectedDoctors.value.forEach(async (doctor: doctorType) => {
                        await createDoctorTypeUserForCompany({
                            companyId: createCompany?.company.id,
                            userId: Number(doctor.id),
                            groupId: Number(doctorTypeGroup.id),
                            status: 'Pending',
                            isOwner: false,
                            isActive: false,
                            requestedBy: authUser?.value.id,
                            joinedDatetime: new Date().toISOString(),                           
                            requestType: "OWNER_REQUEST"
                        })
                    })
                    resetForm()
                    $toast.success(`${ $t('toastMessage.New Clinic  Successfully Created!') }`);
                } else {
                    $toast.error(`${ $t('toastMessage.Something went wrong, please try again later') }`);
                }

            }
        };

        const updateCompany = async () => {
            const existingItems: doctorType[] = []
            const newItems: doctorType[] = []
            const deleteAbleItems: doctorType[] = []


            const existingDoctorIds = existingDoctor.value.map((item: doctorType) => {
                return item.id
            })

            const selectedDoctorIds = selectedDoctors.value.map((item: doctorType) => {
                return item.id
            })

            selectedDoctors.value.forEach((item: doctorType) => {
                if (existingDoctorIds.includes(item.id)) {
                    existingItems.push(item)
                } else {
                    newItems.push(item)
                }
            })

            existingDoctor.value.forEach((item: doctorType) => {
                if (!selectedDoctorIds.includes(item.id)) {
                    deleteAbleItems.push(item)

                }
            })


            if (deleteAbleItems.length > 0) {
                deleteAbleItems.forEach(async (item: doctorType) => {
                    await deleteCompanyUser(item.companyUserid)
                })
            }

            await updateUserCompany({
                id: Number(route.value.query.edit),
                name: clinicName.value,
                state: state.value,
                street: street.value,
                street2: streetTwo.value,
                city: city.value,
                zipcode: zipcode.value,
                country: country.value,
                updatedBy: authUser.value?.id,
            })

            if (newItems.length > 0) {

                const allGroups = computed(() => getters["user/groups"]);
                const doctorTypeGroup = allGroups.value.find((item: groupType) => {
                    return item.name === 'Doctor'
                })

                newItems.forEach(async (doctor: doctorType) => {
                    await createDoctorTypeUserForCompany({
                        companyId: Number(route.value.query.edit),
                        userId: Number(doctor.id),
                        groupId: Number(doctorTypeGroup.id),
                        status: 'Pending',
                        isOwner: false,
                        isActive: false,
                        requestedBy: authUser?.value.id,
                        joinedDatetime: new Date().toISOString(),
                        requestType: "OWNER_REQUEST"
                    })
                })
            }
            $toast.success(`${ $t('toastMessage.Clinic Successfully Updated!') }`);
            discardAll()
        }

        const resetForm = () => {
            clinicName.value = ''
            street.value = ''
            streetTwo.value = ''
            zipcode.value = ''
            country.value = ''
            city.value = ''
            state.value = ''
            selectedDoctors.value = []
            errorReset.value?.reset()
        }

        const removeDoctor = (item: any) => {
            const findIndex = selectedDoctors?.value.findIndex((doctor: doctorType) => {
                return doctor.id === item.id;
            });
            selectedDoctors.value.splice(findIndex, 1);
        };

        const discardAll = () => {
            router.push('/admin/profile/clinic-management')
        }

        const manageEditAbleData = async (id: any) => {
            isEditAbleMode.value = true
            const { company } = await fetchSingleCompany({
                companyId: Number(id),
                groupName: 'Doctor'
            })

            if (company) {
                clinicName.value = company.name
                street.value = company.street
                streetTwo.value = company.street2
                zipcode.value = company.zipcode
                country.value = company.country
                city.value = company.city
                state.value = company.state

                let doctors: doctorType[] = []

                company.companyuserSet?.edges.forEach((item: any) => {
                    if (authUser.value.id !== item.node.user.id) { // without company owner(authUser)

                        if (
                            (item.node.requestedBy && item.node.requestedBy.id === authUser.value.id) ||
                            (item.node.requestedBy && item.node.requestedBy.id !== authUser.value.id &&
                                item.node.status && item.node.status.id === approvedStatus.value?.id)
                        ) {
                            doctors.push({
                                ...item.node.user,
                                companyUserid: item.node.id
                            })
                        }
                    }
                })
                selectedDoctors.value = doctors
                existingDoctor.value = Object.assign([], doctors)
            }
        }

        onMounted(async () => {
            showAssociateHeaders()
            cities.value = fetchCities();
            if (route.value.query?.edit) {
                await manageEditAbleData(route.value.query.edit)
            }
        });



        return {
            associateHeader,
            associateHeaders,
            showAssociateHeaders,
            selectedDoctors,
            removeDoctor,
            country,
            signupFieldsData,
            city,
            cities,
            clinicName,
            street,
            streetTwo,
            state,
            zipcode,
            submitAddClinic,
            doctors,
            addClinicForm,
            discardAll,
            errorReset,
        };
    },
});
</script>
