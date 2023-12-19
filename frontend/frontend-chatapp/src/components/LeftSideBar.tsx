import Nav from "react-bootstrap/Nav";
import { Container, Row, Col } from "react-bootstrap";
import GroupItemComponent from "./GroupItemComponent";

const items = [{ group_id: 0, name: "group0" }];

for (let i = 1; i <= 100; i++) {
  items.push({ group_id: i, name: "group" + i });
}

function LeftSidebar() {
  return (
    <Container
      className="sidebar-container"
      style={{ height: "400px", overflowY: "auto", minHeight: "90vh" }}
    >
      <Row>
        <Col md={12}>
          <Nav variant="pills" className="flex-column">
            {items.map(function (d) {
              return <GroupItemComponent group_id={d.group_id} name={d.name}/>;
            })}
          </Nav>
        </Col>
      </Row>
    </Container>
  );
}

export default LeftSidebar;
