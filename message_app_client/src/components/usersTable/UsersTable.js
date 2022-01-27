import React from "react";
import UsersTableDetail from "./UsersTableDetails";
import "./user_table.css";

const UsersTable = (props) => {
    return (
        <div className="users-table">
            <div className="users-table-nav">
                <a href="/messages">inbox</a>
            </div>
            <UsersTableDetail/>
        </div>
    )
};

export default UsersTable;
