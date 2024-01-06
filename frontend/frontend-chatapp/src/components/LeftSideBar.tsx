import Nav from "react-bootstrap/Nav";
import { Container } from "react-bootstrap";
import GroupItemComponent from "./GroupItemComponent";
import InfiniteScroll from "react-infinite-scroll-component";
import { User } from "../data/interfaces/user";
import { GroupBasic } from "../data/interfaces/group";
import { Dispatch, SetStateAction } from "react";

interface Props {
  user: User;
  setGroupId: Dispatch<SetStateAction<number>>;
}

function LeftSidebar({ user, setGroupId }: Props) {
  const items: GroupBasic[] = user.groups;

  let hasMore = true;
  let i = 0;
  const fetchData = () => {
    console.log("HELLO");
    const data = items[i];
    console.log(data);
    i++;
    if (i >= items.length) hasMore = false;
    return data;
  };
  return (
    <>
      <Container className="sidebar-container">
        <Nav variant="pills" className="flex-column">
          <InfiniteScroll
            dataLength={1} //This is important field to render the next data
            next={fetchData}
            hasMore={hasMore}
            loader={<h4>Loading...</h4>}
            endMessage={
              <p style={{ textAlign: "center" }}>
                <b>Yay! You have seen it all</b>
              </p>
            }
            style={{
              position: "absolute",
              height: "100%",
              overflow: "auto",
              overflowY: "scroll",
            }}
          >
            {items.map(({ name, group_id }) => (
              <GroupItemComponent
                key={"GroupComponent" + group_id}
                name={name}
                group_id={group_id}
                setGroupId={setGroupId}
              />
            ))}
          </InfiniteScroll>
        </Nav>
      </Container>
    </>
  );
}

export default LeftSidebar;
