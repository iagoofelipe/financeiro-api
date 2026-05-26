# Financeiro API
Sistema para controle financeiro.

------------------------------------------------------------------------------------------
### Autenticação de Usuários
A API conta com o modelo de token para a utilização dos serviços. Todos os endpoints que exigem a autenticação recebem o token no cabeçalho da requisição, no padrão `Authorization: Token <meu-token>`. Para mais detalhes, leia [Gerenciando usuários e suas sessões](#gerenciando-usuários-e-suas-sessões).

------------------------------------------------------------------------------------------
### Gerenciando usuários e suas sessões

<details id="post-auth">
 <summary><code>POST</code> <code><b>/auth</b></code> <code>(autenticação do usuário)</code>
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
 <summary><code>POST</code> <code><b>/createUser</b></code> <code>(gera um novo usuário)</code></summary>

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
| `200 OK` | [User](#user) |
| `400 Bad Request` | [Message](#message) |

</details>

------------------------------------------------------------------------------------------
### Gerenciando transações financeiras (registros)

<details>
 <summary><code>GET</code> <code><b>/getRegistries</b></code> <code>(consulta dos registros por filtros)</code></summary>

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
| status | body | opcional | string | `PENDING` \| `OK` \| `LATE` | status do registro |
| type_in | body | opcional | int | `0` \| `1` | registro do tipo entrada ou saída, sendo 1 para entradas e 0 para saídas |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [Registry[]](#registry) |
| `400 Bad Request` | |

</details>

<details>
 <summary><code>GET</code> <code><b>/getRegistry/{id}</b></code> <code>(consulta um registro a partir de seu id)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| id | path | obrigatório | int | - | id para consulta |

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry[]](#registry) |
| `404 Not Found` | [Message](#message) |
| `405 Not Allowed` | [Message](#message) | usuário sem permissão |

</details>

<details id="add-registry-post">
 <summary><code>POST</code> <code><b>/addRegistry</b></code> <code>(gera um novo registro)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| title | body | obrigatório | string |
| value | body | obrigatório | float |
| status | body | obrigatório | string | `PENDING` \| `OK` \| `LATE` |
| occurrance | body | obrigatório | string | formato AAAA-MM-DD HH:MM |
| ref_year | body | obrigatório | int |
| ref_month | body | obrigatório | int |
| type_in | body | obrigatório | boolean |
| description | body | opcional | string |
| invoice_id | body | opcional | int |
| responsable_id | body | opcional | int |

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry](#registry)| registro criado com sucesso |
| `400 Bad Request` | [Message](#message) | IDs ou parâmetros inválidos |
| `403 Forbidden` | [Message](#message) | erro de acesso |

</details>

<details>
 <summary><code>POST</code> <code><b>/updateRegistry/{id}</b></code> <code>(atualiza um registro existente)</code> TODO</summary>

#### Parâmetros
Aceita qualquer parâmetro de [POST /addRegistry](#add-registry-post) de forma opcional, sendo apenas `Authorization` obrigatório.

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry](#registry)| registro atualizado |
| `400 Bad Request` | [Message](#message) | IDs ou parâmetros inválidos |
| `403 Forbidden` | [Message](#message) | erro de acesso |

</details>

<details>
 <summary><code>POST</code> <code><b>/deleteRegistry/{id}</b></code> <code>(apaga um registro)</code> TODO</summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | opções | descrição |
| --- | --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | - | token de autenticação no formato `token <token-api>` |
| id | path | obrigatório | int | - | id para consulta |

#### Responses
| http code | response | descrição |
| --- | --- | --- |
| `200 OK` | [Registry](#registry)| registro atualizado |
| `400 Bad Request` | [Message](#message) | IDs ou parâmetros inválidos |
| `403 Forbidden` | [Message](#message) | erro de acesso |

</details>

------------------------------------------------------------------------------------------
#### Estruturas de dados

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
| `date_ref` | string | formato AAAA-MM |
| `type_in` | boolean |
| `description` | string \| null |
| `card_id` | string \| null |
| `card_name` | string |
| `invoice_id` | int \| null |
| `invoice_ref` | string \| null | formato AAAA-MM |
| `responsable_name` | string |
| `responsable_id` | int \| null |

### Message
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `detail` | string | detalhamento da mensagem |

### User
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `id` | int |
| `username` | string |
| `email` | string |
| `first_name` | string |
| `last_name` | string |

------------------------------------------------------------------------------------------
