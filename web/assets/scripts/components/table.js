export default class Table extends EventTarget {
    #id = '';
    #flags;
    #currentSelection = {
        id: null,
        jquery: null,
        element: null,
    };

    static EVENTS = {
        ROW_CLICKED: 'financeiro-api:component-table:row-click',
    };
    static FLAGS = {
        ROW_SELECTABLE: 1 << 1,
    };

    constructor(jquery, flags) {
        super();
        this.#flags = flags ?? 0;

        jquery.on('click', 'tbody tr', (evt) => this.#emit_row_clicked(evt));
    }

    selection() { return this.#currentSelection; }

    unselect() {
        if (!this.#currentSelection.jquery)
            return;

        if (this.#flags & Table.FLAGS.ROW_SELECTABLE)
            this.#currentSelection.jquery.removeClass('table-active');
        
        this.#currentSelection.id = null;
        this.#currentSelection.jquery = null;
    }

    #emit_row_clicked(evt) {
        if (evt.currentTarget.classList.contains('ignore-click'))
            return;

        let jquery = $(evt.currentTarget);
        
        if (this.#flags & Table.FLAGS.ROW_SELECTABLE) {
            if (evt.currentTarget == this.#currentSelection.element) // ignora caso a linha clicada já esteja selecionada
                return;

            if (this.#currentSelection.jquery)
                    this.#currentSelection.jquery.removeClass('table-active');
            
            jquery.addClass('table-active');
        }
            
        this.#currentSelection = {
            id: parseInt(evt.currentTarget.cells[0].innerText),
            jquery: jquery,
            element: evt.currentTarget,
        };

        this.dispatchEvent(new CustomEvent(Table.EVENTS.ROW_CLICKED, {detail: this.#currentSelection}));
    }
}