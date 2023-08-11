<template>
  <v-sheet rounded="lg">
    <v-card>
      <v-row>
        <v-col class="padding-all">
          <v-img
            src="contact-us.jpg"
            contain
            max-width="500"
            max-height="595"
          />
        </v-col>

        <v-col>
          <v-form class="pr-6">
            <div class="text-h5 mb-6 mt-5 font-weight-bold text-underline">
              {{$t('contactUs.mailUs')}}
            </div>
            <v-row no-gutters>
              <v-col cols="12">
                <v-text-field
                  v-model="name"
                  :placeholder="$t('contactUs.name')"
                  outlined
                />
              </v-col>
            </v-row>

            <v-row no-gutters>
              <v-col cols="12">
                <v-text-field
                  v-model="email"
                  :placeholder="$t('contactUs.email')"
                  outlined
                />
              </v-col>
            </v-row>

            <v-row no-gutters>
              <v-col cols="12">
                <v-text-field
                  v-model="subject"
                  :placeholder="$t('contactUs.subject')"
                  outlined
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col cols="12">
                <v-textarea
                  v-model="body"
                  :placeholder="$t('contactUs.description')"
                  outlined
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <v-btn
                  color="primary"
                  outlined
                  class="pt-6 pb-6 fill"
                >
                  {{$t('contactUs.sendMessage')}}
                  <v-icon
                    dark
                    class="pl-3"
                  >
                    mdi-send
                  </v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </v-card>
  </v-sheet>
</template>

<script>
export default {
  name: 'ContactUs',
  data: () => ({
    name: '',
    email: '',
    subject: '',
    body: ''
  })
}
</script>
<style lang="scss" scoped>
 .padding-all{
  padding: 11px !important;
 }
</style>
