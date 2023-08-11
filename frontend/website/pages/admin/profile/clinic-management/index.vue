<template>
  <div>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title class="pa-6">
            <v-row>
              <v-col>
              </v-col>
              <v-col cols="12" class="mr-auto">
                <span class="text-h6 blue-grey--text text--darken-3 font-size">{{$t('clinicManagement.Manage Clinics')}}</span>
              </v-col>

            </v-row>
          </v-card-title>

          <v-card-text>
            <v-data-table :headers="header" :items="usersCompany" :no-data-text="$t('No data found')" sort-by="id" :footer-props="{
              'items-per-page-text': $t('Rows per page'),
              'items-per-page-all-text': $t('All')
               }"
              class="contact-listing-app header-text"
              :search="search">
              <template v-slot:top>
                <v-toolbar flat class="mb-8">
                  <v-row>
                    <v-col cols="6" class="mr-auto">
                      <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('clinicManagement.Search Clinic')" filled
                        background-color="transparent" hide-details></v-text-field>
                    </v-col>
                    <v-col cols="auto">
                      <div>
                        <v-btn color="primary" nuxt to="/admin/profile/clinic-management/add-clinic">{{$t('clinicManagement.Add Clinic')}}</v-btn>
                        <v-btn color="primary" nuxt to="/admin/profile/clinic-management/join-clinic">{{$t('clinicManagement.Join Clinic')}}
                        </v-btn>
                      </div>
                    </v-col>
                  </v-row>
                </v-toolbar>
              </template>
              <template #item.company="{ item }">
                {{ item.company }} {{ item.isOwner ? `(${$t('clinicManagement.Owner')})` : '' }}
              </template>
              <template #item.joinedDatetime="{ item }">
                {{ datetime(item.joinedDatetime) }}
              </template>
              <template #item.action="{ item }">

                <v-menu v-if="item.isOwner" offset-y origin="center center" transition="scale-transition">
                  <template v-slot:activator="{ on, attrs }">

                    <v-btn v-bind="attrs" v-on="on" depressed icon fab dark color="primary" class="mr-0" small
                      title="Setting">
                      <v-icon>mdi-cog</v-icon>
                    </v-btn>
                  </template>

                  <v-list>
                    <v-list-item class="tw-cursor-pointer">
                      <v-list-item-title @click="editCompany(item)">
                        <v-icon>mdi-pencil</v-icon>
                        {{ $t('clinicManagement.Edit') }}
                      </v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
                <v-btn v-else @click="removeUserCompany(item)" depressed icon fab dark color="primary" class="mr-0"
                  small title="Delete">
                  <v-icon>mdi-close-circle-outline</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <ConfirmationDialog ref="confirmation" />
  </div>
</template>
<script lang="ts">
import {
  ref,
  defineComponent,
  useContext,
  useStore,
  computed,
  onMounted,
  useRouter,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useManageClinic from "~/../composables/useManageClinic";
import { groupType } from '~/types/companyUser'
import useMyInvitations from "~/../composables/useMyInvitations";
import useJoinClinic from "~/../composables/useJoinClinic";
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";


export default defineComponent({
  name: "ClinicManagement",
  middleware: "doctor",
  setup() {
    const { $t } = useNuxtTranslator()
    const { getters } = useStore();
    const { $dayjs, app } = useContext();
    const { $toast } = app;
    const router = useRouter();
    const { deleteUserCompany } = useManageClinic();
    const { fetchAuthUserCompanies, fetchRelatedCompaniesByAuthUser } = useJoinClinic();
    const { fetchUserLookup, } = useMyInvitations();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const manageFetchAllCompanies = async () => {
      const { approvalStatuses } = await fetchUserLookup();
      const status = approvalStatuses.find((item: groupType) => {
        return item.name === "Approve";
      });
      await fetchAuthUserCompanies({
        userId: Number(authUser.value?.id),
        groupName: "Doctor",
        statusId: Number(status.id),
        isOwner: true,
        approvalById: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      });
      await fetchRelatedCompaniesByAuthUser({
        userId: Number(authUser.value?.id),
        groupName: "Doctor",
        statusId: Number(status.id),
        isOwner: false,
        approvalById: null,
        langId: authUser.value?.lang?.id
      });
    };
    onMounted(() => {
      manageFetchAllCompanies();
    });
    const usersCompany = computed(() => getters["clinic/getAuthUserCompanies"]);
    const header = computed(() => {
      return [
        { text: `${$t("Clinic Name")}`, value: "company" },
        { text: `${$t("clinicManagement.Joined")}`, value: "joinedDatetime" },
        { text: `${$t("Actions")}`, value: "action", sortable: false, align: "center" },
      ]
    });
    const loading = ref(false);
    const search = ref("");
    const confirmation = ref();

    const datetime = (date: string) => {
      return $dayjs(date).format("DD/MM/YY");
    };

    const removeUserCompany = async (item: any) => {
      confirmation.value
        .open(`${$t("dialogue.Delete")}`, `${$t("dialogue.Do you want to delete?")}`, { color: 'red' })
        .then(async (res: boolean) => {
          if (res) {
            await deleteUserCompany(Number(item.id));
            $toast.success(`${ $t('toastMessage.Successfully deleted!') }`);
          }
          return false
        });
    };
    const editCompany = (item: any) => {
      router.push(`/admin/profile/clinic-management/add-clinic/?edit=${item.companyId}`);
    };

    return {
      loading,
      header,
      usersCompany,
      search,
      datetime,
      removeUserCompany,
      editCompany,
      confirmation,
    };
  },
  components: { ConfirmationDialog }
});
</script>

<style lang="scss">
.header-text{
  table thead th span{
    font-size: 0.85rem !important;
  }
}
</style>
