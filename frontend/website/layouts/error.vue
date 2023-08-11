<template>
  <v-card class="pt-16">
    <v-row justify="center">
      <div v-if="error.statusCode === 404">
        <v-img
          src="search.png"
          width="256"
        />
        <h1 class="ml-16">
          {{ pageNotFound }}
        </h1>
      </div>
      <h1 v-else>
        {{ otherError }}
      </h1>
      <NuxtLink to="/">
        Go to Start
      </NuxtLink>
    </v-row>
  </v-card>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      pageNotFound: 'Oops!',
      otherError: 'An error occurred'
    }
  },
  head () {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
