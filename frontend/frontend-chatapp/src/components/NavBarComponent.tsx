import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";

interface User {
  name: string;
  status: string | null;
}

function NavBarComponent({ name, status }: User) {
  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand>{name}</Navbar.Brand>
        <Navbar.Brand hidden={status === null}>{status}</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Item>
              <ButtonGroup
                aria-label="Basic example"
                className="btn-group d-flex"
              >
                <Button variant="outline-primary">Add Group</Button>
                <Button variant="outline-primary">Make Group</Button>
              </ButtonGroup>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBarComponent;
