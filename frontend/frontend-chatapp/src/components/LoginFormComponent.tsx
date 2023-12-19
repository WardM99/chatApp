interface Props {
  switchForm: () => void;
}

function LoginFormComponent({ switchForm }: Props) {
  return (
    <>
      <h1>Login</h1>
      <form onSubmit={(event: any)=>{
        event.preventDefault();
        console.log(event.target.elements.username.value);
        console.log(event.target.elements.password.value);
      }}>
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
