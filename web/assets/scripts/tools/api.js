import { getCookie } from "./utils.js";

export async function has_registries() {
    let response = await $.get({
        url: '/api/hasRegistries',
        headers: {
            'Authorization': localStorage.getItem('TOKEN_API'),
        }
    });

    return response.found;
}

export async function add_card(data) {
    try {
        await $.ajax({
            url: '/api/addCard',
            method: 'POST',
            data: JSON.stringify(data),
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        return true;
    } catch (error) {
        console.log('error while creating card', error);
        return false;
    }
}

export async function add_registry(data) {
    try {
        await $.ajax({
            url: '/api/addRegistry',
            method: 'POST',
            data: JSON.stringify(data),
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        return true;
    } catch (error) {
        console.log('error while creating registry', error);
        return false;
    }
}