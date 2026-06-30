import { getCookie, DEFAULT_ERROR } from "../utils.js";

export async function add_card(data) {
    let response = {success: false, error: '', data: null};

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

        response.success = true;
    } catch (e) {
        console.log('error while creating card', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : DEFAULT_ERROR;
    }

    return response;
}

export async function get_cards() {
    let response = {success: false, error: '', data: null};

    try {
        response.data = await $.ajax({
            url: '/api/getCards',
            method: 'GET',
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
            }
        });

        response.success = true;
    } catch (e) {
        console.log('error while querying cards', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : DEFAULT_ERROR;
    }
    
    return response;
}

export async function get_invoice_by_card(params) {
    let response = {success: false, error: '', data: null};

    try {
        response.data = await $.ajax({
            url: '/api/getInvoiceByCard',
            method: 'GET',
            data: params,
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
            }
        });

        response.success = true;
    } catch (e) {
        // console.log('error while querying invoice by card', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : DEFAULT_ERROR;
    }
    
    return response;
}