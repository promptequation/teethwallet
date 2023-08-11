export interface CommonNode {
  id?: string | number
  name?: string
}

export interface PageInfo {
  hasNextPage?: boolean
  hasPreviousPage?: boolean
}

export interface Edges {
  node?: CommonNode
  cursor?: string
}

export interface Gender {
  id?: string | number
  name?: string
}

export interface Group {
  edges?: Edges[],
  pageInfo?: PageInfo,
}

export interface Company {
  id?: string | number
  name?: string
}

export interface User {
  id?: string | number
  name?: string
  firstName?: string
  lastName?: string
  username?: string
  email?: string
  avatar?: string
  dateOfBirth?: string
  phone?: string
  gender?: Gender,
  groups?: Group,
  company?: Company,
}

export interface CompanyUser {
  id?: string | number
  companyId?: number | string
  userId?: number | string
  doctorId?: number | string
  groupId?: number | string
  status?: string
  isOwner?: boolean
  isActive?: boolean
  requestedById?: number | string
  approvalById?: number | string
  approvalAt?: string
  joinedDatetime?: string
}
