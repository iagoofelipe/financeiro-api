import { add_card } from "../../tools/api.js";
import { set_modal } from "../../tools/utils.js";

export default class ModalNewCard extends EventTarget {

    static EVENTS = {
        SAVED: 'financeiro-api:modalnewcard:saved',
    };

    #jquery;

    constructor(jquery) {
        super();
        
        this.#jquery = jquery;

        // eventos
        this.#jquery.find('.btn-modal-new-card-save').on('click', async (e) => await this.#on_btnSave_clicked(e));
    }

    async #on_btnSave_clicked(evt) {
        const 
            jname = this.#jquery.find('.inp-name'),
            data = {
                name: jname.val(),
                closing_day: parseInt(this.#jquery.find('.inp-closing').val()),
                closing_previous_month: this.#jquery.find('.inp-prev-month-closing').prop('checked'),
                due_day: parseInt(this.#jquery.find('.inp-due').val()),
                due_previous_month: this.#jquery.find('.inp-prev-month-due').prop('checked'),
                limit: parseFloat(this.#jquery.find('.inp-limit').val()),
            };

        // validando dados
        this.#jquery.find('[class^="form"].required').removeClass('required');

        if (!data.name) {
            jname.addClass('required');
            return;
        }

        this.#jquery.modal('hide');

        let result = await add_card(data);
        if (!result.success) {
            set_modal('Erro', result.error);
            return;
        }

        this.dispatchEvent(new CustomEvent(ModalNewCard.EVENTS.SAVED));
    }
}