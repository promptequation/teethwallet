<template>
  <div>
    <v-sheet
      v-for="(page, index) in pages"
      :key="index"
      rounded="lg"
      class="mb-3"
    >
      <v-card height="375" hover class="d-flex flex-column">
        <v-row>
          <v-col>
            <v-img
              contain :src="page.image" max-height="375"
              max-width="475"
            />
          </v-col>
          <v-col>
            <v-card-title
              class="text-h4 mb-2 blue-grey--text text--darken-4"
              v-text="page.title"
            />

            <v-card-subtitle
              class="blue-grey--text text--darken-2"
              v-text="page.subtitle"
            />

            <v-card-text>
              <v-chip
                v-for="(tag, indexSub) in page.tags"
                :key="indexSub"
                small
                class="mr-1"
              >
                {{ tag.name }}
              </v-chip>
            </v-card-text>

            <v-container class="grey lighten-5">
              <v-row class="ml-2 bottom row">
                <v-row class="row">
                  <v-col cols="6" align-self="end">
                    <div class="grey--text caption">
                      <v-avatar size="25">
                        <img :src="page.author.image" alt="author">
                      </v-avatar>
                      {{ page.author.name }}
                    </div>
                  </v-col>

                  <v-col cols="6" align-self="center">
                    <div class="grey--text caption">
                      <v-icon small class="mb-1">
                        mdi-clock-outline
                      </v-icon>
                      {{
                        convertTimestampToFormat(page.pubDate, "MMMM DD, YYYY")
                      }}
                    </div>
                  </v-col>
                  <v-col>
                    <v-btn
                      color="primary"
                      outlined
                      class="pt-6 pb-6 fill mb-6"
                      nuxt
                      :to="`blog/${page.id}`"
                    >
                      Read Article
                      <v-icon right dark>
                        mdi-arrow-right
                      </v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </v-card>
    </v-sheet>
  </div>
</template>

<script>
import { mapFields } from "vuex-map-fields";
import useDate from "@common-composables/useDate";
import useBlog from "@common-composables/useBlog";

export default {
  layout: "website",
  setup() {
    const { convertTimestampToFormat } = useDate();

    const { fetchAllPages } = useBlog();

    fetchAllPages();

    return {
      convertTimestampToFormat
    };
  },
  computed: {
    ...mapFields("website", ["pages"])
  }
};
</script>

<style lang="scss" scoped></style>
