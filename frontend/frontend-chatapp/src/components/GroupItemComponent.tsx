import { Dispatch, SetStateAction } from "react";
import Nav from "react-bootstrap/Nav";

interface GroupItem {
  group_id: Number;
  name: string;
  setGroupId: Dispatch<SetStateAction<Number>>;
}

function GroupItemComponent({ group_id, name, setGroupId }: GroupItem) {
  return (
    <Nav.Item>
      <Nav.Link 
        onClick={() => {
          setGroupId(group_id);
        }} 
        className="border border-primary" eventKey={"link-" + group_id}
      >
        {name}
      </Nav.Link>
    </Nav.Item>
  );
}

export default GroupItemComponent;
