export default class DashboardView {
    #jquery;

    constructor(jquery) {
        this.#jquery = jquery;
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos - Estáticos
    static async create() {
        let jquery = $(await $.get('/home/nav-dash'));
        return new DashboardView(jquery);
    }

    //-----------------------------------------------------------------------------
    // Métodos Públicos
    jquery() { return this.#jquery; }

    //-----------------------------------------------------------------------------
}