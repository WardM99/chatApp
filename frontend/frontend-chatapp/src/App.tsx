import { useEffect, useState } from "react";
import LoginOrRegisterComponent from "./components/LoginOrRegisterComponent";
import MainComponent from "./components/MainComponent";
import { User } from "./data/interfaces";
import { currentUser, logout } from "./utils/api/user";

function App() {
  const [user, setUser] = useState<User | null>(null);
  async function getUserApi() {
    const response: User | null = await currentUser();
    setUser(response);
  }

  useEffect(() => {
    const fetchData = async () => {
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
      <MainComponent user={user}/>
    </>
  );
}

export default App;
