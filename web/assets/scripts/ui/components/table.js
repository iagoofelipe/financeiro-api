export default class Table {
    #columns = [];
    #data = {};

    constructor(params) {
        this.#columns = params.columns;
        this.#data = params.data;
    }
    
    async setContent(parent) {
        let thead = $('<thead>');
        let tbody = $('<tbody>');
        
        if (this.#columns) {
            let row = $('<tr>');
            const num_cols = this.#columns.length;

            // headers
            for (let i=0; i < num_cols; i++) {
                $(`<th scope="col">${this.#columns[i]}</th>`).appendTo(row);
            }

            row.appendTo(thead);

            // content
            if (this.#data) {
                for (let index_row=0; index_row < this.#data.length; index_row++) {
                    let row = $('<tr>');
                    let data = this.#data[index_row];
                    
                    for (let index_col=0; index_col < data.length && index_col < num_cols; index_col++) {
                        $(`<td>${data[index_col]}</td>`).appendTo(row);
                    }

                    row.appendTo(tbody);
                }
            }
        }

        $('<div class="table-responsive">')
            .append(
                $('<table class="table table-hover m-0">')
                    .append(thead)
                    .append(tbody)
            )
            .appendTo(parent);
    }
}