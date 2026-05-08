import { number_to_coin_format, get_status_html_by_name } from "../../tools/utils.js";
import Table from "./table.js";

export class TransactionCardView extends EventTarget {
    /* gera um card que compõe a view de transações na tela de registros */
    #ids;
    #transactions;
    #info;
    #jquery;
    #table_in;
    #table_out;

    static templates = {};
    static templates_set = false;
    static EVENTS = {
        TRANSACTION_SELECTED: 'financeiro-api:component-transactioncardview:selection',
    };

    constructor(transactions, info, ids, jquery, table_in, table_out) {
        super();

        this.#transactions = transactions;
        this.#info = info;
        this.#ids = ids;
        this.#jquery = jquery;
        this.#table_in = table_in;
        this.#table_out = table_out;

        // vinculando eventos
        table_in.addEventListener(Table.EVENTS.ROW_CLICKED, (evt) => this.#on_table_rowSelected(true, evt));
        table_out.addEventListener(Table.EVENTS.ROW_CLICKED, (evt) => this.#on_table_rowSelected(false, evt));

        table_in.bindTable(table_out); // quando um for selecionado, o outro é desselecionado
    }

    static async create(transactions, parent) {
        await this.loadTemplates();

        let ids = {
                container: crypto.randomUUID(),
                tables_container: crypto.randomUUID(),
                btn_collapse: crypto.randomUUID(),
            },
            inputs = transactions.values.filter(obj => obj.typeIn),
            outputs = transactions.values.filter(obj => !obj.typeIn),
            info = {
                inputs: inputs,
                outputs: outputs,
                num_late: transactions.values.filter(obj => obj.status == 'LATE').length,
                num_ok: transactions.values.filter(obj => obj.status == 'OK').length,
                num_pending: transactions.values.filter(obj => obj.status == 'PENDING').length,
                sum_inputs: inputs.reduce((prev, obj) => prev + obj.value ?? 0, 0),
                sum_outputs: outputs.reduce((prev, obj) => prev + obj.value ?? 0, 0),
            },
            jquery = $(this.#template_body(ids, transactions, info)).appendTo(parent),
            parent_tables = $('#' + ids.tables_container);

        // gerando tabela de Entradas
        $(this.#template_table_title('Entradas', transactions.input_last_update)).appendTo(parent_tables);
        let input_values = [];
        info.inputs.forEach(row => {
            input_values.push([
                row.id,
                row.title,
                number_to_coin_format(row.value),
                get_status_html_by_name(row.status),
                row.occurranceDate
            ]); // garantindo ordem dos dados
        });

        // inserindo tabela
        let table_in = await Table.create({
            parent: parent_tables,
            flags: Table.FLAGS.ROW_SELECTABLE,
            columns: ['ID', 'Título', 'Valor', 'Status', 'Data de Ocorrência'],
            data: input_values,
            indexId: 0,
            indexHiddenColumns: [0],
        });

        // gerando tabela de Saídas
        $(this.#template_table_title('Saídas', transactions.output_last_update)).appendTo(parent_tables);
        let output_values = [];
        info.outputs.forEach(row => {
            output_values.push([
                row.id,
                row.title,
                number_to_coin_format(row.value),
                get_status_html_by_name(row.status),
                row.occurranceDate,
                row.card ?? ''
            ]); // garantindo ordem dos dados
        });

        // inserindo tabela
        let table_out = await Table.create({
            parent: parent_tables,
            flags: Table.FLAGS.ROW_SELECTABLE,
            columns: ['ID', 'Título', 'Valor', 'Status', 'Data de Ocorrência', 'Cartão'],
            data: output_values,
            indexId: 0,
            indexHiddenColumns: [0],
        });

        return new TransactionCardView(transactions, info, ids, jquery, table_in, table_out);
    }
    
    jquery() { return this.#jquery; }
    tableInputs() { return this.#table_in; }
    tableOutputs() { return this.#table_out; }

    #on_table_rowSelected(typeIn, evt) {
        let data = {
            transactionId: evt.detail.id,
            typeIn: typeIn,
        };
        this.dispatchEvent(new CustomEvent(TransactionCardView.EVENTS.TRANSACTION_SELECTED, {detail: data}));
    }

    unselect() {
        this.#table_in.unselect();
        this.#table_out.unselect();
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        if (this.templates_set)
            return;

        this.templates_set = true;
        this.templates.BODY = await $.get('/templates', { template: 'home/regs/transaction-card.html' });
        this.templates.TABLE_TITLE = await $.get('/templates', { template: 'home/regs/transaction-card-table-title.html' });
    }

    static #template_body(ids, transactions, info) {
        let desc_status = '',
            desc_aux = {
                'Atrasado': info.num_late,
                'Pendente': info.num_pending,
                'Contabilizado': info.num_ok,
            };

        for (const text in desc_aux)
            desc_status += `<label class="title-3 me-3">${desc_aux[text]} ${text}${desc_aux[text] > 1 ? 's' : ''}</label>`;

        return this.templates.BODY
            .replaceAll('{CONTAINER_ID}', ids.container)
            .replaceAll('{TITLE}', transactions.title)
            .replaceAll('{TOTAL_INPUTS}', number_to_coin_format(info.sum_inputs))
            .replaceAll('{TOTAL_OUTPUTS}', number_to_coin_format(info.sum_outputs))
            .replaceAll('{DESC_STATUS}', desc_status)
            .replaceAll('{TABLES_CONTAINER_ID}', ids.tables_container)
            .replaceAll('{BTN_COLLAPSE_ID}', ids.btn_collapse);
    }

    static #template_table_title(title, last_update) {
        return this.templates.TABLE_TITLE
            .replace('{TITLE}', title)
            .replace('{LAST_UPDATE}', last_update);
    }
};


export class TransactionDetailsView extends EventTarget {
    static templates = {};
    static templates_set = false;
    static EVENTS = {
        HIDE: 'financeiro-api:component-transactiondetailsview:hide'
    };

    #ids = {};
    #jquery;

    constructor(ids, jquery) {
        super();

        this.#ids = ids;
        this.#jquery = jquery;

        $('#'+ids.BTN_HIDE).click((evt) => this.#on_btnHide_clicked());
    }

    static async create(parent, visible) {
        await this.loadTemplates();

        let ids = {
                CONTAINER: crypto.randomUUID(),
                FIELD_TITLE: crypto.randomUUID(),
                BTN_HIDE: crypto.randomUUID(),
                FIELD_TYPE: crypto.randomUUID(),
                FIELD_VALUE: crypto.randomUUID(),
                FIELD_OWNER: crypto.randomUUID(),
                FIELD_OCCURRENCE: crypto.randomUUID(),
                FIELD_DESCRIPTION: crypto.randomUUID(),
                FIELD_STATUS: crypto.randomUUID(),
                FIELD_CARD: crypto.randomUUID(),
            },
            jquery = $(this.#template_body(ids)).appendTo(parent);
        
        if (!visible)
            jquery.hide();

        return new TransactionDetailsView(ids, jquery);
    }

    setData(transaction, show) {
        $('#'+this.#ids.FIELD_TITLE).text(transaction.title);
        $('#'+this.#ids.FIELD_TYPE).text(transaction.typeIn? 'Entrada' : 'Saída');
        $('#'+this.#ids.FIELD_VALUE).text(number_to_coin_format(transaction.value));
        $('#'+this.#ids.FIELD_OWNER).text('');
        $('#'+this.#ids.FIELD_OCCURRENCE).text(transaction.occurranceDate);
        $('#'+this.#ids.FIELD_DESCRIPTION).text(transaction.description);
        $('#'+this.#ids.FIELD_STATUS).html(get_status_html_by_name(transaction.status));
        $('#'+this.#ids.FIELD_CARD).text(transaction.card ?? '');

        if (show ?? true)
            this.#jquery.show();
    }

    #on_btnHide_clicked() {
        this.#jquery.hide();
        this.dispatchEvent(new CustomEvent(TransactionDetailsView.EVENTS.HIDE));
    }

    static async loadTemplates() {
        if (this.templates_set)
            return;

        this.templates_set = true;
        this.templates.BODY = await $.get('/templates', { template: 'home/regs/transaction-details.html' });
    }

    static #template_body(ids) {
        return this.templates.BODY
            .replaceAll('{CONTAINER_ID}', ids.CONTAINER)
            .replaceAll('{FIELD_TITLE_ID}', ids.FIELD_TITLE)
            .replaceAll('{BTN_HIDE_ID}', ids.BTN_HIDE)
            .replaceAll('{FIELD_TYPE_ID}', ids.FIELD_TYPE)
            .replaceAll('{FIELD_VALUE_ID}', ids.FIELD_VALUE)
            .replaceAll('{FIELD_OWNER_ID}', ids.FIELD_OWNER)
            .replaceAll('{FIELD_OCCURRENCE_ID}', ids.FIELD_OCCURRENCE)
            .replaceAll('{FIELD_DESCRIPTION_ID}', ids.FIELD_DESCRIPTION)
            .replaceAll('{FIELD_STATUS_ID}', ids.FIELD_STATUS)
            .replaceAll('{FIELD_CARD_ID}', ids.FIELD_CARD);
    }
};