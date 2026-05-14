export default class RegistriesAPI {
    static async query(params) {
        return await $.get({
            url: '/api/regs/',
            headers: {
                Authorization: 'Token d6dd883d9a7cb2ee7694052eeef62ff857f46838', // TODO: o projeto utiliza apenas uma base de dados local, não sendo um risco de segurança estar exposto enquanto em ambiente de teste
            },
            data: params,
        });
    }
}