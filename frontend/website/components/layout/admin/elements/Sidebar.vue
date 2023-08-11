<template>
    <v-navigation-drawer
        v-model="Sidebar_drawer"
        :dark="SidebarColor !== 'white'"
        :color="SidebarColor"
        mobile-breakpoint="960"
        clipped
        :right="$vuetify.rtl"
        mini-variant-width="70"
        :expand-on-hover="!expandOnHover"
        app
        id="main-sidebar"
    >
        <!---USer Area -->
        <v-list-item two-line class="profile-bg justify-start">
            <v-list-item-avatar>
                <v-img v-if="authUser.avatar" :src="authUser.avatar" />
                <span v-else class="white--text text-h6">
                    <v-avatar color="grey custom-margin" size="40">
                        {{ setAvatarLetter }}
                    </v-avatar>
                </span>
            </v-list-item-avatar>

            <v-list-item-content class="white--text">
                <v-list-item-title
                    >{{ authUser.firstName || authUser.username }}
                </v-list-item-title>
            </v-list-item-content>
        </v-list-item>
        <!---USer Area -->

        <v-list expand nav class="mt-1">
            <template v-for="(item, i) in items">
                <!---If Sidebar Caption -->
                <v-row v-if="item.header" :key="item.header" align="center">
                    <v-col cols="12">
                        <v-subheader
                            v-if="item.header"
                            class="d-block text-truncate"
                            >{{ item.header }}
                        </v-subheader>
                    </v-col>
                </v-row>
                <!---If Sidebar Caption -->
                <BaseItemGroup
                    v-else-if="item.children"
                    :key="`group-${i}`"
                    :item="item"
                ></BaseItemGroup>

                <template v-else>
                    <BaseItem :key="`item-${i}`" :item="item" />
                </template>
            </template>

            <!---Sidebar Items -->
        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { mapState } from "vuex";
import useNuxtTranslator from "~/../composables/useNuxti18n";

import {
    useStore,
    computed,
    defineComponent,
    ref,
    watch,
    useContext
} from "@nuxtjs/composition-api";
import useUser from "~/../composables/useUser";

export default defineComponent({
    name: "Sidebar",
    props: {
        expandOnHover: {
            type: Boolean,
            default: false
        }
    },
    setup() {
        const { $t } = useNuxtTranslator();
        const { getters } = useStore();
        const authUser = computed(() => getters["auth/getUserProfile"]);
        const { isDoctor } = useUser();
        const items = computed(() => {
            if (isDoctor.value) {
                return [
                    {
                        icon: "mdi-home",
                        title: `${$t("sidebar.Start")}`,
                        to: "/admin"
                    },
                    {
                        icon: "mdi-email",
                        title: `${$t("sidebar.Messages")}`,
                        to: "/admin/messages"
                    },
                    {
                        icon: "mdi-calendar-month",
                        title: `${$t("sidebar.Appointments")}`,
                        to: "/admin/appointments"
                    },
                    {
                        icon: "mdi-account",
                        title: `${$t("sidebar.My Patients")}`,
                        to: "/admin/patients"
                    },
                    {
                        icon: "mdi-bell",
                        title: `${$t("sidebar.Alerts")}`,
                        to: "/admin/alerts"
                    },
                    {
                        icon: "mdi-account-multiple-plus",
                        title: `${$t("sidebar.My Invitations")}`,
                        to: "/admin/patient-invitations"
                    }
                ];
            } else {
                return [
                    {
                        icon: "mdi-home",
                        title: `${$t("sidebar.Start")}`,
                        to: "/admin"
                    },
                    {
                        icon: "mdi-email",
                        title: `${$t("sidebar.Messages")}`,
                        to: "/admin/messages"
                    },
                    {
                        icon: "mdi-calendar-month",
                        title: `${$t("sidebar.Appointments")}`,
                        to: "/admin/appointments"
                    },
                    {
                        icon: "mdi-history",
                        title: `${$t("sidebar.History")}`,
                        to: "/admin/history"
                    },
                    {
                        icon: "mdi-bell",
                        title: `${$t("sidebar.Alerts")}`,
                        to: "/admin/alerts"
                    }
                ];
            }
        });

        const avatar = name => {
            let textAvatar = "";
            const array = name?.split(" ");
            if (array) {
                array.forEach(item => {
                    textAvatar += item.substring(0, 1);
                });
            }
            return textAvatar;
        };

        const setAvatarLetter = computed(() => {
         let firstName = avatar(authUser?.value?.firstName?.split(' ').map((word) => word[0]).join(''))
         let lastName = avatar(authUser?.value?.lastName?.split(' ').map((word) => word[0]).join(''))
         return (`${firstName}${lastName}`)
        })

        return {
            authUser,
            avatar,
            items,
            isDoctor,
            setAvatarLetter
        };
    },
    computed: {
        ...mapState(["SidebarColor", "SidebarBg"]),
        Sidebar_drawer: {
            get() {
                return this.$store.state.Sidebar_drawer;
            },
            set(val) {
                this.$store.commit("SET_SIDEBAR_DRAWER", val);
            }
        }
    },
    watch: {
        "$vuetify.breakpoint.smAndDown"(val) {
            this.$emit("update:expandOnHover", !val);
        }
    },

    methods: {}
});
</script>
<style lang="scss">
.custom-margin {
    margin-left: 1px;
    margin-top: 1px;
}

#main-sidebar {
    box-shadow: 1px 0 20px rgba(0, 0, 0, 0.08);
    -webkit-box-shadow: 1px 0 20px rgba(0, 0, 0, 0.08);

    .v-navigation-drawer__border {
        display: none;
    }

    .v-list {
        padding: 8px 15px;
    }

    .v-list-item {
        &__icon--text,
        &__icon:first-child {
            justify-content: center;
            text-align: center;
            width: 20px;
        }
    }

    .profile-bg {
        background: url("/images/user-info.jpg") no-repeat;
        padding: 30px;
        padding-left: 15px !important;
    }
}
</style>
