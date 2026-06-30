export async function values_by_category(params) {
    let response = {success: false, error: '', data: null};
    // let default_error = 'Não foi possível realizar a operação';

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
        response.error = (e.responseJSON && e.responseJSON.detail)? e.responseJSON.detail : default_error;
    }

    return response;
}