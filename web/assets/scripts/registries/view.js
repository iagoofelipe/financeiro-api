import Table from "../components/table.js";
import RegistryDetails from "./details.js";
import { delete_registry, has_registries } from "../tools/api/registries.js";
import RegistryForm from "./form.js";
import { set_modal } from "../tools/utils.js";

export default class RegistryView extends EventTarget {
    static templates = {};

    #jquery;
    #reg_details;
    #reg_form;
    #tables = [];
    #cache = {
        regs_by_id: {},
    };
    #table_selected = null;
    ID_CONTENT_TRANSACTIONS = 0;
    ID_CONTENT_REG_FORM = 1;
    #current_date_ref = null;

    constructor(jquery) {
        super();
        this.#jquery = jquery;

        // Template index
        jquery.on('click', '.reg-transactions #btn-trans-expand', () => this.expandAllCards());
        jquery.on('click', '.reg-transactions #btn-trans-collapse', () => this.collapseAllCards());
        jquery.on('click', '.reg-transactions #btn-trans-reload', async () => await this.updateTransactionCards());
        jquery.on('click', '.reg-transactions #btn-new-reg', async () => await this.setContentById(this.ID_CONTENT_REG_FORM, {mode: 'NEW'}));
        jquery.on('change', '#modal-trans-filter .form', async () => await this.updateTransactionCards());
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos - Estáticos
    static async create() {
        let jquery = $('<div class="h-100">'); // div é necessário para armazenar os eventos e a troca do conteúdo interno
        let obj = new RegistryView(jquery);
        
        await obj.setContentById(await has_registries()? obj.ID_CONTENT_TRANSACTIONS : obj.ID_CONTENT_REG_FORM);
        return obj;
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos
    jquery() { return this.#jquery; }

    async setContentById(id, params) {
        let jcontent;

        switch(id)
        {
            case this.ID_CONTENT_REG_FORM:
                this.#reg_form = await RegistryForm.create(this.#jquery, params);
                this.#reg_form.addEventListener(RegistryForm.EVENTS.FINISHED, async () => await this.setContentById(this.ID_CONTENT_TRANSACTIONS));
                break;

            case this.ID_CONTENT_TRANSACTIONS:
                const data = this.#current_date_ref? {date_ref: this.#current_date_ref} : {};
                jcontent = $(await $.get('/home/nav-reg', data));
                this.#jquery.html(jcontent);
                this.#reg_details = new RegistryDetails(jcontent.find('.reg-details'));
                
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.HIDE, () => this.hideDetails());
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.DUPLICATE, async (e) => await this.setContentById(this.ID_CONTENT_REG_FORM, {mode: 'COPY', id: e.detail}));
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.EDIT, async (e) => await this.setContentById(this.ID_CONTENT_REG_FORM, {mode: 'EDIT', id: e.detail}));
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.DELETE, async (e) => await this.#on_regDetails_delete(e));

                await this.updateTransactionCards();
                break;
            
            default:
                throw Error('undefined content id');
        }
    }

    hideDetails() {
        this.#reg_details.hide();
        if (this.#table_selected) {
            this.#table_selected.unselect();
            this.#table_selected = null;
        }
    }

    async updateTransactionCards() {
        this.hideDetails();
        
        // limpando cache
        this.#cache.regs_by_id = {};
        
        let ref_year = this.#jquery.find('#filter-ref-year').val();
        this.#current_date_ref = ref_year + '-' + this.#jquery.find('#filter-ref-month').val() + '-01';
        let data = {
            date_ref: this.#current_date_ref,
            card_id: this.#jquery.find('#filter-card').val(),
        };

        const response = await $.get('/home/nav-reg/trans-cards', data);
        let jquery = this.#jquery.find('#trans-cards').html(response);
        let sum_inputs = this.#jquery.find('#sum-inputs-hidden').val();
        let sum_outputs = this.#jquery.find('#sum-outputs-hidden').val();
        let total_inout = this.#jquery.find('#total-inout-hidden').val();
        let total_is_positive = this.#jquery.find('#positive-inout-hidden').val() == 'True';

        this.#jquery.find('#sum-inputs').text(sum_inputs? sum_inputs : 'R$ 0,00');
        this.#jquery.find('#sum-outputs').text(sum_outputs? sum_outputs : 'R$ 0,00');
        this.#jquery.find('#total-inout').text(total_inout? total_inout : 'R$ 0,00');

        if (total_is_positive) {
            this.#jquery.find('.icon-money-bag-alert').hide();
            this.#jquery.find('.icon-money-bag-success').show();
        } else {
            this.#jquery.find('.icon-money-bag-alert').show();
            this.#jquery.find('.icon-money-bag-success').hide();
        }

        let find_tables = jquery.find('table'),
            len = find_tables.length;

        for (let i=0; i<len; i++) {
            let jquery = $(find_tables[i]);
            let table = new Table(jquery, Table.FLAGS.ROW_SELECTABLE);
            this.#tables.push(table);
            table.addEventListener(Table.EVENTS.ROW_CLICKED, async (e) => await this.#on_tableTransaction_rowClicked(e));
        }

        // atualizando informações dos filtros
        let month_year = `${this.#jquery.find('#filter-ref-month option:selected').text()} ${ref_year}`;
        let card = this.#jquery.find('#filter-card option:selected').text();
        let msg = 'Referência: ' + month_year;

        if (card != '(Todos)') {
            msg += ', Cartão: ' + card;
        }

        this.#jquery.find('#filter-info').text(msg);
    }

    collapseAllCards() {
        $('#trans-cards button[aria-expanded="true"]').click();
    }

    expandAllCards() {
        $('#trans-cards button[aria-expanded="false"]').click();
    }

    //-----------------------------------------------------------------------------
    // Eventos
    async #on_tableTransaction_rowClicked(evt) {
        let id = evt.detail.id;

        if (!(id in this.#cache.regs_by_id)) {
            let response = await $.get({
                url: `/api/getRegistry/${id}`,
                headers: {
                    'Authorization': localStorage.getItem('TOKEN_API'),
                }
            });

            this.#cache.regs_by_id[id] = response;
        }

        if (this.#table_selected && this.#table_selected != evt.target) {
            this.#table_selected.unselect();
        }
        
        this.#table_selected = evt.target;
        this.#reg_details.setValues(this.#cache.regs_by_id[id]);
    }

    async #on_regDetails_delete(evt) {
        const response = await delete_registry(evt.detail);
        if (response.success)
            await this.updateTransactionCards();
        else
            set_modal('Erro de Requisição', response.error);
    };
    //-----------------------------------------------------------------------------
}