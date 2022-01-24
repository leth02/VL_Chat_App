import React from "react";
import UsersTableDetail from "./UsersTableDetails";

const UsersTable = (props) => {
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
