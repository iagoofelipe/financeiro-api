import { getCookie } from "../utils.js";

export async function has_registries() {
    let response = await $.get({
        url: '/api/hasRegistries',
        headers: {
            'Authorization': localStorage.getItem('TOKEN_API'),
        }
    });

    return response.found;
}

export async function add_registry(data) {
    let response = {success: false, error: '', data: null};
    let default_error = 'Não foi possível adicionar o novo registro';

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

        response.success = true;
    } catch (e) {
        console.log('error while creating registry', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : default_error;
    }

    return response;
}

export async function update_registry(data) {
    let response = {success: false, error: '', data: null};
    let default_error = 'Não foi possível atualizar o registro';

    try {
        await $.ajax({
            url: '/api/updateRegistry',
            method: 'POST',
            data: JSON.stringify(data),
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        response.success = true;
    } catch (e) {
        console.log('error while updating registry', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : default_error;
    }

    return response;
}

export async function delete_registry(id) {
    let response = {success: false, error: '', data: null};
    let default_error = 'Não foi possível atualizar o registro';

    try {
        await $.ajax({
            url: `/api/deleteRegistry/${id}`,
            method: 'POST',
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        response.success = true;
    } catch (e) {
        console.log('error while updating registry', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : default_error;
    }

    return response;
}