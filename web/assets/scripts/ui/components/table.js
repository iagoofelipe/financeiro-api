export default class Table {
    #jquery_element;

    constructor(params) {
        let thead = $('<thead>');
        let tbody = $('<tbody>');
        
        if (params.columns) {
            let row = $('<tr>');
            const num_cols = params.columns.length;

            // headers
            for (let i=0; i < num_cols; i++) {
                $(`<th scope="col">${params.columns[i]}</th>`).appendTo(row);
            }

            row.appendTo(thead);

            // content
            if (params.data) {
                for (let index_row=0; index_row < params.data.length; index_row++) {
                    let row = $('<tr>');
                    let data = params.data[index_row];
                    
                    for (let index_col=0; index_col < data.length && index_col < num_cols; index_col++) {
                        $(`<td>${data[index_col]}</td>`).appendTo(row);
                    }

                    row.appendTo(tbody);
                }
            }
        }


        this.#jquery_element = $('<div class="table-responsive">')
            .append(
                $('<table class="table m-0">')
                    .append(thead)
                    .append(tbody)
            );
        
        if (params.parent)
            this.#jquery_element.appendTo(params.parent);
    }

    jquery() { return this.#jquery_element; }
}