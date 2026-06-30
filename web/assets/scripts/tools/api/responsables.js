import { getCookie } from "../utils.js";

export async function add_responsable(data) {
    let response = {success: false, error: '', data: null};
    let default_error = 'Não foi possível adicionar o novo responsável';

    try {
        await $.ajax({
            url: '/api/addResponsable',
            method: 'POST',
            data: JSON.stringify(data),
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        response.success = true;
    } catch (e) {
        console.log('error while creating responsable', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : default_error;
    }

    return response;
}

export async function get_responsables() {
    let response = {success: false, error: '', data: null};
    let default_error = 'Não foi possível consultar os responsáveis';

    try {
        response.data = await $.ajax({
            url: '/api/getResponsables',
            method: 'GET',
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
            }
        });

        response.success = true;
    } catch (e) {
        console.log('error while querying responsables', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : default_error;
    }
    
    return response;
}