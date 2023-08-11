import { extend, ValidationObserver, ValidationProvider } from 'vee-validate';
import { required, email, alpha_spaces, alpha_num } from "vee-validate/dist/rules";
import Vue from 'vue';
Vue.component('validation-observer', ValidationObserver);
Vue.component('validation-provider', ValidationProvider);

extend("required", {
    ...required,
    message: "This field is required."
});

extend('email', {
    ...email,
    message: 'Invalid email.'
});

extend('alpha_spaces', {
    ...alpha_spaces,
    message: 'The field field may only contain alphabetic characters.'
});
extend('alpha_num', {
    ...alpha_num,
    message: 'The {_field_} field may only contain alpha-numeric characters.'
});