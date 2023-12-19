interface Props {
    switchForm: () => void;
  }
  
  function RegisterFormComponent({ switchForm }: Props) {
    return (
      <>
        <h1>Register</h1>
        <form onSubmit={(event: any)=>{
          event.preventDefault();
          console.log(event.target.elements.username.value);
          console.log(event.target.elements.password.value);
          console.log(event.target.elements.passwordControl.value);
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
  