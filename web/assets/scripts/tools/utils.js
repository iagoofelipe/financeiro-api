export const STATUS_PENDING_HTML = '<span class="badge-custom bg-pendente">Pendente</span>';
export const STATUS_LATE_HTML = '<span class="badge-custom bg-atrasado">Atrasado</span>';
export const STATUS_OK_HTML = '<span class="badge-custom bg-contabilizado">Contabilizado</span>';

export function get_status_html_by_name(name) {
    switch (name) {
    case 'PENDING':
        return STATUS_PENDING_HTML;
    case 'LATE':
        return STATUS_LATE_HTML;
    case 'OK':
        return STATUS_OK_HTML;
    default:
        return '<span>?</span>';
    }
}

export function number_to_coin_format(val) {
    return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}