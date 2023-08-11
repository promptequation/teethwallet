import { useAppointmentStore } from 'src/stores/appointment';
import { FetchAppointments } from 'src/types/appointments';

export function useAppointment() {
  const appointmentStore = useAppointmentStore();

  const fetchAppointments = async ({
    patientId,
    doctorId,
    companyId,
    langId,
    isActive,
  }: FetchAppointments) => {
    try {
      const { appointments } = await appointmentStore.fetchAppointments(
        patientId,
        doctorId,
        companyId,
        langId,
        isActive,
      );
      appointmentStore.setAppointments(appointments.edges);
    } catch (error: unknown) {
      console.log(error);
    }
  };

  return {
    fetchAppointments
  };
}
