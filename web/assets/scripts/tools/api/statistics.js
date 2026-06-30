import { DEFAULT_ERROR } from "../utils.js";

export async function values_by_category(params) {
    let response = {success: false, error: '', data: null};
    try {
        response.data = await $.ajax({
            url: '/api/valuesByCategory',
            data: params,
            method: 'GET',
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
            }
        });

        response.success = true;
    } catch (e) {
        // console.log('error while quering values by category', e);
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : DEFAULT_ERROR;
    }

    return response;
}

export async function balance(params) {
    let response = {success: false, error: '', data: null};
    try {
        response.data = await $.ajax({
            url: '/api/balance',
            data: params,
            method: 'GET',
            headers: {
                'Authorization': localStorage.getItem('TOKEN_API'),
            }
        });

        response.success = true;
    } catch (e) {
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : DEFAULT_ERROR;
    }

    return response;
}