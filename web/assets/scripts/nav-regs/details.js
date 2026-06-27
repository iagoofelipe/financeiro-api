import { getElementsByXPath, REG_STATUS_HTML } from "../tools/utils.js";

export default class RegistryDetails extends EventTarget {
    #jquery;
    #id = null;

    static EVENTS = {
        DUPLICATE: 'financeiro-api:registrydetails:duplicate',
        DELETE: 'financeiro-api:registrydetails:delete',
        EDIT: 'financeiro-api:registrydetails:edit',
        HIDE: 'financeiro-api:registrydetails:hide',
    };

    constructor(jquery) {
        super();
        this.#jquery = jquery;

        jquery.on('click', '.btn-duplicate', () => this.dispatchEvent(new CustomEvent(RegistryDetails.EVENTS.DUPLICATE, {detail: this.#id})));
        jquery.on('click', '.btn-delete', () => this.#jquery.find('#modal-trans-delete').modal('show'));
        jquery.on('click', '.btn-edit', () => this.dispatchEvent(new CustomEvent(RegistryDetails.EVENTS.EDIT, {detail: this.#id})));
        jquery.on('click', '.btn-hide', () => this.dispatchEvent(new CustomEvent(RegistryDetails.EVENTS.HIDE)));
        jquery.on('click', '#modal-trans-delete .btn-modal-ok', () => this.#on_modalDelete_btnOK_clicked());
    }

    setValues(data) {
        this.#id = data.id;
        this.#jquery.find('.inp-title .text').text(data.title);
        this.#jquery.find(".inp-type .text").text(data.type_in? 'Entrada' : 'Saída');
        this.#jquery.find(".inp-value .text").text(data.value_formatted ?? '');
        this.#jquery.find(".inp-owner .text").text(data.responsable_name ?? '');
        this.#jquery.find(".inp-occurrance .text").text(data.occurrance_formatted ?? '');
        this.#jquery.find(".inp-description .text").text(data.description ?? '');
        this.#jquery.find(".inp-category .text").text(data.category ?? '');
        this.#jquery.find(".inp-status .text").html(REG_STATUS_HTML[data.status]);
        this.#jquery.find(".inp-card .text").text(data.card_name ?? '');
        this.#jquery.find(".inp-invoice .text").text(data.invoice_ref_formatted ?? '');
        this.#jquery.find(".inp-installment .text").text(data.installment_formatted ?? '');
        this.#jquery.find(".inp-installment-value .text").text(data.installment_value_formatted ?? '');

        let details_paid_pending = this.#jquery.find(".inp-paid-pending");
        details_paid_pending.find(".text.paid").text(data.installment_paid_formatted ?? '');
        details_paid_pending.find(".text.pending").text(data.installment_pending_formatted ?? '');
        
        if (data.installment_formatted) {
            let percent = 100 / data.installment_value;
            details_paid_pending.find('.bar.paid').css('width', `${data.installment_paid * percent}%`);
            details_paid_pending.find('.bar.pending').css('width', `${data.installment_pending * percent}%`);
            
            details_paid_pending.show();
        }
        else details_paid_pending.hide();
        
        // ocultando e exibindo campos de acordo com o conteúdo com XPath
        $(getElementsByXPath("//div[contains(@class, 'inp-')][child::p[contains(@class, 'text') and text()]]", this.#jquery[0])).show();
        $(getElementsByXPath("//div[contains(@class, 'inp-')][child::p[contains(@class, 'text') and not(text())]]", this.#jquery[0])).hide();
        
        this.show();
    }

    show() { this.#jquery.show(); }
    hide() { this.#jquery.hide(); }
    
    //-----------------------------------------------------------------------------
    // Eventos
    #on_modalDelete_btnOK_clicked() {
        this.#jquery.find('#modal-trans-delete').modal('hide');
        this.dispatchEvent(new CustomEvent(RegistryDetails.EVENTS.DELETE, {detail: this.#id}));
    }
    //-----------------------------------------------------------------------------
}