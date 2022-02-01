import { useEffect, useState } from "react";
import { getApiRoute } from "../../state";

const MessageContent = (props) => {
    const { content, hasAttachment, attachmentData } = props;
    const [ imageElement, setImageElement ]  = useState();
    
    useEffect(() => {
        if (!hasAttachment) return;
        
        const { thumbnailName, imageName, width, height, alt } = attachmentData
        const APIGetThumbnail = getApiRoute("getImage") + "/" + thumbnailName;

        const showRegularImageSize = () => {
            // If the user clicked on the thumbnail, display the original image
            const APIGetImage = getApiRoute("getImage") + "/" + imageName;
            fetch(APIGetImage)
            .then(response => response.blob())
            .then(image => window.open(URL.createObjectURL(image)))
            .catch(error => console.error(error));
        }

        // Fetch image from the server
        fetch(APIGetThumbnail)
        .then(response => response.blob())
        .then(image => setImageElement(<img src={URL.createObjectURL(image)} alt={alt} width={width} height={height} onClick={showRegularImageSize}></img>))
        .catch(error => console.error(error));

    }, [hasAttachment, attachmentData])
    

    return (
        <div className="message-content">
            {imageElement}
            <div>{content}</div>
        </div>
    );
};

export default MessageContent;
