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
          minHeight: "10vh"
        }}
      >
        <Card.Body id={"MessageId"+message_id}>
          <Card.Title>{sender_id}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted">{message}</Card.Subtitle>
        </Card.Body>
      </Card>
    </>
  );
}

export default MessageComponent;
