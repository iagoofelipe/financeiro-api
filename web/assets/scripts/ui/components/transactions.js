import { number_to_coin_format, get_status_html_by_name } from "../../tools/utils.js";
import Table from "./table.js";

export class TransactionCardView {
    /* gera um card que compõe a view de transações na tela de registros */
    #ids = {};
    #transactions;
    #info = {
        inputs: [], outputs: [],
        num_late: 0, num_ok: 0, num_pending: 0,
        sum_inputs: 0, sum_outputs: 0,
    };

    static templates = {};
    static templates_set = false;

    constructor(transactions) {
        this.#transactions = transactions;
        this.#info.inputs = transactions.values.filter(obj => obj.typeIn);
        this.#info.outputs = transactions.values.filter(obj => !obj.typeIn);
        this.#info.num_late = transactions.values.filter(obj => obj.status == 'LATE').length;
        this.#info.num_ok = transactions.values.filter(obj => obj.status == 'OK').length;
        this.#info.num_pending = transactions.values.filter(obj => obj.status == 'PENDING').length;
        this.#info.sum_inputs = this.#info.inputs.reduce((prev, obj) => prev + obj.value, 0);
        this.#info.sum_outputs = this.#info.outputs.reduce((prev, obj) => prev + obj.value, 0);
    }

    async setContent(parent) {
        this.#ids.container = crypto.randomUUID();
        this.#ids.tables_container = crypto.randomUUID();
        this.#ids.btn_collapse = crypto.randomUUID();

        if (!TransactionCardView.templates_set)
            await TransactionCardView.loadTemplates();
        
        let
            templates = TransactionCardView.templates,
            desc_status = '',
            desc_aux = {
                'Atrasado': this.#info.num_late,
                'Pendente': this.#info.num_pending,
                'Contabilizado': this.#info.num_ok,
            };

        for (const text in desc_aux)
            desc_status += `<label class="title-3 me-3">${desc_aux[text]} ${text}${desc_aux[text] > 1 ? 's' : ''}</label>`;

        // substituindo valores na estrutura modelo
        let html = templates.BODY
            .replaceAll('{CONTAINER_ID}', this.#ids.container)
            .replaceAll('{TITLE}', this.#transactions.title)
            .replaceAll('{TOTAL_INPUTS}', number_to_coin_format(this.#info.sum_inputs))
            .replaceAll('{TOTAL_OUTPUTS}', number_to_coin_format(this.#info.sum_outputs))
            .replaceAll('{DESC_STATUS}', desc_status)
            .replaceAll('{TABLES_CONTAINER_ID}', this.#ids.tables_container)
            .replaceAll('{BTN_COLLAPSE_ID}', this.#ids.btn_collapse);


        // necessário gerar antes de Table para que seja possível inserir no campo correto através de parent
        $(html).appendTo(parent);

        let parent_tables = $('#' + this.#ids.tables_container);

        // gerando tabela de Entradas
        const inputs_title_html = templates.TABLE_TITLE
            .replace('{TITLE}', 'Entradas')
            .replace('{LAST_UPDATE}', this.#transactions.input_last_update);
            
        $(inputs_title_html).appendTo(parent_tables);

        // tratando dados
        let input_values = [];
        this.#info.inputs.forEach(row => {
            input_values.push([
                row.title,
                number_to_coin_format(row.value),
                get_status_html_by_name(row.status),
                row.occurranceDate
            ]); // garantindo ordem dos dados
        });

        // inserindo tabela
        let table_inputs = new Table({
            columns: ['Título', 'Valor', 'Status', 'Data de Ocorrência'],
            data: input_values
        });
        await table_inputs.setContent(parent_tables);

        // gerando tabela de Saídas
        const outputs_title_html = templates.TABLE_TITLE
            .replace('{TITLE}', 'Saídas')
            .replace('{LAST_UPDATE}', this.#transactions.output_last_update);

        $(outputs_title_html).appendTo(parent_tables);

        // tratando dados
        let output_values = [];
        this.#info.outputs.forEach(row => {
            output_values.push([
                row.title,
                number_to_coin_format(row.value),
                get_status_html_by_name(row.status),
                row.occurranceDate,
                row.card ?? ''
            ]); // garantindo ordem dos dados
        });

        // inserindo tabela
        let table_outputs = new Table({
            columns: ['Título', 'Valor', 'Status', 'Data de Ocorrência', 'Cartão'],
            data: output_values
        });
        await table_outputs.setContent(parent_tables);
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        if (this.templates_set)
            return;

        this.templates_set = true;
        TransactionCardView.templates.BODY = await $.get('/templates', { template: 'home/regs/transaction-card.html' });
        TransactionCardView.templates.TABLE_TITLE = await $.get('/templates', { template: 'home/regs/transaction-card-table-title.html' });
    }
};


export class TransactionDetailsView {

};