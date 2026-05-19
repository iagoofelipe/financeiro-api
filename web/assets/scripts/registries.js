import Table from "./components/table.js";
import { REG_STATUS_HTML, getElementsByXPath } from "./tools/utils.js";

export default class RegistryView extends EventTarget {
    static templates = {};

    #jquery;
    #tables = [];
    #cache_regs_by_id = {};
    #table_selected = null;

    constructor(jquery) {
        super();

        this.#jquery = jquery;

        let find_tables = jquery.find('table'),
            len = find_tables.length;

        for (let i=0; i<len; i++) {
            let jquery = $(find_tables[i]);
            let table = new Table(jquery, Table.FLAGS.ROW_SELECTABLE);
            this.#tables.push(table);
            table.addEventListener(Table.EVENTS.ROW_CLICKED, async (e) => await this.#on_tableTransaction_rowClicked(e));
        }

        $('#reg-details-btn-hide').on('click', (evt) => this.hideDetails());
    }

    static async create(parent) {
        let jquery = $(parent).html(await $.get('/home/nav-regs'));
        return new RegistryView(jquery);
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

    setRegistryDetails(reg) {
        $('#reg-details-title .text').text(reg.title);
        $("#reg-details-type .text").text(reg.type_in? 'Entrada' : 'Saída');
        $("#reg-details-value .text").text(reg.value_formatted);
        $("#reg-details-owner .text").text(reg.responsable_name);
        $("#reg-details-occurrance .text").text(reg.occurrance_formatted);
        $("#reg-details-description .text").text(reg.description);
        $("#reg-details-status .text").html(REG_STATUS_HTML[reg.status]);
        $("#reg-details-card .text").text(reg.card_name);

        $('#reg-details').show();

        // ocultando e exibindo campos de acordo com o conteúdo com XPath
        $(getElementsByXPath("//div[contains(@id, 'reg-details-')][child::p[contains(@class, 'text') and text()]]")).show();
        $(getElementsByXPath("//div[contains(@id, 'reg-details-')][child::p[contains(@class, 'text') and not(text())]]")).hide();
    }

    hideDetails() {
        $('#reg-details').hide();
        if (this.#table_selected) {
            this.#table_selected.unselect();
            this.#table_selected = null;
        }
    }
}