<template>
  <v-app-bar
    color="white" flat fixed
    app
  >
    <v-app-bar-nav-icon @click.stop="drawer = !drawer" />

    <v-spacer />

    <admin-menu />
  </v-app-bar>
</template>
<script>
import { mapFields } from "vuex-map-fields";

export default {
  components: {
    AdminMenu: () => import("./AdminMenu")
  },
  computed: {
    ...mapFields("layout", ["drawer"])
  }
};
</script>
