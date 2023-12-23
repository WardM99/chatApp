import { login } from "../utils/api/user";
import { User } from "../data/interfaces";
import { Dispatch, SetStateAction } from "react";

interface Props {
  switchForm: () => void;
  setUser: Dispatch<SetStateAction<User | null>>;
}

function LoginFormComponent({ switchForm, setUser }: Props) {
  async function loginApi(name: string, password: string) {
    const response: User | null = await login(name, password);
    setUser(response);
  }

  return (
    <>
      <h1>Login</h1>
      <form
        onSubmit={async (event: any) => {
          event.preventDefault();
          const name: string = event.target.elements.username.value;
          const password: string = event.target.elements.password.value;
          await loginApi(name, password);
        }}
      >
        <div className="mb-6">
          <label className="form-label">Name</label>
          <input
            type="text"
            className="form-control"
            id="idUserName"
            name="username"
            aria-describedby="nameHelp"
          />
        </div>
        <div className="mb-6">
          <label className="form-label">Password</label>
          <input
            type="password"
            name="password"
            className="form-control"
            id="idPassword"
          />
        </div>
        <button type="submit" className="btn btn-success">
          Login
        </button>
        <button type="button" onClick={switchForm} className="btn btn-primary">
          No account? Go to to register form
        </button>
      </form>
    </>
  );
}

export default LoginFormComponent;
