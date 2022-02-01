// A helper function to calculate a readable time representation of the message
function getTimeString(timestamp) {
    let now = new Date();
    let todayBeginningTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
    let yesterDayBeginningTime = new Date(todayBeginningTime.getTime() - 86400000);
    let messageTime = new Date(timestamp);

    if (timestamp > todayBeginningTime.getTime()) {
        let minute = messageTime.getMinutes()
        minute = messageTime.getMinutes() < 10 ? "0" + minute : minute
        return `Today at ${messageTime.getHours()}:${minute}`;
    } else if (timestamp > yesterDayBeginningTime.getTime()) {
        return `Yesterday at ${messageTime.getHours()}:${messageTime.getMinutes()}`;
    } else {
        let msgTimeMonth = messageTime.getMonth() + 1;
        let msgTimeDayOfMonth = messageTime.getDate();
        if (msgTimeMonth < 10) msgTimeMonth = "0" + msgTimeMonth;
        if (msgTimeDayOfMonth < 10) msgTimeDayOfMonth = "0" + msgTimeDayOfMonth;

        return `${msgTimeMonth}/${msgTimeDayOfMonth}/${messageTime.getFullYear()}`;
    }
}

const MessageHeader = (props) => {
    const { senderName, sentTime } = props;
    const sentTimeString = getTimeString(sentTime);

    return (
        <div className="message-header">
            <div>
                <div>{senderName}</div>
                <div>{sentTimeString}</div>
            </div>
        </div>
    );
};

export default MessageHeader;
