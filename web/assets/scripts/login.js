import { getCookie, MODAL_FLAGS, set_modal } from "./tools/utils.js";

$(() => {
    $('#btn-auth').on('click', on_auth);
    $('#btn-create').on('click', on_create);
});

async function on_auth() {
    const username = $('#inp-username').val();
    const password = $('#inp-password').val();
    
    if (!username || !password) {
        set_modal('Validação de Parâmetros', 'preencha todos os campos!', true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
        return;
    }
    
    let response;
    const form_controls = $('#login-inputs .form-control, #login-inputs .btn');
    form_controls.prop('disabled', true);
    
    try {
        response = await $.ajax({
            url: '/login/auth',
            method: 'POST',
            data: JSON.stringify({
                username: username,
                password: password,
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

    } catch (e) {
        const detail = (e.responseJSON && e.responseJSON.detail) ? e.responseJSON.detail : 'erro interno inesperado';
        set_modal('Autenticação de Usuário', detail, true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
        form_controls.prop('disabled', false);
        return;
    }

    localStorage.setItem('TOKEN_API', 'Token ' + response.token);
    window.location.reload();
}

async function on_create() {
    let inputs = {};
    let inp_components = $('#container-login .form-control');
    let len = inp_components.length;
    let any_empty = false;

    for (let i = 0; i < len; i++) {
        let component = $(inp_components[i]);
        let val = component.val();
        inputs[component.attr('name')] = val;
        any_empty |= !val;
    }

    if (any_empty) {
        set_modal('Validação de parâmetros', 'Preencha todos os campos!', true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
        return;
    }

    if (inputs.password != inputs.password_confirm) {
        set_modal('Validação de parâmetros', 'As senhas são diferentes!', true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
        return;
    }
    
    let response;
    let form_controls = $('#container-login .form-control');
    form_controls.prop('disabled', true);

    try {
        response = await $.ajax({
            url: '/api/createAccount',
            method: 'POST',
            data: JSON.stringify(inputs),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });
    } catch (e) {
        const detail = (e.responseJSON && e.responseJSON.detail) ? e.responseJSON.detail : 'erro interno inesperado';
        set_modal('Criação de Usuário', detail, true, MODAL_FLAGS.HIDE_HEADER_BTN_CLOSE);
        form_controls.prop('disabled', false);
        return;
    }

    window.location.href = '/login';
}
