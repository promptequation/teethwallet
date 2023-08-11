<template>
  <v-container fluid class="down-top-padding">
    <v-card class="mb-7">
      <v-card-text class="pa-5">
        <v-row justify="space-between">
          <v-col cols="12" lg="4">
            <v-text-field
              prepend-inner-icon="mdi-magnify"
              label="Search Clinics"
              filled
              background-color="transparent"
              hide-details
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-row>
      <v-col
        cols="12"
        sm="6"
        lg="4"
        v-for="(clinic, index) in clinics"
        :key="index"
      >
        <v-card
          class="mb-7 tw-flex tw-flex-col tw-justify-between"
          height="100%"
        >
          <v-card-text class="text-center pa-5 tw-flex-1">
            <div class="tw-h-28 tw-w-28 tw-mx-auto">
              <img
                :src="clinic.image"
                alt="user"
                class="rounded-circle tw-h-full"
              />
            </div>

            <h4 class="mt-3 mb-0 title">{{ clinic.clinicName }}</h4>
            <small class="subtitle-2 font-weight-regular">{{
              clinic.ownerName
            }}</small>
            <div class="mt-3">
              <v-btn depressed small color="primary" class="mr-2"
                >Send Access Request</v-btn
              >
            </div>
            <div class="pt-3 mt-3">
              <address class="subtitle-2 font-weight-regular">
                {{ clinic.address }}
              </address>
            </div>
          </v-card-text>

          <div class="text-center pa-3 blue lighten-4">
            <i class="mr-2 mdi mdi-cellphone-iphone"></i>
            {{ clinic.phone }}
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { ref, defineComponent } from "@nuxtjs/composition-api";
export default defineComponent({
  layout: "admin",
  setup() {
    const clinics = ref([
      {
        phone: "(123) 456 789",
        image:
          "https://my.clevelandclinic.org/-/scassets/images/org/promo-panels/health-essentials-podcast-promo.jpg?h=560&la=en&w=620&hash=58C2A33B152A18D43B52802EF13A04E539197C85",
        clinicName: "Hanna Gover",
        ownerName: "Owner Name",
        address: " 2289 5th Ave, Suite 600 San Francisco New York, NY, 10037 ",
      },
      {
        phone: "(234) 456 789",
        image:
          "https://www.myhealth.ph/wp-content/uploads/2019/08/alabang-1.jpg",
        clinicName: "Daniel Kristeen",
        ownerName: "Owner Name",
        address: " 55 E 11th St #1OTH, Suite 600 New York, NY, 10003 ",
      },
    ]);

    return {
      clinics,
    };
  },
});
</script>
