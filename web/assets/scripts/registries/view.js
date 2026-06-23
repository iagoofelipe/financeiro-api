import Table from "../components/table.js";
import RegistryDetails from "./details.js";
import { has_registries } from "../tools/api.js";
import RegistryForm from "./form.js";

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
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos - Estáticos
    static async create() {
        let jquery = $('<div class="h-100">'); // div é necessário para trocar o conteúdo interno
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
                jcontent = $(await $.get('/home/nav-regs', data));
                this.#jquery.html(jcontent);
                this.#reg_details = new RegistryDetails(jcontent.find('.reg-details'));
                
                // Template index
                jcontent.on('click', '#btn-trans-expand', () => this.expandAllCards());
                jcontent.on('click', '#btn-trans-collapse', () => this.collapseAllCards());
                jcontent.on('click', '#btn-trans-reload', async () => await this.updateTransactionCards());
                jcontent.on('click', '#btn-new-reg', async () => await this.setContentById(this.ID_CONTENT_REG_FORM, {mode: 'NEW'}));
                jcontent.on('change', '#filter-ref-year, #filter-ref-month', async () => await this.updateTransactionCards());
                
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.HIDE, () => this.hideDetails());
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.DUPLICATE, async (e) => this.setContentById(this.ID_CONTENT_REG_FORM, {mode: 'COPY', id: e.detail}));
                this.#reg_details.addEventListener(RegistryDetails.EVENTS.EDIT, async (e) => this.setContentById(this.ID_CONTENT_REG_FORM, {mode: 'EDIT', id: e.detail}));
                
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
        
        this.#current_date_ref = this.#jquery.find('#filter-ref-year').val() + '-' + this.#jquery.find('#filter-ref-month').val() + '-01';
        const response = await $.get('/home/regs-trans-cards', {date_ref: this.#current_date_ref});
        let jquery = this.#jquery.find('#trans-cards').html(response);
        let sum_inputs = this.#jquery.find('#sum-inputs-hidden').text();
        let sum_outputs = this.#jquery.find('#sum-outputs-hidden').text();

        this.#jquery.find('#sum-inputs').text(sum_inputs? sum_inputs : 'R$ 0,00');
        this.#jquery.find('#sum-outputs').text(sum_outputs? sum_outputs : 'R$ 0,00');

        let find_tables = jquery.find('table'),
            len = find_tables.length;

        for (let i=0; i<len; i++) {
            let jquery = $(find_tables[i]);
            let table = new Table(jquery, Table.FLAGS.ROW_SELECTABLE);
            this.#tables.push(table);
            table.addEventListener(Table.EVENTS.ROW_CLICKED, async (e) => await this.#on_tableTransaction_rowClicked(e));
        }
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

    //-----------------------------------------------------------------------------
}