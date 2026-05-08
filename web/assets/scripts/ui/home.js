import RegistryView from "./registries.js";
import DashboardView from "./dashboards.js";
import CreditCardView from "./cards.js";

$(async () => {
    let home_view = new HomeView();
});

class HomeView
{
    #currentNavBtn;
    #initialNavBtn;

    constructor() {
        // configurando nav-btns
        let nav_btns = $('.home-nav .nav-link');

        for(let i=0; i<nav_btns.length; i++) {
            $(nav_btns[i]).on('click', async (evt) => await this.#navBtn_clicked(evt));
        }

        this.#initialNavBtn = nav_btns[1];
        this.#set_animations();

        $(this.#initialNavBtn).click();
    }

    async #navBtn_clicked(evt) {
        evt.preventDefault();

        let jbtn = $(evt.currentTarget);
        let title = jbtn.prop('name');

        // atualizando conteúdo
        const parent = '#home-content';
        switch (title) {
        case 'Dashboards':
            let dashview = await DashboardView.create(parent);
            break;

        case 'Registros':
            let regview = await RegistryView.create(parent);
            break;

        case 'Cartões e Faturas':
            let cardsview = await CreditCardView.create(parent);
            break;

        default:
            console.log('nav option unset', title);
            return;
        }
        
        $('#home-title').text(title); // atualizando título
        this.#update_nav_button(jbtn); // atualizando botão selecionado
    }

    #set_animations() {
        // TODO: tornar em singleton
        $(document).on('click', '.btn-rotate', (evt) => $(evt.currentTarget).toggleClass('btn-rotated'));
        $(document).on('click', '.btn-rotate-full', (evt) => $(evt.currentTarget).toggleClass('btn-rotated-full'));
    }

    #update_nav_button(jbtn) {
        if (this.#currentNavBtn) {
            this.#currentNavBtn.removeClass('nav-link-active');
        }

        this.#currentNavBtn = jbtn;
        this.#currentNavBtn.addClass('nav-link-active');
    }
}