-- database: ../db.sqlite3

-- Apagar dados do usuário teste
SELECT * FROM api_registry
    INNER JOIN auth_user ON api_registry.user_id = auth_user.id WHERE auth_user.username = 'teste';


DELETE FROM api_installmentitem
    WHERE registry_id IN (
        SELECT id FROM api_registry
            INNER JOIN auth_user ON api_registry.user_id = auth_user.id
            WHERE auth_user.username = 'teste'
        );

DELETE FROM api_registry WHERE user_id IN (SELECT id FROM auth_user WHERE username = 'teste');
DELETE FROM api_installment
    INNER JOIN auth_user ON api_registry.user_id = auth_user.id WHERE auth_user.username = 'teste';
DELETE FROM api_responsable
    INNER JOIN auth_user ON api_registry.user_id = auth_user.id WHERE auth_user.username = 'teste';
DELETE FROM api_invoice
    INNER JOIN auth_user ON api_registry.user_id = auth_user.id WHERE auth_user.username = 'teste';
DELETE FROM api_card
    INNER JOIN auth_user ON api_registry.user_id = auth_user.id WHERE auth_user.username = 'teste';