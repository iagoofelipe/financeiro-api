import CategoryChart from "../components/category-chart.js";
import { get_invoice_by_card } from "../tools/api/cards.js";
import { values_by_category } from "../tools/api/statistics.js";

export default class DashboardView {
    #jquery;
    #category_chart;
    #date_ref;

    constructor(jquery, category_chart) {
        this.#jquery = jquery;
        this.#category_chart = category_chart;

        let filter_month_year = jquery.find('#filter-month-year');
        this.#date_ref = filter_month_year.val() + '-01';
        
        // jquery.on não deve ser utilizado pelo conteúdo ser movido
        filter_month_year.on('change', async (e) => await this.#on_filterMonthYear_changed(e));
        this.#jquery.on('change', '.select-card', async (e) => await this.updateCard());
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos - Estáticos
    static async create() {
        let jquery = $(await $.get('/home/nav-dash'));
        let parent = jquery.find('#chart-category');
        const response = await values_by_category({
            data_ref: jquery.find('#filter-month-year').val() + '-01',
        });

        let category_chart = new CategoryChart({
            data: response.data,
            filterOptions: [
                {value: 'in', text: 'Entradas'},
                {value:'out', text: 'Saídas'},
            ],
            fieldLabel: 'title',
            fieldData: 'total',
            appendTo: parent,
            dataAsObject: true,
        });

        let obj = new DashboardView(jquery, category_chart);
        await obj.updateCard();

        return obj;
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos
    jquery() { return this.#jquery; }

    async updateCard() {
        let response = await get_invoice_by_card({
            field: 'id',
            q: this.#jquery.find('.select-card option:selected').val(),
            date_ref: this.#date_ref,
        });

        if (response.success) {
            this.#jquery.find('.field-card-accounted .text').text(response.data.sum_registred_formatted);
            this.#jquery.find('.field-card-pending .text').text(response.data.sum_pending_formatted);
            this.#jquery.find('.field-card-closing-date .text').text(response.data.closing_date_formatted);
            this.#jquery.find('.field-card-due-date .text').text(response.data.due_date_formatted);
        } else {
            this.#jquery.find('.field-card-accounted .text').text('-');
            this.#jquery.find('.field-card-pending .text').text('-');
            this.#jquery.find('.field-card-closing-date .text').text('-');
            this.#jquery.find('.field-card-due-date .text').text('-');
        }
    }

    //-----------------------------------------------------------------------------
    // Eventos
    async #on_filterMonthYear_changed(evt) {
        this.#date_ref = evt.currentTarget.value + '-01';

        let response = await values_by_category({
            date_ref: this.#date_ref,
        });
        if (response.success)
            this.#category_chart.setValues(response.data);

       await this.updateCard();
    }

    //-----------------------------------------------------------------------------
    // Métodos Privados

    //-----------------------------------------------------------------------------
}