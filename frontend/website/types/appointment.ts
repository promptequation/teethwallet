export interface Tooth {
    id?: number | string,
    number?: number
}

export interface Diagnosis {
    id?: number | string,
    name?: string
}

export interface Treatment {
    id?: number | string,
    name?: string
}

export interface Appointment {
    id?: number
    tooth?: Tooth
    diagnosis?: string | Diagnosis
    treatment?: string | Treatment
    duration?: string | number,
    startDate?: string,
    patient?: string,
    doctor?: string,
}

export interface AppointmentDetail {
    id?: number
    appointment?: Appointment
    tooth?: Tooth
    diagnosis?: Diagnosis
    treatment?: Treatment
}
export interface DoctorDetail {
    id?: number | string,
    name: string
}
export interface PatientType {
    id?: number | string,
    userId?: number | string,
    name: string,
    username: string,
    email: string,
    dateOfBirth: string,
    isActive: boolean
}