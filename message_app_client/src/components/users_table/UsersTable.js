import React from "react";
import UsersTableDetail from "./UsersTableDetails";

const UsersTable = (props) => {
    const userId = 1;

    return (
        <div>
            <div>
                <a href="#">inbox</a>
            </div>
            <UsersTableDetail userId={userId}/>
        </div>
    )
};

export default UsersTable;