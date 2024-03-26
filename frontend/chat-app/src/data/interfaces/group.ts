import { UserBasic } from "./user";
export interface GroupBasic {
  group_id: number;
  name: string;
}

export interface Group extends GroupBasic {
  users: UserBasic[];
  owner_id: number;
  owner: UserBasic;
}
