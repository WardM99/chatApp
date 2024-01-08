import { useEffect, useState } from "react";
import { User } from "./data/interfaces";
import { currentUser } from "./utils/api/user";

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

  if (user === null) return <></>;

  return <></>;
}

export default App;
