export interface CreatedBy {
  name: string
}

export interface CreatedFor {
  name: string
}

export interface Company {
  name: string
}

export interface Notifications {
  id: number
  company: Company
  createdAt: string
  createdBy: CreatedBy
  createdFor: CreatedFor
  isRead: boolean
  notificationType: string
}
