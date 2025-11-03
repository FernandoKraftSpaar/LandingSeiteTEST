# Tua Economia - Otimizador de Demanda Elétrica

## 🎯 Sobre o Aplicativo

**Tua Economia** é um calculador inteligente para otimização de contratos de demanda de energia elétrica. O aplicativo ajuda empresas a:

- ✅ Calcular a demanda contratada ótima baseada em dados históricos
- ✅ Estimar custos de subcontratação e sobrecontratação
- ✅ Projetar economia financeira através de ajustes estratégicos
- ✅ Recomendar o melhor momento para modificações contratuais

## 📚 Documentação Completa

Para uma explicação detalhada de como o aplicativo funciona, consulte:
**[CLEVER_CONTRACT_ADVISOR_DOCUMENTATION.md](../CLEVER_CONTRACT_ADVISOR_DOCUMENTATION.md)**

Este documento abrange:
- Arquitetura e tecnologias utilizadas
- Algoritmo de otimização detalhado
- Funcionalidades e casos de uso
- Conceitos técnicos e metodologia

## 🚀 Como Executar Localmente

### Pré-requisitos

- Node.js 18+ e npm instalados
- Git para clonar o repositório

### Instruções

```bash
# 1. Clone o repositório (se ainda não clonou)
git clone https://github.com/FernandoKraftSpaar/LandingSeiteTEST.git
cd LandingSeiteTEST/tuaeconomia

# 2. Instale as dependências
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev

# 4. Abra no navegador
# O aplicativo estará disponível em http://localhost:8080
```

### Comandos Disponíveis

```bash
npm run dev          # Inicia servidor de desenvolvimento com hot-reload
npm run build        # Gera build de produção na pasta /dist
npm run preview      # Visualiza o build de produção localmente
npm run lint         # Executa verificação de código (ESLint)
```

## 🌐 Por Que o App Funciona Apenas no Template de Desenvolvimento?

### O Problema

Este aplicativo foi construído usando a plataforma **Lovable.dev** e atualmente:

✅ **Funciona perfeitamente** no ambiente de desenvolvimento local (via `npm run dev`)  
❌ **NÃO está acessível** como um site publicado online

### As Razões

#### 1. **Aplicativo React Não Compilado**

Este é um aplicativo **React + TypeScript + Vite** que precisa de um processo de build:
- O código-fonte está em TypeScript (`.tsx`, `.ts`)
- Precisa ser **compilado** para JavaScript que o navegador entende
- Requer **bundling** de todos os módulos e dependências
- Não pode ser simplesmente "aberto" como arquivos HTML estáticos

#### 2. **Build de Produção Não Gerado**

A pasta `/dist` (onde fica o build de produção) está no `.gitignore`:
```
dist/          # ← Não está no repositório
build/
out/
```

Isso significa:
- O código compilado **não está** no Git
- Apenas o código-fonte está versionado
- É necessário rodar `npm run build` para gerar arquivos deployáveis

#### 3. **Nenhuma Configuração de Deploy Ativa**

Embora o repositório tenha configuração para Azure Static Web Apps:
- Nenhum **pipeline de CI/CD** está configurado
- Nenhuma **GitHub Action** para build automático
- As variáveis de ambiente de autenticação estão faltando
- O app não está conectado a nenhum serviço de hospedagem

#### 4. **Desenvolvido na Plataforma Lovable**

