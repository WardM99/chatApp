import Card from "react-bootstrap/Card";
interface User {
  name: string;
  status: string;
}

function UserCardComponent({ name, status }: User) {
  return (
    <Card
      style={{ height: "20px", overflowY: "auto", minHeight: "10vh" }}
      className="bg-dark text-light border border-primary"
    >
      <Card.Header>
        <Card.Title>{name}</Card.Title>
      </Card.Header>
      <Card.Body>
        <Card.Subtitle className="mb-2">{status}</Card.Subtitle>
      </Card.Body>
    </Card>
  );
}

export default UserCardComponent;
