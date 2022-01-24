import React, { useState, useEffect } from "react";
import TableRow from "./TableRow";
import { getApiRoute } from "../../state";

const BASE_URL = getApiRoute("requestMessage")
const UsersTableDetail = (props) => {
    const { userId } = props;
    const [ users, setUsers ] = useState([]);
    const [ isFetchSuccess, setIsFetchSuccess ] = useState(true);
    const apiUrl = `${getApiRoute}/get_people/${userId}`;

    const fetchUsers = async () => {
        const response = await fetch(apiUrl)
        .catch(() => {
            setIsFetchSuccess(false);
        });
        const usersData = await response.json();

        setUsers(usersData);
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    if (!isFetchSuccess) {
        return <div>Opps, Something went wrong :(((</div>
    }

    return (
        <div className="users-table-detail">
           {users.map(user => <TableRow key={user.user_id} userId={userId} otherParticipant={user} />)} 
        </div>
    )
};

export default UsersTableDetail;
