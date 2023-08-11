<template>
  <v-sheet rounded="lg" class="mb-6 mt-3">
    <v-card>
      <v-card-title
        class="text-h4 blue-grey--text text--darken-4 ml-3 "
        v-text="currentPage.title"
      />
      <v-container>
        <v-row class="ml-1 mb-1">
          <v-col cols="6" align-self="end">
            <div class="grey--text caption">
              <v-avatar size="25">
                <img :src="currentPage.author.image" alt="author">
              </v-avatar>
              {{ currentPage.author.name }}
            </div>
          </v-col>

          <v-col cols="6" align-self="center">
            <div class="grey--text caption">
              <v-icon small class="mb-1">
                mdi-clock-outline
              </v-icon>
              {{
                convertTimestampToFormat(currentPage.pubDate, "MMMM DD, YYYY")
              }}
            </div>
          </v-col>
        </v-row>

        <v-divider class="mx-4" />

        <v-card-text>
          <vue-markdown v-if="currentPage.body">
            {{ currentPage.body }}
          </vue-markdown>
        </v-card-text>
      </v-container>

      <v-btn
        color="primary"
        outlined
        class="pt-6 pb-6 fill ma-6 "
        nuxt
        to="/blog"
      >
        <v-icon dark>
          mdi-arrow-left
        </v-icon>
        Back
      </v-btn>
    </v-card>
  </v-sheet>
</template>
<script>
import VueMarkdown from "vue-markdown";

import {
  useRoute,
  computed,
  ssrRef,
  onBeforeMount
} from "@nuxtjs/composition-api";

import useDate from "@common-composables/useDate";
import useBlog from "@common-composables/useBlog";

export default {
  key(route) {
    return route.fullPath;
  },
  components: {
    VueMarkdown
  },
  layout: "website",
  setup() {
    const currentPage = ssrRef({ author: {} });

    const route = useRoute();
    const { fetchPage } = useBlog();
    const { convertTimestampToFormat } = useDate();

    const id = computed(() => route.value.params.id);

    onBeforeMount(async () => {
      currentPage.value = await fetchPage(parseInt(id.value));
    });

    return {
      convertTimestampToFormat,
      currentPage
    };
  }
};
</script>
