import Nav from 'react-bootstrap/Nav';

interface GroupItem {
    group_id: Number;
    name: string;
}

function GroupItemComponent({group_id, name}: GroupItem) {
    return <Nav.Link eventKey={"link-"+group_id}>{name}</Nav.Link>
}

export default GroupItemComponent