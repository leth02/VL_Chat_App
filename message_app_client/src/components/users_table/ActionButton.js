import React, { useState } from "react";

const BASE_URL = "http://localhost:5000";
const ActionButton = (props) => {
    const { otherParticipantId, userId } = props;
    const [ status, setStatus ] = useState(props.status);
    const [ isSender, setIsSender ] = useState(props.isSender);

    const handleOnclick = async (buttonType) => {
        if (buttonType === "accept"){
            const accepted_time = Date.now();
            const acceptedResponse = await fetch(BASE_URL + `/api/request/accept/${otherParticipantId}/${userId}/${accepted_time}`, {
                method: "POST"
            });
            if (acceptedResponse.status === 200) {
                setStatus("accepted");
            }
        }else if(buttonType === "reject"){
            const rejectedResponse = await fetch(BASE_URL + `/api/request/reject/${otherParticipantId}/${userId}`, {
                method: "POST"
            });
            if (rejectedResponse.status === 200) {
                setStatus("rejected");
            }
        }else if(buttonType === "request message") {
            const requestTime =  Date.now();
            const requestResponse = await fetch(BASE_URL + `/api/request/send/${userId}/${otherParticipantId}/${requestTime}`, {
                method: "POST"
            });
            if (requestResponse.status === 200) {
                setStatus("pending");
                setIsSender(false)
            }
        }else{
            const cancelResponse = await fetch(BASE_URL + `/api/request/cancel/${userId}/${otherParticipantId}`, {
                method: "POST"
            });
            if (cancelResponse.status === 200) {
                setStatus(null);
                setIsSender(null);
            }
        }
    };

    if(isSender){
        if(status === "pending"){
            return (
                <div className="person-button">
                    <button type="button" onClick={() => handleOnclick("accept")}>Accept</button>
                    <button type="button" onClick={() => handleOnclick("reject")}>Reject</button>
                </div>
            );
        }else if(status === "accepted"){
            return (
                <div className="person-button">
                    <button type="button">Friend</button>
                </div>
            );
        }else{
            return (
                <div className="person-button">
                    <button type="button" onClick={() => handleOnclick("request message")}>Request message</button>
                </div>
            );
        }
    }else{
        if(status === "pending"){
            return (
                <div className="person-button">
                    <button type="button" onClick={() => handleOnclick("cancel request")}>Cancel request</button>
                </div>
            );
        }else if(status === "accepted"){
            return (
                <div className="person-button">
                    <button type="button">Friend</button>
                </div>
            );
        }else{
            return (
                <div className="person-button">
                    <button type="button" onClick={() => handleOnclick("request message")}>Request message</button>
                </div>
            );
        }
    }

};

export default ActionButton;