import React, { useState, useContext } from "react";
import { getApiRoute } from "../../state";
import { SessionDataContext } from "../../Contexts";

const BASE_URL = getApiRoute("requestMessage");
const ActionButton = (props) => {
    const { otherParticipantId } = props;
    const [ status, setStatus ] = useState(props.status);
    const [ isSender, setIsSender ] = useState(props.isSender);
    const { currentUserID: userId } = useContext(SessionDataContext);

    const handleOnclick = async (buttonType) => {
        if (buttonType === "accept") {
            const accepted_time = Date.now();
            const acceptedResponse = await fetch(BASE_URL + `/accept/${otherParticipantId}/${userId}/${accepted_time}`, {
                method: "POST"
            });
            if (acceptedResponse.status === 200) {
                setStatus("accepted");
            }
        } else if (buttonType === "reject") {
            const rejectedResponse = await fetch(BASE_URL + `/reject/${otherParticipantId}/${userId}`, {
                method: "POST"
            });
            if (rejectedResponse.status === 200) {
                setStatus("rejected");
            }
        } else if (buttonType === "request message") {
            const requestTime =  Date.now();
            const requestResponse = await fetch(BASE_URL + `/send/${userId}/${otherParticipantId}/${requestTime}`, {
                method: "POST"
            });
            if (requestResponse.status === 200) {
                setStatus("pending");
                setIsSender(false)
            }
        } else {
            const cancelResponse = await fetch(BASE_URL + `/cancel/${userId}/${otherParticipantId}`, {
                method: "POST"
            });
            if (cancelResponse.status === 200) {
                setStatus(null);
                setIsSender(null);
            }
        }
    };

    if (isSender) {
        if (status === "pending") {
            return (
                <div className="action-button">
                    <button type="button" onClick={() => handleOnclick("accept")}>Accept</button>
                    <button type="button" onClick={() => handleOnclick("reject")}>Reject</button>
                </div>
            );
        } else if (status === "accepted") {
            return (
                <div className="action-button">
                    <button type="button">Friend</button>
                </div>
            );
        } else {
            return (
                <div className="action-button">
                    <button type="button" onClick={() => handleOnclick("request message")}>Request message</button>
                </div>
            );
        }
    } else {
        if (status === "pending") {
            return (
                <div className="action-button">
                    <button type="button" onClick={() => handleOnclick("cancel request")}>Cancel request</button>
                </div>
            );
        } else if (status === "accepted") {
            return (
                <div className="action-button">
                    <button type="button">Friend</button>
                </div>
            );
        } else {
            return (
                <div className="action-button">
                    <button type="button" onClick={() => handleOnclick("request message")}>Request message</button>
                </div>
            );
        }
    }

};

export default ActionButton;
