$(() => {
    let home_view = new HomeView();
    home_view.init();
});


class HomeView
{
    #currentNavBtn = undefined;
    #currentTitle = '';

    constructor() {
        // configurando nav-btns
        let nav_btns = $('.home-nav .nav-link');

        for(let i=0; i<nav_btns.length; i++) {
            $(nav_btns[i]).click((evt) => this.#navBtn_clicked(evt));
        }

        $(nav_btns[1]).click();
    }

    init() {

    }

    #navBtn_clicked(evt) {
        evt.preventDefault();
        let jbtn = $(evt.currentTarget);
        
        
        let title = jbtn.prop('name');

        // bloqueando clicks múltiplos em uma mesma nav
        // if (this.#currentTitle == title) {
        //     return;
        // }

        if (title == 'Sair') {
            alert('logout required');
            return;
        }

        if (this.#currentNavBtn) {
            this.#currentNavBtn.css('background-color', '');
            this.#currentNavBtn.children().css('color', '');
        }
        
        this.#currentTitle = title;
        this.#currentNavBtn = jbtn;
        jbtn.css('background-color', 'var(--primary-color)');
        jbtn.children().css('color', 'white');


        // exibindo título
        $('#home-title').text(title);

        // alterando conteúdo
        let url = jbtn.prop('href');
        $('#home-content').load(url, () => {
            $('#home-content .btn-rotate').click((evt) => $(evt.currentTarget).toggleClass('btn-rotated'));
            $('#home-content .btn-rotate-full').click((evt) => $(evt.currentTarget).toggleClass('btn-rotated-full'));
        });

    }
}