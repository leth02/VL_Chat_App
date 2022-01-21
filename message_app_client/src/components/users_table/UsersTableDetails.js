import React, { useState, useEffect } from "react";
import TableRow from "./TableRow";

const UsersTableDetail = (props) => {
    const { userId } = props;
    const [ users, setUsers ] = useState([]);
    const [ isFetchSuccess, setIsFetchSuccess ] = useState(true);
    const apiUrl = `http://localhost:5000/api/request/get_people/${userId}`;

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
        <div className="people-table">
           {users.map(user => <TableRow key={user.user_id} userId={userId} otherParticipant={user} />)} 
        </div>
    )
};

export default UsersTableDetail;
