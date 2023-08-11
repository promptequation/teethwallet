<template>
  <q-page class="column justify-center items-center" style="background: linear-gradient(#64b5f6, #29589c)">
    <q-card square class="shadow-24 q-pa-lg" style="width: 90vw">
      <q-card-section class="text-center">
        <logo font-size="2" />
      </q-card-section>
      <LoginForm :validation-schema="validationSchema" @submit="handleSubmit">
        <q-card-section>
          <Field v-slot="{ errorMessage, value, field }" name="username">
            <q-input v-model="form.username" :model-value="value" v-bind="field" :error-message="errorMessage"
              :error="!!errorMessage" type="text" label="Username" class="q-pb-md" color="accent">
              <template #prepend>
                <q-icon name="person" />
              </template>
            </q-input>
          </Field>

          <Field v-slot="{ errorMessage, value, field }" name="password">
            <q-input v-model="form.password" :model-value="value" v-bind="field" :error-message="errorMessage"
              :error="!!errorMessage" :type="showPassword ? 'text' : 'password'" label="Password" color="accent">
              <template #prepend>
                <q-icon name="lock" />
              </template>
              <template #append>
                <q-icon :name="showPassword ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                  @click="showPassword = !showPassword" />
              </template>
            </q-input>
          </Field>
        </q-card-section>

        <q-card-actions class="q-pb-md">
          <q-btn type="submit" size="md" color="primary" class="full-width" label="Sign In" :loading="loading"></q-btn>
        </q-card-actions>
      </LoginForm>
      <!-- <q-card-section class="text-center q-pb-md">
        <p class="text-grey-7">
          Forgot your password?
        </p>
      </q-card-section> -->
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { Field, Form } from 'vee-validate'
import * as yup from 'yup'
import { useAuth } from 'src/composables'
import Logo from 'src/components/Logo.vue'

export default defineComponent({
  name: 'IndexPage',

  components: {
    Field,
    LoginForm: Form,
    Logo,
  },

  setup() {
    const isLogin = ref(true);
    const showPassword = ref(false);

    const schema = computed(() => {
      const base = {
        username: yup.string().required(),
        password: yup.string().required(),
      };
      if (!isLogin.value)
        return { email: yup.string().email().required(), ...base };

      return base;
    });

    const validationSchema = computed(() => yup.object(schema.value));

    const { signIn, form, loading } = useAuth();

    const handleSubmit = async () => {
      if (isLogin.value) {
        const { username, password } = form
        await signIn(username, password)
      }
    };

    const toggleLoginLogout = () => (isLogin.value = !isLogin.value);

    return {
      handleSubmit,
      validationSchema,
      isLogin,
      toggleLoginLogout,
      form,
      showPassword,
      loading,
    };
  },
});
</script>
