

export interface userlookupType {
    id?: string | number,
    name?: string
}

export interface groupType {
    id?: string | number,
    name?: string
}

export interface patientInvitationsType {
    id?: string | number,
    user?: any,
    company?: any,
    isOwner?: boolean,
    isActive?: boolean,
    status?: any,
    requestedAt?: string
}

export interface compsnyUserType {
    id?: string | number,
    companyId?: string | number,
    company?: string,
    isOwner?: boolean,
    joinedDatetime?: string,
    userId?: string | number,
    user?: string
}


