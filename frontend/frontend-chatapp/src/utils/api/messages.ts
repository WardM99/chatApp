import { axiosInstance, getHeaders } from "./api";
import { Messages } from "../../data/interfaces";

export async function getMessagesFromGoup(
  groupId: number,
): Promise<Messages | null> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.get(
      "/groups/" + groupId + "/messages",
      config,
    );
    const messages = response.data as Messages;
    return messages;
  } catch (error) {
    return null;
  }
}
