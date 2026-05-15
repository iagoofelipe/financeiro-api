import { TransactionCardView, TransactionDetailsView } from "./components/transactions.js";
import Table from "./components/table.js";
import RegistriesAPI from "../api/regs.js";
import { number_to_coin_format } from "../tools/utils.js";

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

        let total_inputs = 0, total_outputs = 0,
            transactions_api = await RegistriesAPI.query({}),
            transactions = {}, transactions_by_id = {};

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

            // contagens e somas
            if (t.type_in)
                total_inputs += t.value;
            else
                total_outputs += t.value;
        });

        let
            content_id = crypto.randomUUID(),
            card_details_id = crypto.randomUUID(),
            jquery = $(parent).html(this.#template_body(total_inputs, total_outputs, card_details_id, content_id)),
            detailsview = await TransactionDetailsView.create('#'+card_details_id, false),
            instance = new RegistryView(jquery, content_id, detailsview, transactions_by_id);

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

    static #template_body(total_inputs, total_outputs, card_details_id, content_id) {
        return this.templates.BODY
            .replaceAll('{TOTAL_INPUTS}', number_to_coin_format(total_inputs))
            .replaceAll('{TOTAL_OUTPUTS}', number_to_coin_format(total_outputs))
            // .replaceAll('{DESC_STATUS}', desc_status)
            .replaceAll('{CONTENT_ID}', content_id)
            .replaceAll('{CARD_DETAILS_ID}', card_details_id);
    }
}