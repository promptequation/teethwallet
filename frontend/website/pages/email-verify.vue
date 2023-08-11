<template>
  <v-container class="h-100">
    <v-row class="h-100" justify="center" align="center">
      <v-col cols="12" sm="6" md="6">
        <v-card class="elevation-2 pa-3" min-height="300">
          <v-card-title class="justify-center">
            Email Confirmation
          </v-card-title>
          <v-divider />
          <v-card-text>
            <template v-if="success">
              <v-alert :value="true" type="success">
                {{ message }}
              </v-alert>
              <v-btn nuxt to="/start" block class="primary">
                Log In
              </v-btn>
            </template>
            <template v-else>
              <v-alert :value="true" type="error">
                {{ message }}
              </v-alert>
              <!-- <v-btn nuxt to="/auth/resent-email" block class="primary">
                Resent Confirmation Link
              </v-btn> -->
            </template>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { reactive, ref, useRoute } from "@nuxtjs/composition-api";
import { useToast, provideToast } from "vue-toastification/composition";
import useAuth from "@common-composables/useAuth";

export default {
  name: "EmailVerify",
  setup({}, { root }) {
    provideToast({ timeout: 4000, position: "bottom-center" });
    const redirect = {
      login: "/admin",
    };

    const route = useRoute();
    const success = ref(false);
    const message = ref("Something is Wrong please try again!");

    const { emailVerify } = useAuth(
      root.$store,
      root.$router,
      ref,
      reactive,
      useToast(),
      redirect
    );

    if (route.value.query) {
      const token = route.value.query.token;
      const uuid = route.value.query.uuid;
      try {
        emailVerify({
          token,
          uuid,
        });
        success.value = true;
        message.value = 'Successfully email verifed'
      } catch (e) {
        success.value = false;
      }
    }

    return {
      success,
      message,
    };
  },
};
</script>
