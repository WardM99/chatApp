import LeftSidebar from "./LeftSideBar";
import MessageViewComponent from "./messageViewComponent";

function MainComponent() {
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="bg-dark col-auto col-md-2 min-vh-100">
            <LeftSidebar />
        </div>
        <div className="bg-dark col-md-10">
          <MessageViewComponent />
        </div>
      </div>
    </div>
  );
}

export default MainComponent;
