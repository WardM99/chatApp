import Nav from "react-bootstrap/Nav";
import { Container } from "react-bootstrap";
import GroupItemComponent from "./GroupItemComponent";
import InfiniteScroll from "react-infinite-scroll-component";
import UserCardComponent from "./UserCardComponent";
import Button from "react-bootstrap/Button";

function LeftSidebar() {
  const items = [{ group_id: 0, name: "group0" }];

  for (let i = 1; i <= 20; i++) {
    items.push({ group_id: i, name: "group" + i });
  }
  let hasMore = true;
  let i = 0;
  const fetchData = () => {
    let data = items[i];
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
            dataLength={items.length} //This is important field to render the next data
            next={fetchData}
            hasMore={hasMore}
            loader={<h4>Loading...</h4>}
            endMessage={
              <p style={{ textAlign: "center" }}>
                <b>Yay! You have seen it all</b>
              </p>
            }
            style={{ height: "400px", overflowY: "auto", minHeight: "90vh" }}
          >
            {items.map(({ name, group_id }) => (
              <GroupItemComponent
                key={"GroupComponent" + group_id}
                name={name}
                group_id={group_id}
              />
            ))}
            <Button variant="outline-success" id="button-addon2">
              Add group
            </Button>
          </InfiniteScroll>
          <UserCardComponent name="Joske" status="Muziek luisteren" />
        </Nav>
      </Container>
    </>
  );
}

export default LeftSidebar;
