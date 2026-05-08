export default class DashboardView {
    static templates = {};
    static templates_set = false;

    static async create(parent) {
        await this.loadTemplates();
        let jquery = $(parent).html(this.#template_body());
        
        return new DashboardView(jquery);
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        if (this.templates_set)
            return;
        
        this.templates_set = true;
        this.templates.BODY = await $.get('/templates', {template: 'home/dash.html'});
    }

    static #template_body() {
        return this.templates.BODY;
    }
}