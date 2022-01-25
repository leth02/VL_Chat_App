import React from "react";
import UsersTableDetail from "./UsersTableDetails";
import "./user_table.css";

const UsersTable = (props) => {
    // userID should be stored in the cookies after user logged in
    // This value will be replaced after cookies is fully implemented
    const userId = 1;

    return (
        <div className="users-table">
            <div className="users-table-nav">
                <a href="/messages">inbox</a>
            </div>
            <UsersTableDetail userId={userId}/>
        </div>
    )
};

export default UsersTable;
