export interface Appointments {
    id?: string | number
    duration?: number | string
    startDate?: number | string
    isActive?: string
    patient?: string
    doctorId?: number | string
    doctor?: string
    companyId?: number | string
    companyName?: string
}

export interface FetchAppointments {
    patientId: number,
    doctorId: number,
    companyId: number,
    langId: number,
    isActive: boolean,
}