import { TransactionCardView, TransactionDetailsView } from "./components/transactions.js";
import Table from "./components/table.js";
import RegistriesAPI from "../api/regs.js";

export default class RegistryView extends EventTarget {
    static templates = {};
    static templates_set = false;

    #jquery;
    #content_id;
    #detailsview;
    #transactions_by_id;
    #cards = [];
    #cardSelected = undefined;

    constructor(jquery, content_id, detailsview, transactions_by_id) {
        super();
        this.#jquery = jquery;
        this.#content_id = content_id;
        this.#detailsview = detailsview;
        this.#transactions_by_id = transactions_by_id;

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
            transactions_api = await RegistriesAPI.query({}),
            transactions = {},
            transactions_by_id = {};

        transactions_api.forEach(t => {
            let responsable = t.responsable_name ?? 'Pessoais';
            if (!(responsable in transactions)) {
                transactions[responsable] = {
                    title: responsable,
                    input_last_update: 'atualizado há poucos segundos',
                    output_last_update: 'atualizado há poucos segundos',
                    values: [],
                };
            }

            transactions[responsable].values.push(t);
            transactions_by_id[t.id] = t;
        });

        let instance = new RegistryView(jquery, content_id, detailsview, transactions_by_id);
        for (const k in transactions)
            await instance.addCard(transactions[k]);

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
        this.showDetails(this.#transactions_by_id[evt.detail.transactionId]);
    }

    static #template_body(card_details_id, content_id) {
        return this.templates.BODY
            .replaceAll('{CARD_DETAILS_ID}', card_details_id)
            .replaceAll('{CONTENT_ID}', content_id);
    }
}