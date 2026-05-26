import { getCookie, modal, MODAL_FLAGS, set_modal } from "./tools/utils.js";

$(() => {
    $('#btn-login').on('click', on_login);
});

async function on_login() {
    const username = $('#inp-username').val();
    const password = $('#inp-password').val();

    if (!username || !password) {
        set_modal('Validação de Parâmetros', 'preencha todos os campos!', true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
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
            set_modal('Autenticação de Usuário', 'usuário ou senha incorretos!', true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
            return;
        }
        
        set_modal('Autenticação de Usuário', 'erro interno inesperado', true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
        return;
    }

    localStorage.setItem('TOKEN_API', 'Token ' + response.token);
    window.location.reload();
}
