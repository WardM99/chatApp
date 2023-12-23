import { GroupBasic } from "./group";

export interface UserBasic {
  user_id: number;
  name: string;
  status: string | null;
}

export interface User extends UserBasic {
  groups: GroupBasic[];
}

export interface Users {
  users: User[];
}
