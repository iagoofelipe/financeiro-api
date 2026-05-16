export default class RegistryView extends EventTarget {
    static templates = {};
    static templates_set = false;

    #jquery;

    constructor(jquery) {
        super();

        this.#jquery = jquery;
    }

    static async create(parent) {
        await this.loadTemplates();
        let jquery = $(parent).html(this.#template_body());

        return new RegistryView(jquery);
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        // if (this.templates_set)
        //     return;
        
        // this.templates_set = true;
        this.templates.BODY = await $.get('/v2/home/regs');
    }

    static #template_body() {
        return this.templates.BODY;
    }
}