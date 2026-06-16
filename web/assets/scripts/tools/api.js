export async function has_registries() {
    let response = await $.get({
        url: '/api/hasRegistries',
        headers: {
            'Authorization': localStorage.getItem('TOKEN_API'),
        }
    });

    return response.found;
}