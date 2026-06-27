import { add_responsable } from "../../tools/api.js";
import { set_modal } from "../../tools/utils.js";

export default class ModalNewResponsable extends EventTarget {

    static EVENTS = {
        SAVED: 'financeiro-api:modalnewresponsable:saved',
    };

    #jquery;

    constructor(jquery) {
        super();

        this.#jquery = jquery;
        
        // eventos
        this.#jquery.find('.btn-modal-new-responsable-save').on('click', async (e) => await this.#on_btnSave_clicked(e));
    }

    async #on_btnSave_clicked(evt) {
        const 
            jname = this.#jquery.find('#inp-new-responsable-name'),
            name = jname.val();

        // validando dados
        $('[class^="form"].required').removeClass('required');

        if (!name) {
            jname.addClass('required');
            return;
        }

        this.#jquery.modal('hide');

        let result = await add_responsable({name: name});
        if (!result.success) {
            set_modal('Erro', result.error);
            return;
        }
        
        this.dispatchEvent(new CustomEvent(ModalNewResponsable.EVENTS.SAVED));
    }
}
