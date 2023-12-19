import LeftSidebar from "./LeftSideBar";

function MainComponent() {
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="bg-light col-auto col-md-2 min-vh-100">
            <LeftSidebar />
        </div>
        <div className="col-md-10">
            <h1>Koalas zijn mooie dieren</h1>
        </div>
      </div>
    </div>
  );
}

export default MainComponent;
