import LeftSidebar from "./LeftSideBar";
import MessageViewComponent from "./messageViewComponent";
import { User } from "../data/interfaces/user";
import { useState } from "react";
import NavBarComponent from "./NavBarComponent";

interface Props {
  user: User;
}

function MainComponent({ user }: Props) {
  const [groupId, setGroupId] = useState<number>(-1);
  console.log(groupId);
  return (
    <>
    <NavBarComponent name={user.name} status={user.status}/>
    <div className="container-fluid">
      <div className="row">
        <div className="bg-dark col-auto col-md-2 min-vh-100">
          <LeftSidebar user={user} setGroupId={setGroupId} />
        </div>
        <div className="bg-dark col-md-10">
          <MessageViewComponent />
        </div>
      </div>
    </div>
    </>
  );
}

export default MainComponent;
