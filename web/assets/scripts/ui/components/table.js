export default class Table extends EventTarget {
    #id = '';
    #dataIds = [];
    #indexHiddenColumns;
    #flags;
    #currentSelection = {
        index: -1,
        id: undefined,
        jquery: undefined,
    };
    #binds = [];

    static EVENTS = {
        ROW_CLICKED: 'financeiro-api:component-table:row-click',
    };
    static FLAGS = {
        ROW_SELECTABLE: 1 << 1,
    };

    constructor(params) {
        super();

        this.#id = crypto.randomUUID();
        this.#indexHiddenColumns = params.indexHiddenColumns;
        this.#flags = params.flags ?? 0;

        let thead = $('<thead>'),
            tbody = $('<tbody>'),
            row_cols = $('<tr><th scope="col" hidden>Index</th></tr>').appendTo(thead);
        
        if (params.columns) {
            const num_cols = params.columns.length;

            // headers
            for (let i=0; i < num_cols; i++) {
                $(`<th scope="col" ${this.#hidden_column(i)? 'hidden' : ''}>${params.columns[i]}</th>`).appendTo(row_cols);
            }

            // content
            if (params.data) {
                for (let index_row=0; index_row < params.data.length; index_row++) {
                    let row = $(`<tr><td hidden>${index_row}</td></tr>`);
                    let data = params.data[index_row];

                    // armazenando valor de identificação (ID)
                    if (params.indexId != undefined)
                        this.#dataIds.push(data[params.indexId]);
                    
                    for (let index_col=0; index_col < data.length && index_col < num_cols; index_col++) {
                        $(`<td ${this.#hidden_column(index_col)? 'hidden' : ''}>${data[index_col]}</td>`).appendTo(row);
                    }

                    row.appendTo(tbody);
                }
            }
        }

        $(`<div class="table-responsive" id="${this.#id}">`)
            .append(
                $('<table class="table table-hover m-0">')
                    .append(thead)
                    .append(tbody)
            )
            .appendTo(params.parent)
            .on('click', 'tbody tr', (evt) => this.#emit_row_clicked(evt));
    }

    selection() { return this.#currentSelection; }

    unselect() {
        if (!this.#currentSelection.jquery)
            return;

        if (this.#flags & Table.FLAGS.ROW_SELECTABLE)
            this.#currentSelection.jquery.removeClass('table-active');
        
        this.#currentSelection.index = -1;
        this.#currentSelection.id = undefined;
        this.#currentSelection.jquery = undefined;
    }

    bindTable(table) {
        if (this.#binds.indexOf(table) != -1)
            return;

        this.#binds.push(table);
        table.bindTable(this); // necessário quando o evento for emitido da outra tabela
    }

    static async create(params) {
        // async logic...
        return new Table(params);
    }

    #emit(evt_id, data) {
        let evt = new CustomEvent(evt_id, {detail: data});
        this.dispatchEvent(evt);
    }

    #emit_row_clicked(evt) {
        const index = parseInt(evt.currentTarget.cells[0].innerText); // corresponde a primeira coluna, definida como Index
        let jquery = $(evt.currentTarget);
        
        if (this.#flags & Table.FLAGS.ROW_SELECTABLE) {
            if (index == this.#currentSelection.index) // ignora caso a linha clicada já esteja selecionada
                return;

            if (this.#currentSelection.jquery)
                    this.#currentSelection.jquery.removeClass('table-active');
            
            jquery.addClass('table-active');
        }
            
        this.#currentSelection = {
            index: index,
            id: this.#dataIds[index],
            jquery: jquery,
        };

        // removendo seleções de tabelas vinculadas
        this.#binds.forEach(e => e.unselect());

        this.dispatchEvent(new CustomEvent(Table.EVENTS.ROW_CLICKED, {detail: this.#currentSelection}));
    }
        
    #hidden_column(index_col) {
        return this.#indexHiddenColumns? (this.#indexHiddenColumns.indexOf(index_col) != -1) : false;
    }
}