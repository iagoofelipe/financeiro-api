import { TransactionCardView } from "./components/transactions.js";

const ARRAY_TRANSACTIONS = [
    {
        "title": "Pessoais",
        "input_last_update": "alterado há 1 dia atrás",
        "output_last_update": "alterado há 3 dia atrás",
        "values": [
            {
                "title": "Aula Teclado",
                "value": 150,
                "status": "PENDING",
                "occurranceDate": "10 Jan 26",
                "typeIn": true
            },
            {
                "title": "Salário",
                "value": 3000,
                "status": "LATE",
                "occurranceDate": "07 Jan 26",
                "typeIn": true
            },
            {
                "title": "Venda Skins CS",
                "value": 550.34,
                "status": "OK",
                "occurranceDate": "01 Jan 26",
                "typeIn": true
            },
            {
                "title": "Netflix",
                "value": 20.9,
                "status": "OK",
                "occurranceDate": "28 Dez 25",
                "typeIn": false,
                "card": "Nubank"
            },
            {
                "title": "Almoço",
                "value": 23,
                "status": "OK",
                "occurranceDate": "29 Dez 25",
                "typeIn": false
            }
        ]
    },
    {
        "title": "Brunna Carvalho",
        "input_last_update": "alterado há 5 dia atrás",
        "output_last_update": "alterado há pouco",
        "values": [
            {
                "title": "Violão",
                "value": 300,
                "status": "LATE",
                "occurranceDate": "07 Jan 26",
                "typeIn": true
            },
            {
                "title": "Televisão (2/8)",
                "value": 187.41,
                "status": "PENDING",
                "occurranceDate": "08 Jan 26",
                "typeIn": true
            },
            {
                "title": "Pizza",
                "value": 44,
                "status": "PENDING",
                "occurranceDate": "25 Dez 25",
                "card": "Nubank",
                "typeIn": false
            },
            {
                "title": "Televisão (2/8)",
                "value": 187.41,
                "status": "OK",
                "occurranceDate": "20 Jan 26, 08h10",
                "card": "Nubank",
                "typeIn": false
            }
        ]
    }
]

export default class RegistryView {
    static templates = {};
    static templates_set = false;

    async setContent(parent) {
        if (!RegistryView.templates_set)
            await RegistryView.loadTemplates();

        let html = RegistryView.templates.BODY
            .replaceAll('{CARD_DETAILS_ID}', crypto.randomUUID());

        $(parent).html(html);
        for (const index in ARRAY_TRANSACTIONS) {
            let card = new TransactionCardView(ARRAY_TRANSACTIONS[index]);
            await card.setContent('#reg-transactions');
        }
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        if (this.templates_set)
            return;
        
        this.templates_set = true;
        RegistryView.templates.BODY = await $.get('/templates', {template: 'home/regs/index.html'});
    }
}