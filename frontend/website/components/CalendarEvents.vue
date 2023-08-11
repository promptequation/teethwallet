<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64">
        <v-toolbar flat>
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
            {{ $t("startPage.Today") }}
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu bottom right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">
                <!-- <pre>{{ typeToLabel }}</pre> -->
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>
                  mdi-menu-down
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>{{ $t("startPage.Day") }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>{{ $t("startPage.Week") }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>{{ $t("startPage.Month") }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>{{ $t("startPage.Days") }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="600">
        <v-calendar ref="calendar" v-model="focus" color="primary" :events="events" :event-color="getEventColor"
          :type="type" @click:event="showEvent" @click:more="viewDay" @click:date="viewDay" @change="updateRange">
        </v-calendar>
        <v-menu v-model="selectedOpen" :close-on-content-click="false" :activator="selectedElement" offset-x>
          <v-card color="grey lighten-4" min-width="350px" flat>
            <v-toolbar :color="selectedEvent.color" dark>
              <v-btn nuxt :to="`/admin/appointments/entry?editableId=${selectedEvent.id}`" icon>
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon>
                <v-icon>mdi-heart</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </v-toolbar>
            <v-card-text>
              <span v-html="selectedEvent.details"></span>
              <v-simple-table dense>
                <template v-slot:default>
                  <tbody>
                    <tr>
                      <th>{{ $t('startPage.Name') }}</th>
                      <td>{{ selectedEvent.name }}</td>
                    </tr>
                    <tr>
                      <th>{{ $t('Start Date') }}</th>
                      <td>{{ dateTimeFormat(selectedEvent.start) }}</td>
                    </tr>
                    <tr>
                      <th>{{ $t('End Date') }}</th>
                      <td>{{ dateTimeFormat(selectedEvent.end) }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
            <v-card-actions>
              <v-btn text color="secondary" @click="selectedOpen = false">
                <th>{{ $t('startPage.Cancel') }}</th>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import {
  ref,
  computed
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";

export default {
  name: "CalendarEvents",
  props: {
    appointments: {
      type: Array,
      required: true,
      default: function () {
        return []
      }
    },
    isDoctor: {
      type: Boolean,
      required: true,
      default: false
    }
  },

  setup() {
    const { $t } = useNuxtTranslator()
    const type = ref('month');
    const typeToLabel = computed(() => {
      return {
        month: `${$t("startPage.Month")}`,
        week: `${$t("startPage.Week")}`,
        day: `${$t("startPage.Day")}`,
        "4day": `${$t("startPage.Days")}`,
      }
    });
    const title = computed(() => {
      const startMonth = monthFormatter(start)
      const endMonth = monthFormatter(end)
      const suffixMonth = startMonth === endMonth ? '' : endMonth

      const startYear = start.year
      const endYear = end.year
      const suffixYear = startYear === endYear ? '' : endYear

      const startDay = start.day + nth(start.day)
      const endDay = end.day + nth(end.day)
      switch (type.value) {
        case 'month':
          return `${startMonth} ${startYear}`
        case 'week':
        case '4day':
          return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
        case 'day':
          return `${startMonth} ${startDay} ${startYear}`
      }
      return ''
    })

    return {
      type,
      typeToLabel,
      title
    }
  },
  data: () => ({
    focus: '',
    today: null,
    start: null,
    end: null,
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    events: [],
    colors: ['info', 'success', 'warning', 'error', 'indigo', 'pink', 'grey darken-1'],
    names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
  }),
  
  mounted() {
    this.$refs.calendar.checkChange()
  },
  methods: {
    viewDay({ date }) {
      this.focus = date
      this.type = 'day'
    },
    getEventColor(event) {
      return event.color
    },
    setToday() {
      this.focus = this.today
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        setTimeout(() => this.selectedOpen = true, 10)
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }

      nativeEvent.stopPropagation()
    },

    dateTimeFormat(date) {
      if (!date) return ''
      return this.$dayjs(date).format("MMMM DD, YYYY hh:mm A")
    },
    getEndDate(startDate, duration) {
      let endDate = "";
      if (startDate && duration) {
        endDate = this.$dayjs(startDate).add(duration, "m").toISOString();
      }
      return endDate
    },

    updateRange({ start, end }) {
      const events = []
      this.appointments?.forEach(item => {
        events.push({
          name: this.isDoctor ? item.patient : item.doctor,
          id: item.id,
          start: new Date(item.startDate),
          end: new Date(this.getEndDate(item.startDate, item.duration)),
          color: this.colors[this.rnd(0, this.colors.length - 1)],
          timed: true,
        })
      })
      this.start = start
      this.end = end
      this.events = events
    },
    nth(d) {
      return d > 3 && d < 21
        ? 'th'
        : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    formatDate(a, withTime) {
      return withTime
        ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}`
        : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
    },
  }
};
</script>