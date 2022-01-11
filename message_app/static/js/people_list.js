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
                        </div>
                    </div>
                    `
                )
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
                )
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
                )
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
                )
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
                )
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
                )
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
            )
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
// let people = fetch(BASE_URL + `/api/request/get_people/${user_id}`)
// .then(response => {
//     console.log(response.json());
//     return response.json();
// });

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