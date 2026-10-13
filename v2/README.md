### Usuário e sessão

<details id="create-user">
 <summary><code>POST</code> <code><b>/auth/createUser</b></code> <code>(gera um novo usuário)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| username | body | obrigatório | string | nome de usuário para autenticação |
| email | body | obrigatório | email | e-mail do usuário |
| password | body | obrigatório | string | senha do usuário |
| firstName | body | obrigatório | string | primeiro nome do usuário |
| lastName | body | obrigatório | string | último nome do usuário |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [SuccessError](#successerror) |
| `400 Bad Request` | [SuccessError](#successerror) |

</details>

<details id="get-user">
 <summary><code>GET</code> <code><b>/auth/getUser</b></code> <code>(consulta os dados do usuário autenticado)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [User](#user) |
| `401 Unauthorized` | [SuccessError](#successerror) |

</details>

<details id="update-user">
 <summary><code>POST</code> <code><b>/auth/updateUser</b></code> <code>(atualiza os dados do usuário autenticado)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |
| firstName | body | opcional | string |
| lastName | body | opcional | string |
| email | body | opcional | string |
| password | body | opcional | string |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [User](#user) |
| `401 Unauthorized` | [SuccessError](#successerror) |

</details>

<details>
 <summary><code>POST</code> <code><b>/api/deleteUser</b></code> <code>(apaga todos os dados do usuário autenticado)</code></summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| Authorization | header | obrigatório | string | token de autenticação no formato `token <token-api>` |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [SuccessError](#successerror) |
| `404 Not Found` | [SuccessError](#successerror) |

</details>

<details id="auth">
 <summary><code>POST</code> <code><b>/auth/generateToken</b></code> <code>(autenticação do usuário)</code>
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
| `400 Bad Request` | [SuccessError](#successerror) |

</details>

<details id="logout">
 <summary><code>GET</code> <code><b>/auth/logout</b></code> <code>(logout do usuário)</code>
</summary>

#### Parâmetros
| nome | localização | tipo | tipo de dado | descrição |
| --- | --- | --- | --- | --- |
| username | body | obrigatório | string | - |
| password | body | obrigatório | string | - |

#### Responses
| http code | response |
| --- | --- |
| `200 OK` | [SuccessError](#successerror) |

</details>


### Carteira

<details id="create-wallet">
 <summary><code>POST</code> <code><b>/wallet/create</b></code> <code>(gera uma nova carteira)</code>
</summary>

Uma carteira representa um conjunto de [registros](#registry). Combinado com a opção `cardType`, pode ser utilizado para representar um cartão com histórico de transações pela ocorrência do registro (fatura) e outras funcionalidades.

#### Parâmetros
| nome | localização | tipo | tipo de dado | padrão | descrição |
| --- | --- | --- | --- | --- | --- |
| name | body | obrigatório | string |
| cardType | body | opcional | boolean | true |
| limit | body | obrigatório se cardType fornecido | decimal |
| date | body | obrigatório se cardType fornecido | date | | formato `AAAA-MM` |

#### Responses
| http code | response |
| --- | --- |
| `400 Bad Request` | [SuccessError](#successerror) |
| `400 Bad Request` | [SuccessError](#successerror) |

</details>


# Estruturas de dados

### SuccessError
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `detail` | string \| undefined | detalhamento da mensagem |

### User
| nome | tipo de dado | descrição |
| --- | --- | --- |
| `id` | int |
| `username` | string |
| `email` | string |
| `firstName` | string |
| `lastName` | string |

### Registry
| nome | tipo de dado | descrição |
| --- | --- | --- |

### Wallet
| nome | tipo de dado | descrição |
| --- | --- | --- |
|