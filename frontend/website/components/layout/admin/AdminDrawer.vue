<template>
  <v-navigation-drawer
    v-model="drawer" color="white" fixed
    app
  >
    <v-list-item class="mt-3 pb-3">
      <logo />
    </v-list-item>

    <v-select
      v-model="selectedProfile"
      class="ma-5 pb-1"
      :items="profileOptions"
      :prefix="isDoctor ? 'Doctor: ' : 'Patient: '"
      item-text="name"
      item-value="id"
      return-object
      label="Perspective"
      color="accent"
      item-color="accent"
    />

    <v-list class="pa-3" max-width="97%">
      <v-subheader>App</v-subheader>
      <v-list-item-group color="accent">
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          nuxt
          exact
          :to="item.to"
        >
          <v-list-item-icon>
            <v-icon v-text="item.icon" />
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import { mapFields } from "vuex-map-fields";
import { reactive } from "@vue/composition-api";
import useUser from "@common-composables/useUser";
export default {
  components: {
    Logo: () => import("@common-components/Logo.vue")
  },
  setup() {
    const { profileOptions, isDoctor } = useUser();

    const items = reactive([
      { icon: "mdi-home", title: "Start", to: "/admin" },
      { icon: "mdi-email", title: "Messages", to: "/admin/messages" },
      { icon: "mdi-history", title: "History", to: "/admin/history" },
      {
        icon: "mdi-calendar-month",
        title: "Appointments",
        to: "/admin/appointments"
      },
      { icon: "mdi-bell", title: "Alerts", to: "/admin/alerts" }
    ]);

    return {
      items,
      profileOptions,
      isDoctor
    };
  },
  computed: {
    ...mapFields("layout", ["drawer"]),
    ...mapFields("auth", ["selectedProfile"])
  }
};
</script>
