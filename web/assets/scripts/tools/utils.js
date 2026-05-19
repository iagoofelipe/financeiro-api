export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const REG_STATUS_HTML = {
    PENDING: '<span class="badge-custom bg-pendente">Pendente</span>',
    OK: '<span class="badge-custom bg-contabilizado">Contabilizado</span>',
    LATE: '<span class="badge-custom bg-atrasado">Atrasado</span>',
};

export function getElementsByXPath(xpath, context = document) {
    let result = document.evaluate(xpath, context, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    let array = [];

    for (let i = 0; i < result.snapshotLength; i++) {
        array.push(result.snapshotItem(i));
    }

    return array;
}