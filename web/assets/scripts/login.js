import { getCookie } from "./tools/utils.js";

$(() => {
    $('#btn-login').on('click', on_login);
});

async function on_login() {
    const username = $('#inp-username').val();
    const password = $('#inp-password').val();

    if (!username || !password) {
        alert('preencha todos os campos!');
        return;
    }

    let response;

    try {
        response = await $.ajax({
            url: '/login/auth',
            method: 'POST',
            data: {
                username: username,
                password: password,
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

    } catch (e) {
        console.log('Error', e);

        if (e.status == 400) {
            alert('usuário ou senha incorretos!');
            return;
        }
        
        alert('erro inesperado');
        return;
    }

    localStorage.setItem('TOKEN_API', 'Token ' + response.token);
    window.location.reload();
}
