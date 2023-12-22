import { useEffect, useState } from "react";
import LoginOrRegisterComponent from "./components/LoginOrRegisterComponent";
import MainComponent from "./components/MainComponent";
import { User } from "./data/interfaces";
import { currentUser, logout } from "./utils/api/user";

function App() {
  const [user, setUser] = useState<User | null>(null);
  logout();
  async function getUserApi() {
    const response: User | null = await currentUser();
    setUser(response);
  }

  useEffect(() => {
    const fetchData = async () => {
      console.log("TEST")
      await getUserApi();
    };
    fetchData();
  }, []);

  if (user === null)
    return (
      <>
        <LoginOrRegisterComponent setUser={setUser} />
      </>
    );

  return (
    <>
      <MainComponent />
    </>
  );
}

export default App;
