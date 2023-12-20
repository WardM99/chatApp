import Card from "react-bootstrap/Card";
interface Message {
  message: string;
  sender_id: number;
  message_id: number;
}

function MessageComponent({ message, sender_id, message_id }: Message) {
  return (
    <>
      <Card
        style={{
          height: "20px",
          minHeight: "10vh",
        }}
        className="bg-dark text-light border border-success"
      >
        <Card.Body id={"MessageId" + message_id}>
          <Card.Title>{sender_id}</Card.Title>
          <Card.Text>{message}</Card.Text>
        </Card.Body>
      </Card>
    </>
  );
}

export default MessageComponent;
