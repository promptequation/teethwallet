import { defineStore } from 'pinia';
import { gql } from 'graphql-request';
import { graphQLClient } from 'src/boot/graphql';
import { Appointments } from 'src/types/appointments'

interface State {
  appointments: Appointments[] | null
}

export const useAppointmentStore = defineStore('appointment', {
  state: (): State => ({
    appointments: [],
  }),
  getters: {
    getAppointments: (state) => {
      return state.appointments?.map((item: any) => {
        return {
          id: item.node.id,
          duration: item.node.duration,
          startDate: item.node.startDate,
          isActive: item.node.isActive,
          patient: item.node.patient.name,
          doctorId: item.node.doctor.id,
          doctor: item.node.doctor.name,
          companyId: item.node.company.id,
          companyName: item.node.company.name,
        };
      });
    },
  },
  actions: {
    setAppointments(appointments: Appointments[]) {
      this.appointments = appointments;
    },

    async fetchAppointments(
      patientId: number,
      doctorId: number,
      companyId: number,
      langId: number,
      isActive: boolean,
    ) {
      const query = gql`
        query (
          $patientId: ID
          $doctorId: Float
          $companyId: Float
          $langId: Float
          $isActive: Boolean
        ) {
          appointments(
            patient: $patientId
            doctor_Id: $doctorId
            company_Id: $companyId
            isActive: $isActive
          ) {
            edges {
              node {
                id
                patient {
                  id
                  name
                }
                doctor {
                  id
                  name
                }
                company {
                  id
                  name
                }
                isActive
                startDate
                duration
                createdAt
                appointmentlangSet(lang_Id: $langId) {
                  edges {
                    node {
                      note
                    }
                  }
                }
              }
            }
          }
        }
      `;
      const variables = { patientId, doctorId, companyId, langId, isActive };

      return await graphQLClient.request(query, variables);
    },
  },
});
