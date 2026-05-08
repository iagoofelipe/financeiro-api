export default class DashboardView {
    static templates = {};
    static templates_set = false;

    async setContent(parent) {
        if (!DashboardView.templates_set)
            await DashboardView.loadTemplates();

        $(parent).html(DashboardView.templates.BODY);
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        if (this.templates_set)
            return;
        
        this.templates_set = true;
        this.templates.BODY = await $.get('/templates', {template: 'home/dash.html'});
    }
}