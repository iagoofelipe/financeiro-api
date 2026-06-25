import ModalNewCard from "./modal/new-card.js";
import ModalNewResponsable from "./modal/new-responsable.js";
import { MODAL_FLAGS, set_modal } from "../tools/utils.js";
import { get_cards, get_responsables } from "../tools/api.js";
import { add_registry, update_registry } from "../tools/api/registries.js";

export default class RegistryForm extends EventTarget {
    
    static EVENTS = {
        FINISHED: 'financeiro-api:registryform:finished',
    };

    #jquery;
    #modal_new_card;
    #modal_new_responsable;
    
    constructor(jquery) {
        super();

        this.#jquery = jquery;
        this.#modal_new_card = new ModalNewCard(this.#jquery.find('#modal-new-card'));
        this.#modal_new_responsable = new ModalNewResponsable(this.#jquery.find('#modal-new-responsable'));
        
        this.#modal_new_card.addEventListener(ModalNewCard.EVENTS.SAVED, async () => await this.#on_newCard_saved());
        this.#modal_new_responsable.addEventListener(ModalNewResponsable.EVENTS.SAVED, async () => await this.#on_newResponsable_saved());

        this.#jquery.on('click', '.btn-reg-form-save', async (e) => await this.#on_btnSave_clicked(e));
        this.#jquery.on('click', '.btn-reg-form-cancel', () => this.dispatchEvent(new CustomEvent(RegistryForm.EVENTS.FINISHED)));
    }

    static async create(jquery_container, params) {
        let jquery = $(await $.get('/home/reg-form', params));
        jquery_container.html(jquery);
        return new RegistryForm(jquery);
    }

    async #on_btnSave_clicked(evt) {
        const
            self_reg = this.#jquery.find('#inp-self-reg').prop('checked'),
            type = this.#jquery.find('#inp-type').val(),
            has_card = this.#jquery.find('#inp-has-card').prop('checked'),
            value = this.#jquery.find('#inp-value').val(),
            installment_current = this.#jquery.find('#inp-current-installment').val(),
            installment_total = this.#jquery.find('#inp-num-installments').val(),
            inp_id = this.#jquery.find('#inp-id'),
            is_new_reg = !inp_id.length,
            ref_year = this.#jquery.find('#inp-ref-year').val();
            
        let data = {
            title: this.#jquery.find('#inp-title').val(),
            value: value? parseFloat(value) : 0,
            occurrance: this.#jquery.find('#inp-occurrance').val(),
            description: this.#jquery.find('#inp-desc').val(),
            date_ref: `${ref_year}-${this.#jquery.find('#inp-ref-month').val()}`,
            type_in: this.#jquery.find('#inp-radio-type-in').prop('checked'),
            status: this.#jquery.find('#inp-status').val(),
        };
        
        if (is_new_reg) {
            data.responsable_id = !self_reg? this.#jquery.find('#inp-responsable').val() : null;
            data.card_id = has_card? this.#jquery.find('#inp-card').val() : null;
            data.installment_current = installment_current? parseInt(installment_current) : 1;
            data.installment_total = installment_total? parseInt(installment_total) : 1;
        } else {
            data.id = inp_id.val();
        }

        // verificando campos obrigatórios
        let required_fields = {
            title: '#inp-title',
            occurrance: '#inp-occurrance',
        };
        
        // validando entradas
        this.#jquery.find('[class^="form"].required').removeClass('required');

        if (is_new_reg && data.installment_current > data.installment_total) {
            this.#jquery.find('#inp-current-installment, #inp-num-installments').addClass('required');

            set_modal('Validação de Entradas', 'o valor da parcela atual não pode ser maior que o total de parcelas!', true, MODAL_FLAGS.HIDE_FOOTER);
            return;
        }

        if (isNaN(ref_year) || ref_year < 2000) {
            this.#jquery.find('#inp-ref-year').addClass('required');

            set_modal('Validação de Entradas', 'o ano de referência deve ser maior ou igual a 2000', true, MODAL_FLAGS.HIDE_FOOTER);
            return;
        }
        
        let fields_missing = [];
        for (const field in required_fields) {
            if (!data[field])
                fields_missing.push(required_fields[field]);
        }

        if (fields_missing.length) {
            this.#jquery.find(fields_missing.join(', ')).addClass('required');
            set_modal('Validação de Entradas', 'preencha todos os campos obrigatórios!', true, MODAL_FLAGS.HIDE_FOOTER);
            return;
        }

        const response = await (is_new_reg? add_registry : update_registry)(data);
        if (response.success)
            this.dispatchEvent(new CustomEvent(RegistryForm.EVENTS.FINISHED));
        else
            set_modal('Erro', response.error);
    }

    async #on_newCard_saved() {
        let result = await get_cards();
        if (result.success) {
            const inp_cards = this.#jquery.find('#inp-card').html('');

            result.data.forEach((card) => {
                $(`<option value="${card.id}">${card.name}</option>`).appendTo(inp_cards);
            });
        } else {
            set_modal('Erro', result.error);
        }
    }

    async #on_newResponsable_saved() {
        let result = await get_responsables();
        if (result.success) {
            const inp_responsables = this.#jquery.find('#inp-responsable').html('');

            result.data.forEach((e) => {
                $(`<option value="${e.id}">${e.name}</option>`).appendTo(inp_responsables);
            });
        } else {
            set_modal('Erro', result.error);
        }
    }
}