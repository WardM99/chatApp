import { UserBasic } from "./user";
import { GroupBasic } from "./group";
export interface MessageBasic {
  message_id: number;
  message: string;
  sender_id: number;
  sender: UserBasic;
}

export interface Message {
  group_id: number;
  group: GroupBasic;
  reply_id: number | null;
  reply: MessageBasic | null;
}

export interface Messages {
  messages: Message[];
}
