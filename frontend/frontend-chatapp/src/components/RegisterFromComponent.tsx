import { Dispatch, SetStateAction } from "react";
import { User } from "../data/interfaces";
import { createUser } from "../utils/api/user";

interface Props {
  switchForm: () => void;
  setUser: Dispatch<SetStateAction<User | null>>;
}

function RegisterFormComponent({ switchForm, setUser }: Props) {
  async function createUserApi(name: string, password: string) {
    const response: User | null = await createUser(name, password);
    setUser(response);
  }

  return (
    <>
      <h1>Register</h1>
      <form
        onSubmit={async (event: any) => {
          event.preventDefault();
          const name: string = event.target.elements.username.value;
          const password: string = event.target.elements.password.value;
          const passwordControl: String =
            event.target.elements.passwordControl.value;
          if (password === passwordControl) {
            await createUserApi(name, password);
          }
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
        <div className="mb-6">
          <label className="form-label">Password</label>
          <input
            type="password"
            name="passwordControl"
            className="form-control"
            id="idPasswordControl"
          />
        </div>
        <button type="submit" className="btn btn-success">
          Register
        </button>
        <button type="button" onClick={switchForm} className="btn btn-primary">
          Already an account? Go to to login form
        </button>
      </form>
    </>
  );
}

export default RegisterFormComponent;
