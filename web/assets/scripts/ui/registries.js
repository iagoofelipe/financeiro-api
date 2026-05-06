import { MODEL_TRANSACTIONS, MODEL_TRANSACTIONS_2, TransactionCard } from "./components/transactioncard.js";

export default class RegistryView {
    #url = '/home/nav-regs';

    constructor() {
        
    }

    async updateContent(parent) {
        $(parent).html(await $.get(this.#url));
        let card_1 = new TransactionCard(MODEL_TRANSACTIONS, '#reg-transactions');
        let card_2 = new TransactionCard(MODEL_TRANSACTIONS_2, '#reg-transactions');
    }
}