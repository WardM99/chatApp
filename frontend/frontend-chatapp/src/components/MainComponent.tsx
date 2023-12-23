import LeftSidebar from "./LeftSideBar";
import MessageViewComponent from "./messageViewComponent";
import { User } from "../data/interfaces/user";
import { useState } from "react";

interface Props {
  user: User;
}

function MainComponent({ user }: Props) {

  const [groupId, setGroupId] = useState<Number>(-1)


  return (
    <div className="container-fluid">
      <div className="row">
        <div className="bg-dark col-auto col-md-2 min-vh-100">
          <LeftSidebar user={user} setGroupId={setGroupId}/>
        </div>
        <div className="bg-dark col-md-10">
          <MessageViewComponent />
        </div>
      </div>
    </div>
  );
}

export default MainComponent;
