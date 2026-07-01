import RegistryView from "./nav-regs/view.js";
import DashboardView from "./nav-dash/view.js";
// import CreditCardView from "./cards.js";

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
            $(nav_btns[i]).on('click', async (evt) => await this.#on_navBtn_clicked(evt));
        }

        this.#initialNavBtn = nav_btns[0];
        this.#set_animations();

        $(this.#initialNavBtn).click();
        $('#btn-nav-collapse').click(this.#on_btnNavCollapse_clicked);
    }

    async #on_navBtn_clicked(evt) {
        evt.preventDefault();

        let jbtn = $(evt.currentTarget);
        let title = jbtn.prop('name');
        let jfilter_month_year = $('#filter-month-year');

        // atualizando conteúdo
        let new_widget;

        switch (title) {
        case 'Dashboards':
            new_widget = await DashboardView.create(jfilter_month_year);
            break;

        case 'Registros':
            new_widget = await RegistryView.create(jfilter_month_year);
            break;

        // case 'Cartões e Faturas':
        //     let cardsview = await CreditCardView.create(parent);
        //     break;

        case 'Sair':
            let response = await $.get('/login/logout');
            if (response.success)
                window.location.reload();
            else
                alert('não foi possível realizar o logout');

            return;

        default:
            console.log('nav option unset', title);
            return;
        }
        
        $('#home-title').text(title); // atualizando título
        this.#update_nav_button(jbtn); // atualizando botão selecionado
        
        // atualizando conteúdo
        let jquery = new_widget.jquery();
        $('#home-content').html(jquery);
        $('#home-navtop').html(jquery.find('#home-navtop-content'));
    }

    #set_animations() {
        // TODO: tornar em singleton
        $(document).on('click', '.btn-rotate', (evt) => $(evt.currentTarget).toggleClass('btn-rotated'));
        // $(document).on('click', '.btn-rotate-full', (evt) => $(evt.currentTarget).toggleClass('btn-rotated-full'));
    }

    #update_nav_button(jbtn) {
        if (this.#currentNavBtn) {
            this.#currentNavBtn.removeClass('nav-link-active');
        }

        this.#currentNavBtn = jbtn;
        this.#currentNavBtn.addClass('nav-link-active');
    }

    #on_btnNavCollapse_clicked(evt) {
        $('.home-nav').toggleClass('collapsed');
    }
}