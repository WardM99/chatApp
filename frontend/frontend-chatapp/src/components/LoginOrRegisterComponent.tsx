import { useState } from "react";
import LoginFormComponent from "./LoginFormComponent";
import RegisterFormComponent from "./RegisterFromComponent";

type LoginStates = "Login" | "Register";

function LoginOrRegisterComponent() {
  const [loginState, setLoginState] = useState<LoginStates>("Login");

  const SwitchStatus = () => {
    if (loginState === "Login") {
      setLoginState("Register");
    } else if (loginState == "Register") {
      setLoginState("Login");
    }
  };

  if (loginState === "Login")
    return <LoginFormComponent switchForm={SwitchStatus} />;
  else if (loginState === "Register") {
    return <RegisterFormComponent switchForm={SwitchStatus} />;
  }
}

export default LoginOrRegisterComponent;
