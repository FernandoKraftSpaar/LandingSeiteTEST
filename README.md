# LandingSeiteTEST

Das ist ein Test für unsere erste öffentliche Seite

## 📁 Estrutura do Repositório

Este repositório contém duas aplicações principais:

### 1. Landing Page Principal
- Arquivos HTML estáticos no diretório raiz
- `index.html`, `login.html`, `dashboard.html`, etc.
- Pronta para deploy direto

### 2. Tua Economia - Calculadora de Demanda Elétrica
- Localizada em: **`/tuaeconomia`**
- Aplicativo React para otimização de contratos de energia
- Requer processo de build antes do deploy

## 📚 Documentação

- **[Tua Economia - Documentação Completa](./CLEVER_CONTRACT_ADVISOR_DOCUMENTATION.md)**: Explicação detalhada de como o calculador funciona
- **[Tua Economia - Guia de Deploy](./tuaeconomia/README_DEPLOYMENT.md)**: Como fazer deploy online e por que não está acessível atualmente

## 🚀 Como Executar

### Landing Page
Simplesmente abra `index.html` em um navegador ou faça deploy em qualquer host estático.

### Calculadora Tua Economia
```bash
cd tuaeconomia
npm install
npm run dev
```

Acesse http://localhost:8080

## 📊 Status

| Componente | Status | Acessível Online? |
|------------|--------|-------------------|
| Landing Page | ✅ Pronto | Depende do deploy |
| Calculadora Tua Economia | ✅ Funcional localmente | ❌ Não (precisa deploy) |

## 📝 Notas

A calculadora foi movida de `clever-contract-advisor-main/clever-contract-advisor-main` para `/tuaeconomia` para simplificar a estrutura do repositório.
