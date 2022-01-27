import React from "react";
import ActionButton from "./ActionButton";
import "./user_table.css";

const TableRow = (props) => {
    const { otherParticipant } = props;
    const { username: otherParticipantName, user_id: otherParticipantId, request_status: status, is_sender: isSender } = otherParticipant;

    return (
        <div className="table-row">
            <div className="person-infor">{otherParticipantName}</div>
            <ActionButton
                otherParticipantId={otherParticipantId}
                status={status}
                isSender={isSender}
            />
        </div>
    )
}

export default TableRow;
