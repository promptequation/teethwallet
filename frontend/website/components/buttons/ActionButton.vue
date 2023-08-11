<template>
  <v-card-actions>
    <v-btn type="submit" dark color="green" @click="$emit('click:save')">
      {{$t('actionButtons.Save')}}
    </v-btn>
    <v-btn  color="warning" @click="$emit('click:discard')">
      {{$t('actionButtons.Discard')}}
    </v-btn>
    <v-btn v-if="deleteBtn" color="error" @click="$emit('click:delete')"> {{$t('actionButtons.Delete')}} </v-btn>
    <v-btn v-if="resetBtn" color="primary" @click="$emit('click:reset')"> {{$t('actionButtons.Reset All')}} </v-btn>
  </v-card-actions>
</template>

<script>
export default {
  name: "ActionButton",
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "Submit",
    },
    deleteBtn: {
      type: Boolean,
      default: true
    },
    resetBtn: {
      type: Boolean,
      default: false
    }
  },
};
</script>
