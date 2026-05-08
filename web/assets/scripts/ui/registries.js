import { TransactionCardView, TransactionDetailsView } from "./components/transactions.js";
import Table from "./components/table.js";

const ARRAY_TRANSACTIONS = [
    {
        "title": "Pessoais",
        "input_last_update": "alterado há 1 dia atrás",
        "output_last_update": "alterado há 3 dia atrás",
        "values": [
            {
                "id": "32c5153e94-5f4e23a3773bbff2",
                "title": "Aula Teclado",
                "value": 150,
                "status": "PENDING",
                "occurranceDate": "10 Jan 26",
                "description": "",
                "typeIn": true
            },
            {
                "id": "32c5153ebd-b56d86c08ea51ddf",
                "title": "Salário",
                "value": 3000,
                "status": "LATE",
                "occurranceDate": "07 Jan 26",
                "description": "",
                "typeIn": true
            },
            {
                "id": "32c5153ec1-97a83016e8dcb6ed",
                "title": "Venda Skins CS",
                "value": 550.34,
                "status": "OK",
                "occurranceDate": "01 Jan 26",
                "description": "Skin Romanov",
                "typeIn": true
            },
            {
                "id": "32c5153ec4-ccbbc8c2ad7490a1",
                "title": "Netflix",
                "value": 20.9,
                "status": "OK",
                "occurranceDate": "28 Dez 25",
                "description": "",
                "card": "Nubank",
                "typeIn": false
            },
            {
                "id": "32c5153ec6-e16195c05c71c568",
                "title": "Almoço",
                "value": 23,
                "status": "OK",
                "occurranceDate": "29 Dez 25",
                "description": "Almoço no BK com Peixoto",
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
                "id": "32c5153edb-693eb0b67ad7888d",
                "title": "Violão",
                "value": 300,
                "status": "LATE",
                "occurranceDate": "07 Jan 26",
                "description": "",
                "typeIn": true
            },
            {
                "id": "32c5153edd-9a2b4b85ca87717f",
                "title": "Televisão (2/8)",
                "value": 187.41,
                "status": "PENDING",
                "occurranceDate": "08 Jan 26",
                "description": "",
                "typeIn": true
            },
            {
                "id": "32c5153ee0-a1f2f35095f1a961",
                "title": "Pizza",
                "value": 44,
                "status": "PENDING",
                "occurranceDate": "25 Dez 25",
                "description": "",
                "card": "Nubank",
                "typeIn": false
            },
            {
                "id": "32c5153ee2-c6bfcef0dd057eb4",
                "title": "Televisão (2/8)",
                "value": 187.41,
                "status": "OK",
                "occurranceDate": "20 Jan 26, 08h10",
                "description": "",
                "card": "Nubank",
                "typeIn": false
            }
        ]
    }
]

let _transactions_by_id = {};
ARRAY_TRANSACTIONS.forEach(t => t.values.forEach(v => _transactions_by_id[v.id] = v));
const TRANSACTIONS_BY_ID = _transactions_by_id;

export default class RegistryView extends EventTarget {
    static templates = {};
    static templates_set = false;

    #jquery;
    #content_id;
    #detailsview;
    #cards = [];
    #cardSelected = undefined;

    constructor(jquery, content_id, detailsview) {
        super();
        this.#jquery = jquery;
        this.#content_id = content_id;
        this.#detailsview = detailsview;

        detailsview.addEventListener(TransactionDetailsView.EVENTS.HIDE, (evt) => {
            if (!this.#cardSelected)
                return;

            this.#cardSelected.unselect();
            this.#cardSelected = undefined;
        });
    }

    static async create(parent) {
        if (!RegistryView.templates_set) {
            RegistryView.templates.BODY = await $.get('/templates', {template: 'home/regs/index.html'});
            this.templates_set = true;
        }

        let
            content_id = crypto.randomUUID(),
            card_details_id = crypto.randomUUID(),
            jquery = $(parent).html(this.#template_body(card_details_id, content_id)),
            detailsview = await TransactionDetailsView.create('#'+card_details_id, false),
            instance = new RegistryView(jquery, content_id, detailsview);

        for (const index in ARRAY_TRANSACTIONS)
            await instance.addCard(ARRAY_TRANSACTIONS[index]);
        
        return instance;
    }

    async addCard(transactions) {
        let card = await TransactionCardView.create(transactions, '#'+this.#content_id);
        card.addEventListener(TransactionCardView.EVENTS.TRANSACTION_SELECTED, (e) => this.#on_transactionCard_transactionSelected(e));

        this.#cards.push(card);
    }

    showDetails(transacion) {
        this.#detailsview.setData(transacion);
    }

    jquery() { return this.#jquery; }

    #on_transactionCard_transactionSelected(evt) {
        if (this.#cardSelected && this.#cardSelected != evt.target) { // removendo seleção anterior
            this.#cardSelected.unselect();
        }

        this.#cardSelected = evt.target;
        this.showDetails(TRANSACTIONS_BY_ID[evt.detail.transactionId]);
    }

    static #template_body(card_details_id, content_id) {
        return this.templates.BODY
            .replaceAll('{CARD_DETAILS_ID}', card_details_id)
            .replaceAll('{CONTENT_ID}', content_id);
    }
}