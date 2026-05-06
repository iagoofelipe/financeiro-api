import { number_to_coin_format, get_status_html_by_name } from "../../tools/utils.js";
import Table from "./table.js";

export const MODEL_TRANSACTIONS = {
    title: 'Pessoais',
    num_late: 1,
    num_pending: 1,
    num_ok: 2,
    inputs: {
        total: 3700.34,
        last_update_msg: 'alterado há 1 dia atrás',
        values: [
            {
                title: 'Aula Teclado',
                value: 150,
                status: 'PENDING',
                occurranceDate: '10 Jan 26',
            },
            {
                title: 'Salário',
                value: 3000,
                status: 'LATE',
                occurranceDate: '07 Jan 26',
            },
            {
                title: 'Venda Skins CS',
                value: 550.34,
                status: 'OK',
                occurranceDate: '01 Jan 26',
            }
        ]
    },
    outputs: {
        total: 20.9,
        last_update_msg: 'alterado há 3 dia atrás',
        values: [
                {
                title: 'Netflix',
                value: 20.9,
                status: 'OK',
                occurranceDate: '28 Dez 25',
            }
        ]
    }
};

export const MODEL_TRANSACTIONS_2 = {
    title: 'Brunna Carvalho',
    num_late: 1,
    num_pending: 2,
    num_ok: 1,
    inputs: {
        total: 3700.34,
        last_update_msg: 'alterado há 5 dia atrás',
        values: [
            {
                title: 'Violão',
                value: 300,
                status: 'LATEa',
                occurranceDate: '07 Jan 26',
            },
            {
                title: 'Televisão (2/8)',
                value: 187.41,
                status: 'PENDING',
                occurranceDate: '08 Jan 26',
            },
        ]
    },
    outputs: {
        total: 231.51,
        last_update_msg: 'alterado há pouco',
        values: [
            {
                title: 'Pizza',
                value: 44,
                status: 'PENDING',
                occurranceDate: '25 Dez 25',
                card: 'Nubank',
            },
            {
                title: 'Televisão (2/8)',
                value: 187.41,
                status: 'OK',
                occurranceDate: '20 Jan 26, 08h10',
                card: 'Nubank',
            }
        ]
    }
};

export class TransactionCard {
    /* gera um card que compõe a view de transações na tela de registros */
    #ids;
    #jquery_element;
    
    constructor(transactions, parent) {
        this.#ids = {
            container: crypto.randomUUID(),
            tables_container: crypto.randomUUID(),
            btn_collapse: crypto.randomUUID(),
        }

        let desc_status = '';
        const desc_aux = {
            'Atrasado': transactions.num_late,
            'Pendente': transactions.num_pending,
            'Contabilizado': transactions.num_ok,
        };
        
        for (const text in desc_aux)
            desc_status += `<label class="title-3 me-3">${desc_aux[text]} ${text}${desc_aux[text] > 1? 's' : ''}</label>`;

        // substituindo valores na estrutura modelo
        let html = BODY_STRUCT
            .replaceAll('{CONTAINER_ID}', this.#ids.container)
            .replaceAll('{TITLE}', transactions.title)
            .replaceAll('{TOTAL_INPUTS}', number_to_coin_format(transactions.inputs.total))
            .replaceAll('{TOTAL_OUTPUTS}', number_to_coin_format(transactions.outputs.total))
            .replaceAll('{DESC_STATUS}', desc_status)
            .replaceAll('{TABLES_CONTAINER_ID}', this.#ids.tables_container)
            .replaceAll('{INPUT_LAST_UPDATE}', transactions.inputs.last_update_msg)
            .replaceAll('{BTN_COLLAPSE_ID}', this.#ids.btn_collapse);

        
        // necessário gerar antes de Table para que seja possível inserir no campo correto através de parent
        this.#jquery_element = $(html).appendTo(parent);

        let parent_tables = $('#'+this.#ids.tables_container);

        // gerando tabela de Entradas
        $(
            `<div class="d-flex justify-content-between align-items-center mb-3">
                <label class="title-2">Entradas</label>
                <label class="title-3">${transactions.inputs.last_update_msg}</label>
            </div>`
        ).appendTo(parent_tables);


        // tratando dados
        let input_values = [];
        transactions.inputs.values.forEach(row => {
            input_values.push([
                row.title,
                number_to_coin_format(row.value),
                get_status_html_by_name(row.status), 
                row.occurranceDate
            ]); // garantindo ordem dos dados
        });
        
        // inserindo tabela
        let table_inputs = new Table({
            parent: parent_tables,
            columns: ['Título', 'Valor', 'Status', 'Data de Ocorrência'],
            data: input_values
        });

        // gerando tabela de Saídas
        $(
            `<div class="d-flex justify-content-between align-items-center mt-3 mb-3">
                <label class="title-2">Saídas</label>
                <label class="title-3">${transactions.outputs.last_update_msg}</label>
            </div>`
        ).appendTo(parent_tables);

        // tratando dados
        let output_values = [];
        transactions.outputs.values.forEach(row => {
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
            parent: parent_tables,
            columns: ['Título', 'Valor', 'Status', 'Data de Ocorrência', 'Cartão'],
            data: output_values
        });
    }

    toggleExpand() {
        $('#'+this.#ids.btn_collapse).click();
    }
};

const BODY_STRUCT = `
<div class="card card-transaction p-3" id="{CONTAINER_ID}">
    <div class="d-flex flex-row align-items-center justify-content-between">
        <div>
            <p class="title mb-2">{TITLE}</p>
            <div class="d-flex flex-row card-transaction-desc">
                <i class="bi bi-plus-circle-fill me-1"></i>
                <label class="title-3 me-3">{TOTAL_INPUTS}</label>
                <i class="bi bi-dash-circle-fill me-1"></i>
                <label class="title-3 me-3">{TOTAL_OUTPUTS}</label>
                {DESC_STATUS}
            </div>
        </div>
        <button id="{BTN_COLLAPSE_ID}" class="btn border-0 p-0 btn-rotate" type="button" data-bs-toggle="collapse"
            data-bs-target="#{TABLES_CONTAINER_ID}" aria-expanded="false" aria-controls="{TABLES_CONTAINER_ID}">
            <i class="bi bi-chevron-up"></i>
        </button>
    </div>
    <div class="collapse" id="{TABLES_CONTAINER_ID}">
        <hr>
    </div>
</div>`;