O aplicativo foi criado usando [Lovable](https://lovable.dev):
- Lovable é uma plataforma visual para desenvolvimento React
- Permite editar código via prompts e interface visual
- Tem deploy integrado, mas requer ação manual de "Publish"
- O projeto **não foi publicado** através do Lovable ainda

#### 5. **Separação Entre Landing Page e Calculadora**

O repositório contém duas aplicações distintas:
- **Landing Page**: Arquivos HTML estáticos no diretório raiz
- **Calculadora Tua Economia**: Aplicação React em `/tuaeconomia`
- Não há integração entre as duas
- Cada uma precisa de seu próprio processo de deploy

### Como Esta Estrutura Difere de Sites Tradicionais

| Site Estático Tradicional | Este Aplicativo React |
|---------------------------|----------------------|
| Arquivos `.html`, `.css`, `.js` prontos | Código-fonte que precisa compilação |
| Pode abrir direto no navegador | Precisa de servidor de desenvolvimento |
| Upload direto para hospedagem | Requer processo de build antes do deploy |
| Não precisa Node.js | Depende de Node.js e npm |

## 📦 Como Fazer o Deploy Online

Existem várias formas de publicar este aplicativo:

### Opção 1: Publicar via Lovable (Mais Fácil)

1. Acesse o [Projeto Lovable](https://lovable.dev/projects/f85cee55-0079-485e-87ef-98fe5e3c159b)
2. Clique em **Share → Publish**
3. Lovable gera uma URL pública automaticamente
4. O app fica hospedado na infraestrutura do Lovable

**Prós**: Sem configuração, deploy imediato  
**Contras**: URL fica no domínio lovable.dev

### Opção 2: Deploy Manual (Controle Total)

#### 2.1 Gerar Build de Produção

```bash
cd tuaeconomia
npm install
npm run build
```

Isso cria a pasta `/dist` com todos os arquivos otimizados.

#### 2.2 Fazer Deploy em Plataforma de Hospedagem

Escolha uma das opções abaixo e faça upload da pasta `/dist`:

**Vercel** (Recomendado para React)
```bash
npm install -g vercel
cd tuaeconomia
vercel --prod
```

**Netlify**
```bash
npm install -g netlify-cli
cd tuaeconomia
netlify deploy --prod --dir=dist
```

**GitHub Pages**
```bash
# Requer configuração de branch gh-pages
npm run build
# Copiar /dist para branch gh-pages
```

**Azure Static Web Apps**
- Conectar repositório GitHub
- Configurar GitHub Actions workflow
- Azure faz build e deploy automaticamente

### Opção 3: Integrar com Landing Page Principal

Para ter tudo em um único site:

1. **Build da calculadora**
```bash
cd tuaeconomia
npm run build
```

2. **Copiar para diretório público**
```bash
# Criar subdiretório no root
mkdir -p ../calculadora
cp -r dist/* ../calculadora/
```

3. **Atualizar staticwebapp.config.json**
```json
{
  "routes": [
    {
      "route": "/calculadora/*",
      "allowedRoles": ["anonymous"]
    }
  ]
}
```

4. **Link da landing page**
```html
<!-- Em index.html -->
<a href="/calculadora/">Calcular Economia</a>
```

## 🔧 Tecnologias Utilizadas

- **React 18.3**: Framework JavaScript
- **TypeScript**: Tipagem estática
- **Vite**: Build tool ultra-rápido
- **shadcn/ui**: Componentes de UI modernos
- **Tailwind CSS**: Estilização utility-first
- **React Hook Form**: Gerenciamento de formulários
- **Zod**: Validação de schemas
- **React Router**: Navegação entre páginas
- **TanStack Query**: Gerenciamento de estado assíncrono

## 📊 Fluxo de Trabalho de Desenvolvimento

```
1. Editar código em /src
   ↓
2. Vite detecta mudanças
   ↓
3. Hot Module Replacement (HMR)
   ↓
4. Navegador atualiza automaticamente
   ↓
5. (Quando pronto) npm run build
   ↓
6. Deploy da pasta /dist
```

## 🎓 Por Que Usar um Build Tool?

### Sem Build Tool (HTML tradicional)
```html
<!-- index.html -->
<script src="script1.js"></script>
<script src="script2.js"></script>
<script src="script3.js"></script>
<!-- Muitas requisições HTTP, sem otimização -->
```

### Com Vite (Moderno)
```typescript
// Código modular em TypeScript
import { Component } from './component'
import './styles.css'

// Vite combina tudo em bundles otimizados
// Minificação, tree-shaking, code-splitting automático
```

**Benefícios**:
- ✅ Um único arquivo JS otimizado (ou poucos chunks)
- ✅ CSS inline ou em arquivo separado minificado
- ✅ Assets otimizados e com hash de cache
- ✅ Código moderno transpilado para navegadores antigos
- ✅ Remover código não utilizado (tree-shaking)

## 🔐 Segurança e Privacidade

Este aplicativo é **100% client-side**:
- ✅ Todos os cálculos acontecem no navegador do usuário
- ✅ Nenhum dado é enviado para servidores externos
- ✅ Dados mensais permanecem no dispositivo local
- ✅ Sem necessidade de autenticação para usar a calculadora
- ✅ Sem armazenamento de dados pessoais

## 📞 Suporte

Para dúvidas sobre:
- **Funcionalidades do app**: Consulte a [documentação completa](../CLEVER_CONTRACT_ADVISOR_DOCUMENTATION.md)
- **Deploy e hospedagem**: Veja as seções acima de "Como Fazer o Deploy Online"
- **Código e desenvolvimento**: Abra uma issue no GitHub

## 📄 Licença

Este projeto está no repositório [FernandoKraftSpaar/LandingSeiteTEST](https://github.com/FernandoKraftSpaar/LandingSeiteTEST).

---

**Última atualização**: Novembro 2025  
**Status**: Pronto para deploy ✅
