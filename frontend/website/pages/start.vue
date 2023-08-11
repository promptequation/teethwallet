<template>
  <div class="landing-page-background tw-mb-20">
    <v-container>
        <v-row>
          <v-col offset-lg="1" offset-xl="2" lg="10" xl="8" md="12" sm="12">
            <v-card>
    <v-window v-model="step">
      <v-window-item value="login">
        <v-row>
          <v-col cols="12" md="8">
            <v-card-text class="pa-15">
              <h1 class="text-center display-2 primary--text pb-6">
                {{$t('start.Log in')}}
              </h1>
              <ValidationObserver v-slot="{ handleSubmit }">
                <v-form @submit.prevent="handleSubmit(handleLogin)">
                  <ValidationProvider v-slot="{ errors }" rules="required">
                    <v-text-field v-model="form.username" :error-messages="errors" :label="$t('Username')" name="Username"
                      prepend-icon="mdi-account" type="text" color="primary" />
                  </ValidationProvider>

                  <ValidationProvider v-slot="{ errors }" rules="required">
                    <v-text-field id="password" v-model="form.password" :error-messages="errors" :label="$t('start.Password')"
                      name="password" prepend-icon="mdi-lock" type="password" color="primary" />
                  </ValidationProvider>

                  <div class="text-center mt-6 mb-6">
                    <v-btn class="custom-height" type="submit" color="primary" dark>
                      {{$t('start.Log in')}}
                    </v-btn>
                  </div>
                </v-form>
              </ValidationObserver>
              <!-- <h3 class="text-center">
                Forgot your password ?
              </h3> -->
            </v-card-text>
          </v-col>
          <v-col cols="12" md="4" style="background: linear-gradient(#29589c, #64B5F6);">
            <v-card-text class="white--text mt-12">
              <h1 class="text-center display-1">
                {{$t('start.Hello, Friend!')}}
              </h1>
              <h5 class="text-center">
                {{$t('start.Enter your personal details and start journey with us')}}
              </h5>
            </v-card-text>
            <div class="text-center">
              <v-btn outlined dark @click="changeWindow">
                {{$t('start.Create a new account')}}
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-window-item>
      <v-window-item value="register">
        <v-row class="fill-height">
          <v-col cols="12" md="4" style="background: linear-gradient(#29589c, #64B5F6);">
            <v-card-text class="white--text mt-12">
              <h1 class="text-center display-1">
                {{$t('start.Welcome Back!')}}
              </h1>
              <h5 class="text-center">
                {{$t('start.To Keep connected with us please login with your personnel info')}}
              </h5>
            </v-card-text>
            <div class="text-center">
              <v-btn outlined dark @click="changeWindow">
                {{$t('start.Log in')}}
              </v-btn>
            </div>
          </v-col>

          <v-col cols="12" md="8">
            <v-card-text class="pa-15">
              <h1 class="text-center display-2 primary--text text--">
                {{$t('start.Create Account')}}
              </h1>
              <v-window v-model="registerStep">
                <v-form>
                  <v-window-item value="step1">
                    <ValidationObserver v-slot="{ handleSubmit, invalid }">
                      <ValidationProvider v-slot="{ errors }" rules="required|email">
                        <v-text-field v-model="form.email" :error-messages="errors" :label="$t('Email')" name="Email"
                          prepend-icon="mdi-email" type="text" color="primary" />
                      </ValidationProvider>

                      <ValidationProvider v-slot="{ errors }" rules="required|alpha_num" name="username">
                        <v-text-field v-model="form.username" :error-messages="errors" :label="$t('Username')" name="username"
                          prepend-icon="mdi-account" type="text" color="primary" />
                      </ValidationProvider>

                      <ValidationProvider v-slot="{ errors }" rules="required|alpha_spaces">
                        <v-text-field v-model="form.firstName" :error-messages="errors" :label="$t('First Name')"
                          name="FirstName" prepend-icon="mdi-account" type="text" color="primary" />
                      </ValidationProvider>

                      <ValidationProvider v-slot="{ errors }" rules="required|alpha_spaces">
                        <v-text-field v-model="form.lastName" :error-messages="errors" :label="$t('Last Name')" name="LastName"
                          prepend-icon="mdi-account" type="text" color="primary" />
                      </ValidationProvider>

                      <ValidationProvider v-slot="{ errors }" rules="required">
                        <v-text-field id="password" v-model="form.password" :error-messages="errors" :label="$t('start.Password')"
                          name="password" prepend-icon="mdi-lock" type="password" color="primary" />
                      </ValidationProvider>

                      <ValidationProvider v-slot="{ errors }" rules="required">
                        <v-menu ref="menu" v-model="menu" :close-on-content-click="false" transition="scale-transition"
                          offset-y min-width="auto">
                          <template v-slot:activator="{ on, attrs }">
                            <ValidationProvider v-slot="{ errors }" rules="required">
                              <v-text-field title="Birthday date" v-model="form.birthdate" :error-messages="errors"
                                clearable :placeholder="$t('Birthday date')" prepend-icon="mdi-calendar" readonly
                                v-bind="attrs" v-on="on" @click:clear="form.birthdate = null" />
                            </ValidationProvider>
                          </template>
                          <ValidationProvider v-slot="{ errors }" rules="required">
                            <v-date-picker v-model="form.birthdate" :active-picker.sync="activePicker"
                              :max="(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
                              min="1910-01-01" @change="saveDate" />
                          </ValidationProvider>
                        </v-menu>
                      </ValidationProvider>
                      <div class="text-center mt-6">
                        <v-btn :disabled="invalid" @click="changeRegisterWindow" color="primary" dark>
                          {{$t('start.PROCEED')}}
                        </v-btn>
                      </div>
                    </ValidationObserver>
                  </v-window-item>
                  <v-window-item value="step2">
                    <ValidationObserver v-slot="{ handleSubmit, invalid }">
                      <ValidationProvider v-slot="{ errors }" rules="required">
                        <v-text-field v-model="form.address" :error-messages="errors" :label="$t('start.Address')" name="address"
                          prepend-icon="mdi-map-marker" type="text" color="primary" />
                      </ValidationProvider>
                      <ValidationProvider v-slot="{ errors }" rules="required">
                        <v-select v-model="form.country" :error-messages="errors" :items="signupFieldsData.countryList"
                          item-value="code" item-text="name" :label="$t('Country')" name="country" prepend-icon="mdi-earth"
                          type="text" color="primary" />
                      </ValidationProvider>
                      <ValidationProvider v-slot="{ errors }" rules="required">
                        <v-select v-model="form.nationality" :error-messages="errors"
                          :items="signupFieldsData.nationalityList" item-value="code" item-text="name"
                          :label="$t('start.Nationality')" name="nationality" prepend-icon="mdi-passport" type="text"
                          color="primary" />
                      </ValidationProvider>
                      <ValidationProvider v-slot="{ errors }" rules="required">
                        <v-select v-model="form.language" :error-messages="errors"
                          :items="signupFieldsData.multiLanguage" item-value="id" item-text="name" :label="$t('Language')"
                         prepend-icon="mdi-translate" type="text" color="primary" />
                      </ValidationProvider>
                      <div class="text-center mt-6">
                        <v-btn :disabled="invalid" @click="handleSubmit(handleRegister)" color="primary" dark>
                          {{ $t('start.SIGN UP') }}
                        </v-btn>
                      </div>
                    </ValidationObserver>
                  </v-window-item>
                </v-form>
              </v-window>
            </v-card-text>
          </v-col>
        </v-row>
      </v-window-item>
    </v-window>
  </v-card>
          </v-col>
        </v-row>
      </v-container>
  </div>
  
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import { defineComponent, ref } from "@nuxtjs/composition-api";
import { POSITION } from 'vue-toastification';
import { provideToast } from "vue-toastification/composition";

