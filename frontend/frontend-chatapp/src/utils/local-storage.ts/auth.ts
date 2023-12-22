import { LocalStorageKey } from "../../data/enums";

export function setAccessToken(value: string | null) {
  setToken(LocalStorageKey.ACCESS_TOKEN, value);
}

export function setTokenType(value: string | null) {
  setToken(LocalStorageKey.TOKEN_TYPE, value);
}

function setToken(key: LocalStorageKey, value: string | null) {
  if (value === null) {
    localStorage.removeItem(key);
  } else {
    localStorage.setItem(key, value);
  }
}

export function getAccessToken(): string | null {
  return getToken(LocalStorageKey.ACCESS_TOKEN);
}

export function getTokenType(): string | null {
  return getToken(LocalStorageKey.TOKEN_TYPE);
}

function getToken(key: LocalStorageKey) {
  return localStorage.getItem(key);
}
