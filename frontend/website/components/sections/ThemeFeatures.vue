<template>
  <base-section id="app-features">
    <base-section-heading :title="$t('themeFeature.appServices')">
      {{$t('themeFeature.clinicalDentalData')}}
    </base-section-heading>

    <v-container>
      <v-row>
        <v-col
          v-for="(feature, i) in features"
          :key="i"
          cols="12"
          md="6"
        >
          <base-avatar-card
            v-bind="feature"
            align="left"
            horizontal
          >
          {{ feature.description }} 
          </base-avatar-card>
        </v-col>
      </v-row>
    </v-container>
  </base-section>
</template>

<script>

export default {
  name: 'SectionThemeFeatures',
  data: () => ({
    features: [
      {
        color: 'accent',
        dark: true,
        title: 'All your oral health history',
        description: 'Manage your dental history with a functional and concise organization.',
        icon: 'health-report.png',
      },
      {
        color: 'accent',
        dark: true,
        title: 'Health score',
        description: 'Risk assessment calculated by professionals.',
        icon: 'word-of-mouth.png',
      },
      {
        color: 'primary',
        dark: true,
        title: 'Chat with your doctors',
        description: 'Real-time access to your oral health care provider: message board with free and open communication.',
        icon: 'chat.png',
      },
      {
        color: 'primary',
        dark: true,
        title: 'Manage your appointments',
        description: 'Your oral health will no longer stay behind with our alarmistic system.',
        icon: 'calendar.png',
      },
    ],
  }),
}
</script>
