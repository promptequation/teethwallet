<template>
  <v-app id="inspire">
    <Header v-model="expandOnHover"></Header>

    <v-main>
      <v-container fluid class="page-wrapper">
        <Nuxt />
      </v-container>
    </v-main>
    <Sidebar :expand-on-hover.sync="expandOnHover"></Sidebar>
    <Footer></Footer>

    <v-overlay :value="showingOverlay"></v-overlay>
    <v-dialog v-model="showingLoading" hide-overlay persistent width="600">
      <v-card color="primary" dark>
        <v-card-text>
          Please wait...
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import Header from "~/components/layout/admin/elements/Header.vue";
import Sidebar from "~/components/layout/admin/elements/Sidebar";
import Footer from "~/components/layout/admin/elements/Footer";
import { useStore, defineComponent, computed, } from "@nuxtjs/composition-api";

export default defineComponent({
  name: "Layout",
  middleware: ["authenticated"],
  components: {
    Header,
    Sidebar,
    Footer,
  },
  props: {
    source: String,
  },
  data: () => ({
    expandOnHover: true,
    dialog: true,
  }),

  setup() {
    const { state } = useStore()

    const showingOverlay = computed(() => {
      return state.showOverlay
    })

    const showingLoading = computed(() => {
      return state.loading
    })

    return {
      showingOverlay,
      showingLoading,
    }
  }

});
</script>
