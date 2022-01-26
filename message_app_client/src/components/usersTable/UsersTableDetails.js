import React, { useState, useEffect, useContext } from "react";
import TableRow from "./TableRow";
import { SessionDataContext } from "../../contexts/SessionDataContext";
import { useNavigate } from "react-router-dom";
import { getApiRoute, routes } from "../../state";

const BASE_URL = getApiRoute("requestMessage")
const UsersTableDetail = (props) => {
    const { userId } = props;
    const [ users, setUsers ] = useState([]);
    const [ isFetchSuccess, setIsFetchSuccess ] = useState(true);
    const { currentUserID, setCurrentRoute } = useContext(SessionDataContext);
    const navigate = useNavigate();
    const apiUrl = `${BASE_URL}/get_people/${currentUserID}`;

    const fetchUsers = async () => {
        const response = await fetch(apiUrl)
        .catch(() => {
            setIsFetchSuccess(false);
        });
        const usersData = await response.json();

        setUsers(usersData);
    };

    useEffect(() => {
        if (!currentUserID) {
            setCurrentRoute("/find_users");
            navigate(routes.login);
            alert("You must login first!");
        } else {
            fetchUsers();
        }
    }, [currentUserID, navigate]);

    if (!isFetchSuccess) {
        return <div>Opps, Something went wrong :(((</div>
    }

    return (
        <div className="users-table-detail">
           {users.map(user => <TableRow key={user.user_id} otherParticipant={user} />)} 
        </div>
    )
};

export default UsersTableDetail;
