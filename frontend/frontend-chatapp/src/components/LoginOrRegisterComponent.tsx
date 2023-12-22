import { Dispatch, SetStateAction, useState } from "react";
import LoginFormComponent from "./LoginFormComponent";
import RegisterFormComponent from "./RegisterFromComponent";
import { User } from "../data/interfaces";

type LoginStates = "Login" | "Register";

interface Props {
  setUser: Dispatch<SetStateAction<User | null>>;
}

function LoginOrRegisterComponent({ setUser }: Props) {
  const [loginState, setLoginState] = useState<LoginStates>("Login");

  const SwitchStatus = () => {
    if (loginState === "Login") {
      setLoginState("Register");
    } else if (loginState == "Register") {
      setLoginState("Login");
    }
  };

  if (loginState === "Login")
    return <LoginFormComponent switchForm={SwitchStatus} setUser={setUser} />;
  else if (loginState === "Register") {
    return <RegisterFormComponent switchForm={SwitchStatus} setUser={setUser} />;
  }
}

export default LoginOrRegisterComponent;
