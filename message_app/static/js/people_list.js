const PEOPLE_TABLE_HTML = document.querySelector(".people-table");
const BASE_URL = window.location.origin;

class PeopleModel{
    constructor(id, username, request_id, is_receiver, is_sender, request_status) {
        this.id = id;
        this.username = username;
        this.request_id = request_id;
        this.is_receiver = is_receiver;
        this.is_sender = is_sender;
        this.request_status = request_status;
        this.HTMLElement = new PeopleHTMLElement(this);
    }

    show() {
        this.HTMLElement.show();
    }
}

class PeopleHTMLElement{
    slefEl = null;
    parentEl = PEOPLE_TABLE_HTML;

    constructor(peopleObj) {
        this.peopleObj = peopleObj;
    }

    generateMarkup(){
        const is_receiver = this.peopleObj.is_receiver;
        const is_sender = this.peopleObj.is_sender;
        const request_status = this.peopleObj.request_status;

        if(is_sender){
            if(request_status == "pending"){
                return (
                    `
                    <div class="person" id="user-${this.peopleObj.id}">
                        <div class="person-infor">${this.peopleObj.username}</div>
                        <div class="person-button">
                            <button type="button" onclick="acceptRequest(this)">Accept</button>
                            <button type="button" onclick="rejectRequest(this)">Reject</button>
                        </div>
                    </div>
                    `
                );
            }else if(request_status == "accepted"){
                return (
                    `
                    <div class="person" id="user-${this.peopleObj.id}">
                        <div class="person-infor">${this.peopleObj.username}</div>
                        <div class="person-button">
                            <button type="button">Friend</button>
                        </div>
                    </div>
                    `
                );
            }else{
                return (
                    `
                    <div class="person" id="user-${this.peopleObj.id}">
                        <div class="person-infor">${this.peopleObj.username}</div>
                        <div class="person-button">
                            <button type="button" onclick="requestMessage(this)">Request Message</button>
                        </div>
                    </div>
                    `
                );
            }
        }else if(is_receiver){
            if(request_status == "pending"){
                return (
                    `
                    <div class="person" id="user-${this.peopleObj.id}">
                        <div class="person-infor">${this.peopleObj.username}</div>
                        <div class="person-button">
                            <button type="button" onclick="cancelRequest(this)">Cancel Request</button>
                        </div>
                    </div>
                    `
                );
            }else if(request_status == "accepted"){
                return (
                    `
                    <div class="person" id="user-${this.peopleObj.id}">
                        <div class="person-infor">${this.peopleObj.username}</div>
                        <div class="person-button">
                            <button type="button">Friend</button>
                        </div>
                    </div>
                    `
                );
            }else{
                return (
                    `
                    <div class="person" id="user-${this.peopleObj.id}">
                        <div class="person-infor">${this.peopleObj.username}</div>
                        <div class="person-button">
                            <button type="button" onclick="requestMessage(this)">Request Message</button>
                        </div>
                    </div>
                    `
                );
            }
        }else{
            return (
                `
                <div class="person" id="user-${this.peopleObj.id}">
                    <div class="person-infor">${this.peopleObj.username}</div>
                    <div class="person-button">
                        <button type="button" onclick="requestMessage(this)">Request Message</button>
                    </div>
                </div>
                `
            );
        }
    }

    show() {
        this.selfEl = document.createElement("div");
        this.selfEl.innerHTML = this.generateMarkup();
        this.parentEl.append(this.selfEl);
    }
}

const tableElement = document.querySelector(".people-table");
const user_id = tableElement.id.split("-")[1];

async function fetchData() {
    const response = await fetch(BASE_URL + `/api/request/get_people/${user_id}`)
    .then(res => {
        return res.json();
    });
    return response;
}

async function populateData(){
    let data = await fetchData();

    for (const d of data){
        console.log(d.user_id);
        const person = new PeopleModel(d.user_id, d.username, d.request_id, d.is_receiver, d.is_sender, d.request_status);
        person.show();
    }
}

populateData();

async function requestMessage(buttonElement){
    const person_id = buttonElement.parentElement.parentElement.id.split("-")[1];
    const request_time = Date.now();
    let sendResponse = await fetch(BASE_URL + `/api/request/send/${user_id}/${person_id}/${request_time}`, {
        method: "POST"
    });

    if (sendResponse.status === 200){
        buttonElement.innerHTML = "cancel request";
        buttonElement.setAttribute("onclick", "cancelRequest(this)");
    }
}

async function acceptRequest(buttonElement){
    const parent_button_elememt = buttonElement.parentElement
    const person_id = parent_button_elememt.parentElement.id.split("-")[1];
    const accepted_time = Date.now();
    let sendResponse = await fetch(BASE_URL + `/api/request/accept/${person_id}/${user_id}/${accepted_time}`, {
        method: "POST"
    });

    if (sendResponse.status === 200){
        parent_button_elememt.removeChild(buttonElement);
        parent_button_elememt.firstElementChild.innerHTML = "friend";
        parent_button_elememt.firstElementChild.removeAttribute("onclick");
    }
}

async function cancelRequest(buttonElement){
    const person_id = buttonElement.parentElement.parentElement.id.split("-")[1];
    const request_time = Date.now();
    let sendResponse = await fetch(BASE_URL + `/api/request/cancel/${user_id}/${person_id}`, {
        method: "POST"
    });

    if (sendResponse.status === 200){
        buttonElement.innerHTML = "request message";
        buttonElement.setAttribute("onclick", "requestMessage(this)");
    }
}

async function rejectRequest(buttonElement){
    const parent_button_elememt = buttonElement.parentElement
    const person_id = parent_button_elememt.parentElement.id.split("-")[1];
    let sendResponse = await fetch(BASE_URL + `/api/request/reject/${person_id}/${user_id}`, {
        method: "POST"
    });

    if (sendResponse.status === 200){
        parent_button_elememt.removeChild(buttonElement);
        parent_button_elememt.firstElementChild.innerHTML = "request message";
        parent_button_elememt.firstElementChild.setAttribute("onclick", "requestMessage(this)");
    }
}