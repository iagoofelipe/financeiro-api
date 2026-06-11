import RegistryView from "./registries.js";
// import DashboardView from "./dashboards.js";
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
            $(nav_btns[i]).on('click', async (evt) => await this.#navBtn_clicked(evt));
        }

        this.#initialNavBtn = nav_btns[1];
        this.#set_animations();

        $(this.#initialNavBtn).click();
        $('#btn-nav-collapse').click(this.#on_btnNavCollapse_clicked);
    }

    async #navBtn_clicked(evt) {
        evt.preventDefault();

        let jbtn = $(evt.currentTarget);
        let title = jbtn.prop('name');

        // atualizando conteúdo
        const parent = '#home-content';
        switch (title) {
        // case 'Dashboards':
        //     let dashview = await DashboardView.create(parent);
        //     break;

        case 'Registros':
            let regview = await RegistryView.create(parent);
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
        // let elements = $('.home-nav .nav-logo, .home-nav span');
        // const jquery = $(evt.currentTarget);

        $('.home-nav').toggleClass('collapsed');

        // console.log(jquery.ariaExpanded);

        // if (jquery.attr('aria-expanded') == 'true') {
        //     $('#btn-nav-collapse').attr('aria-expanded', 'false');
        //     $('#')
        //     // elements.hide();
        // } else {
        //     $('#btn-nav-collapse').attr('aria-expanded', 'true');
        //     // elements.show();
        // }

        // toggle icons
        // let to_show = $('#btn-nav-collapse img[hidden]');
        // let to_hide = $('#btn-nav-collapse img:not([hidden])');

        // to_hide.prop('hidden', true);
        // to_show.prop('hidden', false);
    }
}