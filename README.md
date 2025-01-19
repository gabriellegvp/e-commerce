# Sistema de E-commerce Simples

Uma aplicação Django para gerenciar um e-commerce, com funcionalidades de carrinho de compras, controle de inventário e integração com Stripe.

## Recursos
- Adicionar/remover itens no carrinho.
- Processamento de pagamentos via Stripe.
- Gerenciamento de estoque.

## Como Configurar
1. Clone o repositório:  
   git clone <url-do-repositorio>
2. Instale as dependências:  
   pip install -r requirements.txt
3. Configure as variáveis de ambiente para Stripe no arquivo .env.
4. Execute a aplicação:  
   python manage.py runserver

## Endpoints Principais
- POST /cart/add - Adicionar itens ao carrinho.
- POST /checkout - Processar pagamento.
- GET /products - Listar produtos disponíveis.