import useAuth from "../../composables/useAuth";
import useCountry from "../composables/useCountry";

export default defineComponent({
  components: {
    ValidationObserver,
    ValidationProvider
  },
  setup({ }, { root }) {
    provideToast({ timeout: 4000, position: POSITION.BOTTOM_CENTER });

    const activePicker = '';
    const date = null;
    const menu = false;

    const { signUp, signIn, form, resetForm, step, registerStep } = useAuth();

    const { signupFieldsData, getSignupFieldsData } = useCountry();

    getSignupFieldsData();


    const handleSubmit = async (fn) => {
      await fn(form);
    };

    const handleRegister = () => handleSubmit(signUp);

    const handleLogin = () => handleSubmit(signIn);
    const changeWindow = () => {
      step.value = step.value === "login" ? "register" : "login";
      resetForm();
    };
    const changeRegisterWindow = () => {
      registerStep.value = registerStep.value === "step1" ? "step2" : "step1";
    };

    return {
      handleRegister,
      handleLogin,
      changeWindow,
      step,
      form,
      activePicker,
      date,
      menu,
      registerStep,
      changeRegisterWindow,
      signupFieldsData,
    };
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
  },
  methods: {
    saveDate(date) {
        if (this.$refs.menu) {
            this.$refs.menu.save(date)
        }
    },
  },

});
</script>

<style>
.custom-height{
  height: 38px!important;
}
</style>
