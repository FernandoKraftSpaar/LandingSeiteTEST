#!/bin/bash

# Script para testar a API DAB após configuração
# Execute: chmod +x test_dab_api.sh && ./test_dab_api.sh

# Configurações (ajuste conforme necessário)
BASE_URL="${1:-https://jolly-tree-034e7b00f.5.azurestaticapps.net}"
API_PATH="/data-api/rest/Equipamento"
FULL_URL="${BASE_URL}${API_PATH}"

echo "🧪 Testando API DAB em: $FULL_URL"
echo "================================================"

# Função para mostrar resultado do teste
test_result() {
    local status=$1
    local description=$2
    local response=$3
    
    if [ $status -eq 0 ]; then
        echo "✅ $description"
    else
        echo "❌ $description"
        echo "   Resposta: $response"
    fi
    echo ""
}

# Teste 1: GET - Listar equipamentos
echo "📋 Teste 1: GET - Listar equipamentos"
response=$(curl -s -w "\n%{http_code}" -X GET "$FULL_URL" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    test_result 0 "GET /Equipamento - Status 200 OK"
    echo "   📊 Dados retornados:"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    test_result 1 "GET /Equipamento - Status $http_code" "$body"
fi

# Teste 2: POST - Criar equipamento (se autenticado)
echo "🆕 Teste 2: POST - Criar equipamento de teste"
test_data='{
    "nome": "Teste API Script",
    "potencia": 2.5,
    "horas_uso": 6.0,
    "categoria": "Teste",
    "observacoes": "Equipamento criado via script de teste"
}'

response=$(curl -s -w "\n%{http_code}" -X POST "$FULL_URL" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "$test_data")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" = "201" ] || [ "$http_code" = "200" ]; then
    test_result 0 "POST /Equipamento - Status $http_code"
    echo "   📦 Equipamento criado:"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    test_result 1 "POST /Equipamento - Status $http_code (pode ser normal se não autenticado)" "$body"
fi

# Teste 3: Verificar autenticação
echo "🔐 Teste 3: Verificar endpoint de autenticação"
auth_response=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}/.auth/me" \
    -H "Accept: application/json")

auth_http_code=$(echo "$auth_response" | tail -n1)
auth_body=$(echo "$auth_response" | head -n -1)

if [ "$auth_http_code" = "200" ]; then
    test_result 0 "GET /.auth/me - Status 200 OK"
    echo "   👤 Info de autenticação:"
    echo "$auth_body" | jq '.' 2>/dev/null || echo "$auth_body"
else
    test_result 1 "GET /.auth/me - Status $auth_http_code" "$auth_body"
fi

# Teste 4: GraphQL endpoint (opcional)
echo "🔍 Teste 4: GraphQL endpoint"
graphql_query='{"query": "{ equipamentos { id nome potencia } }"}'
graphql_response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/data-api/graphql" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "$graphql_query" 2>/dev/null)

graphql_http_code=$(echo "$graphql_response" | tail -n1)
graphql_body=$(echo "$graphql_response" | head -n -1)

if [ "$graphql_http_code" = "200" ]; then
    test_result 0 "POST /data-api/graphql - Status 200 OK"
    echo "   🔗 Resposta GraphQL:"
    echo "$graphql_body" | jq '.' 2>/dev/null || echo "$graphql_body"
else
    test_result 1 "POST /data-api/graphql - Status $graphql_http_code" "$graphql_body"
fi

echo "================================================"
echo "🏁 Testes concluídos!"
echo ""
echo "💡 Dicas para troubleshooting:"
echo "   - Status 401/403: Problema de autenticação/autorização"
echo "   - Status 400: Problema na connection string ou payload"
echo "   - Status 500: Problema no banco de dados ou configuração"
echo "   - Status 404: Endpoint não encontrado (verifique deploy)"
echo ""
echo "📖 Consulte o guia completo em: DAB_CONFIGURATION_GUIDE.md"