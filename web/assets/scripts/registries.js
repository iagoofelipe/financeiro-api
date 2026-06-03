import Table from "./components/table.js";
import { REG_STATUS_HTML, getElementsByXPath } from "./tools/utils.js";

export default class RegistryView extends EventTarget {
    static templates = {};

    #jquery;
    #current_date_ref;
    #tables = [];
    #cache_regs_by_id = {};
    #table_selected = null;

    constructor(jquery) {
        super();
        this.#jquery = jquery;
        this.#current_date_ref = $('#dropdown-date-ref .dropdown-item.active').attr('value');

        // jquery.on('click', '#trans-cards button[data-bs-toggle="collapse"]', this.#on_btnCollapsable_clicked);
        $('#reg-details-btn-hide').on('click', (evt) => this.hideDetails());
        $('#dropdown-date-ref .dropdown-item').on('click', async (e) => await this.#on_dropdownDateRefItem_clicked(e));
        $('#btn-trans-reload').on('click', async (e) => await this.updateTransactionCards());
        $('#btn-trans-expand').click(this.expandAllCards);
        $('#btn-trans-collapse').click(this.collapseAllCards);

        this.updateTransactionCards();
        // this.collapseAllCards();
    }

    static async create(parent) {
        let jquery = $(parent).html(await $.get('/home/nav-regs'));
        return new RegistryView(jquery);
    }

    hideDetails() {
        $('#reg-details').hide();
        if (this.#table_selected) {
            this.#table_selected.unselect();
            this.#table_selected = null;
        }
    }

    setRegistryDetails(reg) {
        $('#reg-details-title .text').text(reg.title);
        $("#reg-details-type .text").text(reg.type_in? 'Entrada' : 'Saída');
        $("#reg-details-value .text").text(reg.value_formatted ?? '');
        $("#reg-details-owner .text").text(reg.responsable_name ?? '');
        $("#reg-details-occurrance .text").text(reg.occurrance_formatted ?? '');
        $("#reg-details-description .text").text(reg.description ?? '');
        $("#reg-details-status .text").html(REG_STATUS_HTML[reg.status]);
        $("#reg-details-invoice .text").text(reg.invoice_ref_formatted ?? '');
        $("#reg-details-installment .text").text(reg.installment_index? `${reg.installment_index+1} de ${reg.installment_num_items}` : '');
        $("#reg-details-installment-value .text").text(reg.installment_value_formatted ?? '');
        $("#reg-details-paid .text").text(reg.installment_paid_formatted ?? '');
        $("#reg-details-pending .text").text(reg.installment_pending_formatted ?? '');

        $('#reg-details').show();

        // ocultando e exibindo campos de acordo com o conteúdo com XPath
        $(getElementsByXPath("//div[contains(@id, 'reg-details-')][child::p[contains(@class, 'text') and text()]]")).show();
        $(getElementsByXPath("//div[contains(@id, 'reg-details-')][child::p[contains(@class, 'text') and not(text())]]")).hide();
    }

    async updateTransactionCards() {
        this.hideDetails();
        // let controllers = $('#btn-date-ref, #btn-trans-reload');
        // controllers.prop('disabled', true);
        
        // limpando cache
        this.#cache_regs_by_id = {};

        const response = await $.get('/home/regs-trans-cards', {date_ref: this.#current_date_ref});
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

        // controllers.prop('disabled', false);
    }

    collapseAllCards() {
        // $('#btn-trans-collapse').hide();
        // $('#btn-trans-expand').show();
        $('#trans-cards button[aria-expanded="true"]').click();
    }

    expandAllCards() {
        // $('#btn-trans-expand').hide();
        // $('#btn-trans-collapse').show();
        $('#trans-cards button[aria-expanded="false"]').click();
    }

    async #on_tableTransaction_rowClicked(evt) {
        let id = evt.detail.id;

        if (!(id in this.#cache_regs_by_id)) {
            let response = await $.get({
                url: `/api/getRegistry/${id}`,
                headers: {
                    'Authorization': localStorage.getItem('TOKEN_API'),
                }
            });

            this.#cache_regs_by_id[id] = response;
        }

        if (this.#table_selected && this.#table_selected != evt.target) {
            this.#table_selected.unselect();
        }
        
        this.#table_selected = evt.target;
        this.setRegistryDetails(this.#cache_regs_by_id[id]);
    }

    async #on_dropdownDateRefItem_clicked(evt) {
        let selected = $(evt.currentTarget);
        if (selected.hasClass('active'))
            return;
        
        this.#current_date_ref = selected.attr('value');
        $('#dropdown-date-ref .dropdown-item.active').removeClass('active');
        selected.addClass('active');
        $('#btn-date-ref').text(selected.text());
        await this.updateTransactionCards();
    }

    // #on_btnCollapsable_clicked(evt) {
    //     if ($('#trans-cards button[aria-expanded="true"]').length) {
    //         $('#btn-trans-expand').hide();
    //         $('#btn-trans-collapse').show();
    //     } else {
    //         $('#btn-trans-collapse').hide();
    //         $('#btn-trans-expand').show();
    //     }
    // }
}