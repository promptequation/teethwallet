export interface User {
  id?: number | string
  userId?: number | string
  name?: string
  username?: string
  email?: string
  avatar?: string
  dateOfBirth?: string
}

export interface Patient extends User {
    adddress?: string
}
