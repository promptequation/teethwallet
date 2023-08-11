<template>
  <div>
    <nav>
      <v-tabs color="grey darken-3">
        <v-tab to="/admin/profile/info"> {{$t('profile.Info')}} </v-tab>
        <v-tab v-if="!isDoctor" to="/admin/profile/diseases"> {{$t('profile.Diseases')}} </v-tab>
        <v-tab to="/admin/profile/medication"> {{$t('profile.Medication')}} </v-tab>
        <v-tab v-can="isDoctor" to="/admin/profile/clinic-management">
          {{$t('profile.Clinic Management')}}
        </v-tab>
        <v-tab v-if="!isDoctor" to="/admin/profile/doctors"> {{$t('profile.Doctors')}} </v-tab>
        <v-tab v-if="!isDoctor" to="/admin/profile/access-management"> {{$t('profile.Access Management')}} </v-tab>
      </v-tabs>
    </nav>
    <NuxtChild />
  </div>
</template>
<script>
import { defineComponent } from "@nuxtjs/composition-api";
import useUser from "~/../composables/useUser";
export default defineComponent({
  layout: "admin",
  setup() {
    const { isDoctor } = useUser();
    return {
      isDoctor,
    };
  },
});
</script>
<style scoped>
</style>



