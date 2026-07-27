$(() => {
    // animação rotação
    $(document).on('click', '.btn-rotate', (evt) => $(evt.currentTarget).toggleClass('btn-rotated'));
});