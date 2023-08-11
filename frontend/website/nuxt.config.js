import { resolve } from "path";
const DEV = process.env.NODE_ENV == "development";
const envPath = DEV ? "../../env.development" : "../../env.staging";
const graphQlOptions = { credentials: "include", mode: "cors" };
export default {
  head: {
    titleTemplate: "Oral e-Health Monitoring Platform",
    htmlAttrs: {
      lang: "en"
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "💎💎💎 The \"Oral e-Health Monitoring Platform\" aims to improve the oral health of the population by centralizing and articulating the medical-dental clinical record with its various stakeholders: patients, dentists, dental technicians and teaching/research centres." },
      { name: "format-detection", content: "telephone=no" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    "~/assets/tailwind.css",
    "~/assets/main.scss",
    "~/assets/vuetify/overrides.scss",
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    "~/plugins/vee-validate",
    "~/plugins/vue-bar",
    "~/plugins/vue-skycons.client",
    '~/plugins/directives',
    '~/plugins/v-chat-scroll.client',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    "@nuxt/typescript-build",
    "@nuxtjs/composition-api/module",
    "nuxt-graphql-request",
    "vue-toastification/nuxt",
    // https://go.nuxtjs.dev/vuetify
    "@nuxtjs/vuetify",
    "@nuxt/postcss8"
  ],
  env: require("dotenv").config({ path: envPath }).parsed,
  publicRuntimeConfig: {
    baseUrlWs: process.env.WS_CLIENT,
    apiClient: process.env.API_CLIENT,
    graphql: {
      clients: {
        default: {
          endpoint: `${process.env.API_CLIENT}/graphql`,
          options: graphQlOptions
        }
      },
      useFetchPolyfill: true,
      includeNodeModules: true
    }
  },
  privateRuntimeConfig: {
    baseUrlWs: process.env.WS_SERVER,
    graphql: {
      clients: {
        default: {
          endpoint: `${process.env.API_SERVER}/graphql`,
          options: graphQlOptions
        }
      },
      useFetchPolyfill: true,
      includeNodeModules: true
    }
  },
  graphql: {
    clients: {
      default: {
        endpoint: `${process.env.API_SERVER}/graphql`,
        options: graphQlOptions
      }
    },
    useFetchPolyfill: true,
    includeNodeModules: true
  },
  // Modules: https://go.nuxtjs.dev/config-modules
  modules: ["@nuxtjs/i18n", "@nuxtjs/dayjs", "cookie-universal-nuxt", "vue-toastification/nuxt"],

  // i18n module options
  i18n: {
    locales: [
      { name: 'Portuguese', code: 'pt', iso: 'pt-PT', file: 'pt-PT.js'},
      { name: 'English', code: 'en', iso: 'en-US', file: 'en-US.js'},
    ],
    defaultLocale: 'pt',
    skipSettingLocaleOnNavigate: true,
    strategy: 'no_prefix',
    lazy: true,
    langDir: '~/locales/',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root', 
    },
    vueI18n: {
      fallbackLocale: 'pt',
    }
  },

  dayjs: {
    locales: ["en"],
    defaultLocale: "en",
    plugins: ["relativeTime", "advancedFormat", "localizedFormat", "calendar", 'duration']
  },
  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    treeShake: true,
    customVariables: ["~/assets/variables.scss"],
    theme: {
      themes: {
        light: {
          primary: "#1e88e5",
          accent: "#fc4b6c",
          secondary: "#00544a",
          info: "#1e88e5",
          warning: "#F4944F",
          error: "#F44336",
          success: "#21c1d6",
          default: '#563dea'
        }
      }
    }
  },
  alias: {
    "@types": resolve(__dirname, "./types"),
    "@store": resolve(__dirname, "./store"),
    "@layouts": resolve(__dirname, "./layouts"),
    "@components": resolve(__dirname, "./components"),
    "@composables": resolve(__dirname, "./composables"),
    "@common-composables": resolve(__dirname, "..", "./composables"),
    "@common-components": resolve(__dirname, "..", "./components"),
    "@common-store": resolve(__dirname, "..", "./store")
  },
  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    transpile: ["vee-validate/dist/rules"],
    postcss: {
      plugins: {
        tailwindcss: {},
        autoprefixer: {},
      },
    },
  }
};
