# Financeiro API
Sistema para controle financeiro.

## Endpoints

### Autenticação de Usuários
A API conta com o modelo de token para a utilização dos serviços. Todos os endpoints que exigem a autenticação recebem o token no cabeçalho da requisição, no padrão `Authorization: Token <meu-token>`. Para mais detalhes, leia [Gerenciando usuários e suas sessões](#gerenciando-usuários-e-suas-sessões).

------------------------------------------------------------------------------------------
### Usuários e sessões

<details id="post-auth">
 <summary><code>POST</code> <code><b>/api/auth</b></code> <code>(autenticação do usuário)</code>
</summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| username | body | obrigatório | string | - |
| password | body | obrigatório | string | - |


#### Responses
| http code | response |
| --- | --- |
| `200 OK` | `{"token": "<token>"}` |
| `400 Bad Request` | |

</details>

<details>
 <summary><code>POST</code> <code><b>/api/createAccount</b></code> <code>(gera um novo usuário)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| username | body | obrigatório | string | nome de usuário para autenticação |
| email | body | obrigatório | email | e-mail do usuário |
| password | body | obrigatório | string | senha do usuário |
| first_name | body | obrigatório | string | primeiro nome do usuário |
| last_name | body | obrigatório | string | último nome do usuário |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [SuccessError](#successerror) |
| `400 Bad Request` | [Message](#message) |

</details>

<details>
 <summary><code>POST</code> <code><b>/api/deleteAccount</b></code> <code>(apaga todos os dados do usuário autenticado)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |

#### Responses
| http code | response |
| --- | --- | --- |
| `200 OK` | [SuccessError](#successerror) |
| `404 Not Found` | [Message](#message) |

</details>

<details>
 <summary><code>GET</code> <code><b>/api/getUser</b></code> <code>(consulta os dados do usuário autenticado)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |

#### Responses
| http code | response |
| --- | --- | --- |
| `200 OK` | [User](#user) |

</details>

------------------------------------------------------------------------------------------
### Cartões

<details>
  <summary><code>GET</code> <code><b>/api/getCards</b></code> <code>(consulta os cartões do usuário)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Card[]](#card) |
| `404 Not Found` | [Message](#message) |

</details>

<details>
  <summary><code>GET</code> <code><b>/api/getCard/{id}</b></code> <code>(consulta um cartão pelo ID)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |
| id | path | obrigatório | int | id do cartão |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Card](#card) |
| `403 Forbidden` | [Message](#message) |
| `404 Not Found` | [Message](#message) |

</details>

<details>
  <summary><code>POST</code> <code><b>/api/addCard</b></code> <code>(cria um novo cartão)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | padrão | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| name | body | obrigatório | string |
| closing_day | body | obrigatório | int | - | dia de fechamento do cartão |
| due_day | body | obrigatório | int | - | dia de vencimento do cartão |
| limit | body | obrigatório | float | - | limite do cartão |
| closing_previous_month | body | opcional | boolean | false | se o dia de fechamento corresponde ao mês anterior da fatura |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Card](#card) |
| `400 Bad Request` | [Message](#message) |

</details>

------------------------------------------------------------------------------------------
### Faturas

<details>
  <summary><code>GET</code> <code><b>/api/getInvoice/{id}</b></code> <code>(consulta uma fatura por ID)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | padrão | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| id | path | obrigatório | int |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Card](#card) |
| `403 Forbidden` | [Message](#message) |
| `404 Not Found` | [Message](#message) |

</details>

<details>
  <summary><code>GET</code> <code><b>/api/getInvoiceByCard</b></code> <code>(consulta a fatura pelo cartão)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | padrão | opções | descrição |
| --- | --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | - | token de autenticação no formato `token <token-api>` |
| q | body | obrigatório | int \| string | - | - | dado para consulta |
| field | body | opcional | string | id | id \| name | campo de consulta do cartão |
| date_ref | body | opcional | date (AAA-MM-01) | `FIRST_DAY_CURRENT_MONTH` | - | mês/ano da fatura |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Card](#card) |
| `403 Forbidden` | [Message](#message) |
| `404 Not Found` | [Message](#message) |

</details>

------------------------------------------------------------------------------------------
### Transações financeiras (registros)

<details>
 <summary><code>GET</code> <code><b>/api/getRegistries</b></code> <code>(consulta dos registros por filtros)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| value | body | opcional | float | - | valor exato do registro |
| value__gt | body | opcional | float | - | valor maior que o do registro |
| value__gte | body | opcional | float | - | valor maior ou igual ao do registro |
| value__lt | body | opcional | float | - | valor menor que o do registro |
| value__lte | body | opcional | float | - | valor menor que ou igual ao do registro |
| title | body | opcional | string | - | valor exato do título |
| title__icontains | body | opcional | string | - | o título contém (case-insensitive) |
| type_in | body | opcional | int | `0` \| `1` | registro do tipo entrada ou saída, sendo 1 para entradas e 0 para saídas |
| occurrance_init | body | opcional | datetime (AAAA-MM-DD HH:MM:SS) | - | data/hora inicial da ocorrência |
| occurrance_end | body | opcional | datetime (AAAA-MM-DD HH:MM:SS) | - | data/hora limite da ocorrência |
| date_ref | body | opcional | date (AAAA-MM-DD) | - | data de referência |
| card_id | body | opcional | int | - | id do cartão |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Registry[]](#registry) |
| `400 Bad Request` | [Message](#message) |

</details>

<details>
 <summary><code>GET</code> <code><b>/api/getRegistry/{id}</b></code> <code>(consulta um registro a partir de seu id)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| id | path | obrigatório | int | - | id para consulta |

O retorno é ordenado por `occurrance`, do mais recente para o mais antigo.

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry[]](#registry) |
| `403 Forbidden` | [Message](#message) |
| `404 Not Found` | [Message](#message) |

</details>

<details id="add-registry-post">
 <summary><code>POST</code> <code><b>/api/addRegistry</b></code> <code>(gera um novo registro)</code></summary>

#### Parcelamento de um registro
A API permite a criação de um registro dividivo em parcelas, ideal para compras parceladas no cartão.

>o campo `value` corresponde ao valor de cada parcela, sendo o valor total da transação a soma de todas as parcelas

>por padrão, o `status` das parcelas subsequentes é definido como `ACCOUNTED`, o qual representa a compra faturada, porém não paga

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | padrão | descrição |
| --- | --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | - | token de autenticação no formato `token <token-api>` |
| title | body | obrigatório | string |
| value | body | obrigatório | float |
| occurrance | body | obrigatório | string | - | - | formato DD/MM/AAAA HH:MM |
| date_ref | body | obrigatório | string | - | - | formato AAAA-MM |
| status | body | opcional | string | PENDING \| OK \| ACCOUNTED | PENDING |
| type_in | body | opcional | boolean | - | false |
| installment_current | body | opcional | int | - | - | parcela atual do registro |
| installment_total | body | opcional | int | - | - | total de parcelas do registro |
| description | body | opcional | string |
| category | body | opcional | string |
| card_id | body | opcional | int |
| responsable_id | body | opcional | int |

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry](#registry)| registro criado com sucesso |
| `400 Bad Request` | [Message](#message) | IDs ou parâmetros inválidos |
| `403 Forbidden` | [Message](#message) | erro de acesso |

</details>

<details>
 <summary><code>POST</code> <code><b>/api/updateRegistry</b></code> <code>(atualiza um registro existente)</code> TODO</summary>

#### Parâmetros
Aceita qualquer parâmetro de [POST /api/addRegistry](#add-registry-post) de forma opcional, sendo apenas `Authorization` e `id` obrigatório.

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry](#registry)|
| `400 Bad Request` | [Message](#message) |
| `403 Forbidden` | [Message](#message) |
| `404 Not Found` | [Message](#message) |

</details>

<details>
 <summary><code>POST</code> <code><b>/api/deleteRegistry/{id}</b></code> <code>(apaga um registro)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| id | path | obrigatório | int | - | id do registro |


#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry](#registry)|
| `400 Bad Request` | [Message](#message) |
| `403 Forbidden` | [Message](#message) |
| `404 Not Found` | [Message](#message) |

</details>

------------------------------------------------------------------------------------------
## Estruturas de dados

### Registry
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `id` | int |
| `title` | string |
| `value` | float |
| `value_formatted` | string | `value` no formato R$ 0,00 |
| `status` | string |
| `occurrance` | string | formato AAAA-MM-DD HH:MM |
| `occurrance_formatted` | string | `occurrance` no formato DD MMM AA, HhMM, sendo o mês em texto |
| `description` | string \| null |
| `category` | string |
| `date_ref` | string | formato AAAA-MM |
| `type_in` | boolean |
| `card_name` | string |
| `responsable_name` | string |
| `responsable_id` | int \| null |
| `invoice_id` | int \| null |
| `installment_formatted` | string | formato X de X (caso haja parcelas) |

### Message
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `detail` | string | detalhamento da mensagem |

### SuccessError
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `success` | boolean | operação realizada com sucesso |
| `detail` | string | detalhamento da mensagem |

### User
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `id` | int |
| `username` | string |
| `email` | string |
| `first_name` | string |
| `last_name` | string |

### Card
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `id` | int |
| `name` | string |
| `closing_day` | int | dia de fechamento |
| `due_day` | int | dia de vencimento |
| `limit`| float | limite atual do cartão (será utilizado como padrão para novas faturas) |
| `closing_previous_month`| boolean | se o dia de fechamento da fatura corresponde ao mês anterior (util para faturas que fecham no final do mês anterior) |


------------------------------------------------------------------------------------------
