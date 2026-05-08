export default class CreditCardView {
    static templates = {};
    static templates_set = false;

    async setContent(parent) {
        if (!CreditCardView.templates_set)
            await CreditCardView.loadTemplates();

        $(parent).html(CreditCardView.templates.BODY);
    }

    static async loadTemplates() {
        // coleta os templates necessários para o componente
        if (this.templates_set)
            return;
        
        this.templates_set = true;
        CreditCardView.templates.BODY = await $.get('/templates', {template: 'home/cards.html'});
    }
}