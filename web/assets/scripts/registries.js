import Table from "./components/table.js";
import { has_registries } from "./tools/api.js";
import { MODAL_FLAGS, REG_STATUS_HTML, getElementsByXPath, set_modal } from "./tools/utils.js";

export default class RegistryView extends EventTarget {
    static templates = {};

    #jquery;
    #tables = [];
    #cache = {
        regs_by_id: {},
        invoices_by_card_id: {},
    };
    #table_selected = null;
    ID_CONTENT_TRANSACTIONS = 0;
    ID_CONTENT_NEW_REG = 1;

    constructor(jquery) {
        super();
        this.#jquery = jquery;
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos - Estáticos
    static async create() {
        let jquery = $('<div class="h-100">'); // div é necessário para trocar o conteúdo interno
        let obj = new RegistryView(jquery);
        
        await obj.setContentById(await has_registries()? obj.ID_CONTENT_TRANSACTIONS : obj.ID_CONTENT_NEW_REG);
        return obj;
    }


    //-----------------------------------------------------------------------------
    // Métodos Públicos
    jquery() { return this.#jquery; }

    async setContentById(id) {
        let jcontent;
        
        switch(id)
        {
            case this.ID_CONTENT_NEW_REG:
                jcontent = $(await $.get('/home/new-reg'));
                
                // Template new-reg
                jcontent.on('change', '#inp-card', async () => await this.updateNewRegInvoices());
                // jcontent.on('change', '#inp-type', async (e) => await this.#on_regType_changed(e));
                jcontent.on('click', '#btn-save-new-reg', async (e) => await this.#on_btnSaveNewReg_clicked(e));
                jcontent.on('click', '#btn-cancel-new-reg', async (e) => await this.#on_btnCancelNewReg_clicked(e));
                break;
            
            case this.ID_CONTENT_TRANSACTIONS:
                jcontent = $(await $.get('/home/nav-regs'));
                
                // Template home-regs
                jcontent.on('click', '#btn-trans-expand', this.expandAllCards);
                jcontent.on('click', '#reg-details-btn-hide', this.hideDetails);
                jcontent.on('click', '#btn-trans-collapse', this.collapseAllCards);
                jcontent.on('click', '#btn-trans-reload', async () => await this.updateTransactionCards());
                jcontent.on('click', '#btn-new-reg', async (e) => await this.#on_btnNewReg_clicked(e));
                jcontent.on('click', '#dropdown-date-ref .dropdown-item', async (e) => await this.#on_dropdownDateRefItem_clicked(e));

                this.updateTransactionCards();
                break;
            
            default:
                throw Error('undefined content id');
        }

        // this.#jquery.html('');
        // jcontent.appendTo(this.#jquery);
        this.#jquery.html(jcontent);
    }

    setRegistryDetails(reg) {
        $('#reg-details-title .text').text(reg.title);
        $("#reg-details-type .text").text(reg.type_in? 'Entrada' : 'Saída');
        $("#reg-details-value .text").text(reg.value_formatted ?? '');
        $("#reg-details-owner .text").text(reg.responsable_name ?? '');
        $("#reg-details-occurrance .text").text(reg.occurrance_formatted ?? '');
        $("#reg-details-description .text").text(reg.description ?? '');
        $("#reg-details-status .text").html(REG_STATUS_HTML[reg.status]);
        $("#reg-details-card .text").text(reg.card_name ?? '');
        $("#reg-details-invoice .text").text(reg.invoice_ref_formatted ?? '');
        $("#reg-details-installment .text").text(reg.installment_formatted ?? '');
        $("#reg-details-installment-value .text").text(reg.installment_value_formatted ?? '');

        let details_paid_pending = $("#reg-details-paid-pending");
        details_paid_pending.find(".text.paid").text(reg.installment_paid_formatted ?? '');
        details_paid_pending.find(".text.pending").text(reg.installment_pending_formatted ?? '');
        
        if (reg.installment_formatted) {
            let percent = 100 / reg.installment_value;
            details_paid_pending.find('.bar.paid').css('width', `${reg.installment_paid * percent}%`);
            details_paid_pending.find('.bar.pending').css('width', `${reg.installment_pending * percent}%`);
            
            details_paid_pending.show();
        }
        else details_paid_pending.hide();
        
        // ocultando e exibindo campos de acordo com o conteúdo com XPath
        $(getElementsByXPath("//div[contains(@id, 'reg-details-')][child::p[contains(@class, 'text') and text()]]")).show();
        $(getElementsByXPath("//div[contains(@id, 'reg-details-')][child::p[contains(@class, 'text') and not(text())]]")).hide();
        
        $('#reg-details').show();
    }

    hideDetails() {
        $('#reg-details').hide();
        if (this.#table_selected) {
            this.#table_selected.unselect();
            this.#table_selected = null;
        }
    }

    async updateTransactionCards() {
        this.hideDetails();
        
        // limpando cache
        this.#cache.regs_by_id = {};
        this.#cache.invoices_by_card_id = {};

        const current_date_ref = $('#dropdown-date-ref .dropdown-item.active').attr('value');
        const response = await $.get('/home/regs-trans-cards', {date_ref: current_date_ref});
        let jquery = $('#trans-cards').html(response);
        $('#sum-inputs').text($('#sum-inputs-hidden').text());
        $('#sum-outputs').text($('#sum-outputs-hidden').text());

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

    async updateNewRegInvoices() {
        const id_option = $('#inp-card').val();
        if (!(id_option in this.#cache.invoices_by_card_id)) {
            this.#cache.invoices_by_card_id[id_option] = await $.get({
                url: `/api/getInvoices`,
                data: {
                    card_id: id_option,
                },
                headers: {
                    'Authorization': localStorage.getItem('TOKEN_API'),
                }
            });
        }

        let inp_invoice = $('#inp-invoice').html('');

        this.#cache.invoices_by_card_id[id_option].forEach(element => {
            $(`<option value="${element.id}">${element.date_ref_formatted}</option>`).appendTo(inp_invoice);
        });
    }

    //-----------------------------------------------------------------------------
    // Eventos template home-regs
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
        this.setRegistryDetails(this.#cache.regs_by_id[id]);
    }

    async #on_dropdownDateRefItem_clicked(evt) {
        let selected = $(evt.currentTarget);
        if (selected.hasClass('active'))
            return;
        
        // this.#current_date_ref = selected.attr('value');
        $('#dropdown-date-ref .dropdown-item.active').removeClass('active');
        selected.addClass('active');
        $('#btn-date-ref').text(selected.text());

        await this.updateTransactionCards();
    }

    async #on_btnNewReg_clicked(evt) {
        await this.setContentById(this.ID_CONTENT_NEW_REG);
    }

    //-----------------------------------------------------------------------------
    // Eventos template new-reg
    async #on_btnSaveNewReg_clicked(evt) {
        const
            self_reg = this.#jquery.find('#inp-self-reg').prop('checked'),
            type = this.#jquery.find('#inp-type').val(),
            has_card = this.#jquery.find('#inp-has-card').prop('checked'),
            value = this.#jquery.find('#inp-value').val(),
            installment_current = this.#jquery.find('#inp-current-installment').val(),
            installment_total = this.#jquery.find('#inp-num-installments').val();
            
        let data = {
            title: this.#jquery.find('#inp-title').val(),
            value: value? parseFloat(value) : 0,
            status: this.#jquery.find('#inp-status').val(),
            occurrance: this.#jquery.find('#inp-occurrance').val(),
            description: this.#jquery.find('#inp-desc').val(),
            ref_year: parseInt(this.#jquery.find('#inp-ref-year').val()),
            ref_month: parseInt(this.#jquery.find('#inp-ref-month').val()),
            type_in: this.#jquery.find('#inp-radio-status-in').prop('checked'),
            responsable_id: !self_reg? this.#jquery.find('#inp-responsable').val() : null,
            card_id: has_card? this.#jquery.find('#inp-card').val() : null,
            installment_current: installment_current? parseInt(installment_current) : 1,
            installment_total: installment_total? parseInt(installment_total) : 1,
        };

        // verificando campos obrigatórios
        let required_fields = {
            title: '#inp-title',
            occurrance: '#inp-occurrance',
        };
        
        // validando entradas
        $('[class^="form"].required').removeClass('required');

        if (data.installment_current > data.installment_total) {
            this.#jquery.find('#inp-current-installment, #inp-num-installments').addClass('required');

            set_modal('Validação de Entradas', 'o valor da parcela atual não pode ser maior que o total de parcelas!', true, MODAL_FLAGS.HIDE_FOOTER);
            return;
        }

        if (isNaN(data.ref_year) || data.ref_year < 2000) {
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
            $(fields_missing.join(', ')).addClass('required');
            set_modal('Validação de Entradas', 'preencha todos os campos obrigatórios!', true, MODAL_FLAGS.HIDE_FOOTER);
            return;
        }

        console.log(data);
    }

    async #on_btnCancelNewReg_clicked(evt) {
        await this.setContentById(this.ID_CONTENT_TRANSACTIONS);
    }

    //-----------------------------------------------------------------------------
}