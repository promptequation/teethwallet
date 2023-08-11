<template>
  <v-menu
    bottom min-width="200px" rounded
    offset-y
  >
    <template #activator="{ on }">
      <v-btn icon x-large v-on="on">
        <v-avatar>
          <img :src="userProfile.avatar" @error="$event.target.src = '/avatar.jpeg'" alt="">
        </v-avatar>
      </v-btn>
    </template>
    <v-card>
      <v-list-item-content class="justify-center">
        <div class="mx-auto text-center">
          <div class="mb-2">
            {{ userProfile.firstName }}
          </div>
          <p class=" grey--text text-caption mt-1">
            {{ userProfile.email }}
          </p>
          <v-divider class="my-3" />

          <v-list class="font-weight-light" dense>
            <v-list-item-group color="info">
              <v-list-item to="/admin/profile/info" nuxt>
                <v-list-item-icon>
                  <v-icon>
                    mdi-account
                  </v-icon>
                </v-list-item-icon>
                <v-list-item-title>Profile</v-list-item-title>
              </v-list-item>

              <v-list-item v-if="isCompanyOwner" to="/admin/company" nuxt>
                <v-list-item-icon>
                  <v-icon>
                    mdi-domain
                  </v-icon>
                </v-list-item-icon>
                <v-list-item-title>Company</v-list-item-title>
              </v-list-item>

              <v-list-item @click="logout">
                <v-list-item-icon>
                  <v-icon>
                    mdi-exit-to-app
                  </v-icon>
                </v-list-item-icon>
                <v-list-item-title>Logout</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </div>
      </v-list-item-content>
    </v-card>
  </v-menu>
</template>
<script>
import useAuth from "@common-composables/useAuth";
import useUser from "@common-composables/useUser";
import { computed, reactive, ref } from "@nuxtjs/composition-api";
import { useToast } from "vue-toastification/composition";
export default {
  setup({}, { root }) {
    const redirect = {
      logout: "/start"
    };
    const { logout } = useAuth(
      root.$store,
      root.$router,
      ref,
      reactive,
      useToast,
      redirect
    );
    const { userProfile } = useUser();

    const isCompanyOwner = computed(
      () => userProfile?.doctor?.isCompanyOwner || false
    );

    return {
      isCompanyOwner,
      logout,
      userProfile
    };
  }
};
</script>
