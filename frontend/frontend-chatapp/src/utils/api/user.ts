import axios from "axios";
import { axiosInstance, getHeaders } from "./api";
import { User } from "../../data/interfaces";
import { setAccessToken, setTokenType } from "../local-storage.ts/auth";

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

function setLoginTokens(response: LoginResponse) {
  setAccessToken(response.access_token);
  setTokenType(response.token_type);
}

export async function createUser(
  name: string,
  password: string
): Promise<User | null> {
  const payload = {
    name,
    password,
  };
  try {
    const response = await axiosInstance.post("/users", payload);
    const login = response.data as LoginResponse;
    setLoginTokens(login);
    return login.user;
  } catch (error) {
    return null;
  }
}

export async function login(
  name: string,
  password: string
): Promise<User | null> {
  const payload = new FormData();
  payload.append("username", name);
  payload.append("password", password);
  try {
    const response = await axiosInstance.post("/users/login", payload);
    const login = response.data as LoginResponse;
    setLoginTokens(login);
    return login.user;
  } catch (error) {
    return null;
  }
}

export function logout(): void {
  setAccessToken(null);
  setTokenType(null);
}

export async function currentUser(): Promise<User | null> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.get("/users", config);
    const player = response.data as User;
    return player;
  } catch (error) {
    return null;
  }
}
