import RegistryView from "./registries.js";

$(() => {
    let home_view = new HomeView();
    home_view.init();
});

const URLS = {
    'Dashboards': '/home/nav-dash',
    'Registros': '/home/nav-regs',
    'Cartões e Faturas': '/home/nav-cards',
};


class HomeView
{
    #currentNavBtn = undefined;
    #currentTitle = '';
    #initialNavBtn;
    #regview = new RegistryView();


    constructor() {
        // configurando nav-btns
        let nav_btns = $('.home-nav .nav-link');

        for(let i=0; i<nav_btns.length; i++) {
            $(nav_btns[i]).on('click', async (evt) => await this.#navBtn_clicked(evt));
        }

        this.#initialNavBtn = nav_btns[1];

        // configurando animações
        $(document).on('click', '.btn-rotate', (evt) => $(evt.currentTarget).toggleClass('btn-rotated'));
        $(document).on('click', '.btn-rotate-full', (evt) => $(evt.currentTarget).toggleClass('btn-rotated-full'));
    }
    
    init() {
        $(this.#initialNavBtn).click();

        // let table = new Table({parentId: '#home-content', columns: ['Col1', 'Col2', 'Col3']});
    }

    async #navBtn_clicked(evt) {
        evt.preventDefault();
        let jbtn = $(evt.currentTarget);
        
        
        let title = jbtn.prop('name');
        let url = URLS[title];

        // bloqueando clicks múltiplos em uma mesma nav
        // if (this.#currentTitle == title) {
        //     return;
        // }

        if (!url) { // TODO: o evento deve ser processado separadamente
            console.log('unbinded nav event:', title);
            return;
        }

        if (this.#currentNavBtn) {
            this.#currentNavBtn.removeClass('shadow');
            this.#currentNavBtn.css('background-color', '');
            this.#currentNavBtn.children().css('color', '');
        }
        
        this.#currentTitle = title;
        this.#currentNavBtn = jbtn;
        this.#currentNavBtn.addClass('shadow');
        jbtn.css('background-color', 'var(--primary-color)');
        jbtn.children().css('color', 'white');

        // exibindo título
        $('#home-title').text(title);

        // alterando conteúdo
        const parent = '#home-content';
        
        if (title == 'Registros') {
            await this.#regview.updateContent(parent);
        } else {
            const content = await $.get(url);
            $(parent).html(content);
        }
        
        
    }
}