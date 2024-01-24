import "./App.css";
import { useEffect, useState } from "react";
import { User } from "./data/interfaces";
import { currentUser } from "./utils/api/user";
import { Login } from "./components/Login";
import { MainView } from "./components/MainView";

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

  if (user === null) return <Login setUser={setUser} />;

  return <MainView user={user} setUser={setUser} />;
}

export default App;
