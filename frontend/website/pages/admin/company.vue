<template>
  <v-row>
    <v-col>
      <v-card>
        <v-card-title class="pa-6">
          <v-row>
            <v-col cols="auto" class="mr-auto">
              <v-icon large left>
                mdi-domain
              </v-icon>

              <span
                class="text-h6 blue-grey--text text--darken-3"
              >Company</span>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text>
          <v-card-title>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="search"
                  prepend-inner-icon="mdi-magnify"
                  placeholder="Search"
                  outlined
                />
              </v-col>

              <v-spacer />

              <v-col class="text-right">
                <v-menu
                  v-model="menu"
                  transition="slide-x-transition"
                  :close-on-content-click="false"
                  :min-width="400"
                  :offset-x="true"
                  left
                >
                  <template #activator="{ on, attrs }">
                    <v-btn
                      color="primary" dark v-bind="attrs"
                      v-on="on"
                    >
                      Add assistant
                    </v-btn>
                  </template>

                  <v-card class="pt-6 pl-6 pr-6">
                    <ValidationObserver v-slot="{ valid, dirty }">
                      <ValidationProvider v-slot="{ errors }" rules="email">
                        <v-text-field
                          v-model="email"
                          prepend-inner-icon="mdi-email"
                          placeholder="Fill the email"
                          :error-messages="errors"
                          outlined
                        >
                          <template v-if="valid && dirty" #append-outer>
                            <v-icon
                              large
                              color="primary"
                              style="margin-top:-12px"
                              @click="sendEmail"
                            >
                              mdi-send
                            </v-icon>
                          </template>
                        </v-text-field>
                      </ValidationProvider>
                    </ValidationObserver>
                  </v-card>
                </v-menu>
              </v-col>
            </v-row>
          </v-card-title>
          <!-- eslint-disable vue/no-deprecated-v-bind-sync vue/valid-v-slot-->
          <v-data-table
            :options.sync="options"
            :headers="headers"
            :items="assistants.items"
            :server-items-length="assistants.total"
            item-key="name"
            :footer-props="{
              'items-per-page-text': $t('Rows per page'),
              'items-per-page-all-text': $t('All')
            }"
            class="elevation-1 header-text"
          >
            <template #item.dateJoined="{ item }">
              {{ convertTimestampToFormat(item.dateJoined, "MMMM DD, YYYY") }}
            </template>
            <template #item.role>
              Assistant
            </template>
            <template #item.actions>
              <v-tooltip right>
                <template #activator="{ on, attrs }">
                  <v-btn
                    small color="info" v-bind="attrs"
                    v-on="on"
                  >
                    <v-icon small>
                      mdi-close
                    </v-icon>
                  </v-btn>
                </template>

                <span>Remove access</span>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-card-text>
        <v-overlay :absolute="true" :value="menu" />
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import { watch } from "@vue/composition-api";
import { ref } from "@nuxtjs/composition-api";
import useAssistant from "@composables/useAssistant";
import useDate from "@common-composables/useDate";
export default {
  components: {
    ValidationObserver,
    ValidationProvider
  },
  layout: "admin",
  setup({}, {}) {
    const {
      fetchAssistantsByCompanyId,
      sendAssistantEmailInvitation,
      assistants
    } = useAssistant();
    const { convertTimestampToFormat } = useDate();

    const email = ref([]);
    const search = ref([]);
    const options = ref({});
    const menu = ref(false);

    const headers = [
      { text: "Name", align: "start", sortable: false, value: "name" },
      { text: "Role", align: "start", sortable: false, value: "role" },
      { text: "Join Date", align: "start", value: "dateJoined" },
      { text: "Actions", value: "actions", sortable: false }
    ];

    watch(
      () => options.value,
      () => fetchAssistantsByCompanyId(options.value),
      { deep: true }
    );

    watch(
      () => search.value,
      newValue => {
        fetchAssistantsByCompanyId({ ...options.value, name: newValue });
      },
      { deep: true }
    );

    const sendEmail = async () => {
      await sendAssistantEmailInvitation(email.value);
    };

    return {
      sendEmail,
      convertTimestampToFormat,
      menu,
      email,
      search,
      assistants,
      headers,
      options
    };
  },
  computed: {}
};
</script>
