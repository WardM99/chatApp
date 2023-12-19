import Card from 'react-bootstrap/Card';
interface User {
  name: string;
  status: string;
}

function UserCardComponent({name, status}: User) {
  return (
    <Card 
    style={{ height: "20px", overflowY: "auto", minHeight: "10vh" }}>
      <Card.Body>
        <Card.Title>{name}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">{status}</Card.Subtitle>
      </Card.Body>
    </Card>
  );
}

export default UserCardComponent;
