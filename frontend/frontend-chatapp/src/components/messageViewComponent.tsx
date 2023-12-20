import InfiniteScroll from "react-infinite-scroll-component";
import Form from "react-bootstrap/Form"
import InputGroup from "react-bootstrap/InputGroup"
import Button from "react-bootstrap/Button";
import MessageComponent from "./MessageComponent";

function MessageViewComponent() {
  const items = [{ message_id: 0, message: "message0", sender_id: 1 }];

  for (let i = 1; i <= 30; i++) {
    items.push({ message_id: i, message: "message" + i, sender_id: 1 });
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
        style={{
          height: "400px",
          overflowY: "auto",
          minHeight: "90vh",
          display: "flex",
          flexDirection: "column-reverse",
        }}
      >
        {items.map(({ message_id, message, sender_id }) => (
          <MessageComponent
            key={"MessageComponent" + message_id}
            message_id={message_id}
            message={message}
            sender_id={sender_id}
          />
        ))}
      </InfiniteScroll>
      <br />
      <InputGroup>
        <Form.Control
          placeholder="new message"
          aria-describedby="basic-addon2"
        />
        <Button variant="outline-success" id="button-addon2">
          Send
        </Button>
      </InputGroup>
    </>
  );
}

export default MessageViewComponent;
