# Clever Contract Advisor - Otimizador de Demanda Elétrica

## 📋 Overview

The Clever Contract Advisor is an **energy demand contracting calculator** designed to help businesses optimize their electricity contracts by analyzing historical consumption data and estimating potential savings through strategic contract adjustments.

## 🎯 Purpose

This application aims to:
- **Calculate optimal energy demand contracts** based on historical usage patterns
- **Estimate miscontracting costs** by analyzing differences between contracted and actual demand
- **Project financial savings** from optimized demand contracting
- **Recommend timing** for contract modifications to maximize savings

## 🏗️ Architecture

### Technology Stack

- **Frontend Framework**: React 18.3 with TypeScript
- **Build Tool**: Vite 5.4
- **UI Components**: shadcn/ui (based on Radix UI primitives)
- **Styling**: Tailwind CSS
- **State Management**: React Hooks + TanStack Query
- **Routing**: React Router DOM
- **Form Management**: React Hook Form with Zod validation

### Application Structure

```
clever-contract-advisor-main/
├── src/
│   ├── pages/
│   │   ├── Index.tsx          # Main calculator page
│   │   └── NotFound.tsx       # 404 page
│   ├── components/
│   │   ├── OptimizationForm.tsx       # Input parameters form
│   │   ├── MonthlyDataTable.tsx       # Historical data input table
│   │   ├── ResultsDisplay.tsx         # Optimization results display
│   │   └── ui/                        # shadcn/ui components
│   ├── lib/
│   │   ├── optimizer.ts       # Core optimization algorithm
│   │   └── utils.ts           # Utility functions
│   └── App.tsx                # Root component with routing
```

## 🧮 How It Works

### 1. Input Parameters (OptimizationForm)

Users configure the optimization criteria:

- **Risco de Ultrapassagem (%)**: Risk tolerance for exceeding contracted demand (lower = more conservative)
- **Contratação Mínima (kW)**: Minimum contractable demand set by utility company
- **Passo de Ajuste (kW)**: Step size for testing different demand values (e.g., 5 kW increments)
- **Delay de Implementação (meses)**: Months between requesting change and implementation
- **Frequência de Redução (meses)**: Minimum interval between demand reductions per utility rules

### 2. Historical Data Input (MonthlyDataTable)

Users input monthly electricity consumption data:

- **ano_mes**: Month/year (YYYY-MM format)
- **demanda_contratada_kw**: Currently contracted demand in kW
- **demanda_medida_kw**: Actual measured demand in kW
- **custo_demanda**: Cost per kW of contracted demand
- **custo_ultrapassagem**: Penalty cost per kW for exceeding contracted demand

### 3. Optimization Algorithm (optimizer.ts)

The core algorithm (`optimizeWithTiming`) performs these steps:

#### a) Statistical Analysis
- Calculates the risk-adjusted demand threshold using quantile analysis
- Determines viable demand contracting range based on historical data

#### b) Candidate Generation
- Creates a grid of potential demand values within the viable range
- Rounds candidates to the specified step size (e.g., multiples of 10 kW)

#### c) Cost Matrix Computation
For each candidate demand level and each historical month:
```typescript
cost = (contracted_demand × demand_tariff) + (excess_demand × penalty_tariff)
where excess_demand = max(0, measured_demand - contracted_demand)
```

#### d) Timing Optimization
- Tests all possible request months (s_req)
- Calculates effective month (s_eff) based on implementation delay
- Applies utility frequency rules for demand reductions
- Computes corrected savings with monetary inflation adjustment (IGPM)

#### e) Best Solution Selection
Returns the combination of:
- **x**: Optimal demand to contract (kW)
- **s_req**: Best month to request the change
- **s_eff**: Month when the change becomes effective
- **economia_corr**: Total projected savings with inflation correction

### 4. Results Display (ResultsDisplay)

Shows the optimization outcome:

- **Economia Projetada**: Total savings in BRL (Brazilian Real)
- **Demanda Ótima**: Recommended contracted demand in kW
- **Mês de Solicitação**: When to request the contract modification
- **Início Vigência**: When the new contract takes effect
- **Recomendações**: Action items and monitoring advice

## 💡 Key Features

### Conservative Approach
The algorithm uses a **conservative optimization method** that:
- Balances between reducing costs and avoiding penalty charges
- Uses quantile-based risk assessment to prevent frequent overshoots
- Respects utility company constraints (minimum contracts, change frequency)

### Monetary Correction
- Applies IGPM (General Market Price Index) for inflation adjustment
- Provides present-value calculations for future savings
- More accurate long-term financial projections

### Practical Constraints
- Honors minimum contract requirements
- Respects change request delays
- Enforces reduction frequency rules
- Rounds to utility-acceptable increments

## 📊 Example Use Case

**Scenario**: A factory with fluctuating monthly demand wants to optimize their contract.

**Input**:
- Current contract: 500 kW
- Risk tolerance: 5%
- Historical data shows demand ranges from 380-520 kW
- Step size: 10 kW
- Implementation delay: 1 month

**Process**:
1. Algorithm calculates 95th percentile of demand ≈ 495 kW
2. Tests contracts from 495 kW to 570 kW in 10 kW steps
3. For each value, calculates costs over all months
4. Finds optimal timing considering delay and savings

**Output**:
- Recommended contract: 490 kW
- Request in: Month 3 (March)
- Effective from: Month 4 (April)
- Projected savings: R$ 12,500.00

## 🔍 Miscontracting Detection

The app identifies two types of miscontracting:

### Over-Contracting
- Contracted demand significantly exceeds actual usage
- Paying for unused capacity
- **Solution**: Reduce contract to optimal level

### Under-Contracting
- Actual demand frequently exceeds contract
- Incurring penalty charges
- **Solution**: Increase contract to avoid penalties

The optimization algorithm finds the **sweet spot** that minimizes total costs (contract + penalties).

## 🚀 Development Platform: Lovable

### What is Lovable?

Lovable (lovable.dev) is a **visual development platform** that enables building React applications through:
- AI-assisted coding and prompting
- Real-time preview and iteration
- Automatic Git integration
- Built-in deployment capabilities

### Why This App Uses Lovable

The Clever Contract Advisor was built using Lovable because:

1. **Rapid Prototyping**: Complex UI components (forms, tables, charts) can be created quickly
2. **TypeScript + React Best Practices**: Auto-generated code follows modern patterns
3. **Component Library Integration**: Pre-configured with shadcn/ui for professional UI
4. **Development Workflow**: Seamless local development with Vite hot-reload

### Why It Works in Template but Not Online (Deployment Issues)

The app may not be accessible online for several reasons:

#### 1. **Development-Only State**
- The app exists in the **Lovable development environment**
- Code is in the repository but **not yet deployed** to a live server
- Requires explicit "Publish" action in Lovable platform

#### 2. **Missing Build Artifacts**
- The `/dist` folder (production build) is gitignored
- Source code exists but compiled bundle doesn't
- Needs `npm run build` to generate deployable files

#### 3. **Deployment Configuration**
The repository includes Azure Static Web App config (`staticwebapp.config.json`) but:
- No Azure deployment pipeline is configured
- No GitHub Actions workflow for automated builds
- Authentication setup incomplete (missing environment variables)

#### 4. **Environment Dependencies**
The app requires:
- Node.js environment (not just static HTML)
- Build step to compile TypeScript + React
- Module bundling via Vite
- Cannot be opened directly in browser like simple HTML files

#### 5. **Separation of Concerns**
- The main repository contains a **landing page** (index.html)
- The **calculator app** is nested in `clever-contract-advisor-main/`
- No integration between the two - they're separate applications

### How to Deploy (Solutions)

To make the app accessible online:

#### Option A: Lovable Publishing
1. Open the [Lovable Project](https://lovable.dev/projects/f85cee55-0079-485e-87ef-98fe5e3c159b)
2. Click **Share → Publish**
3. Lovable handles hosting and provides a live URL

#### Option B: Manual Deployment
```bash
cd clever-contract-advisor-main/clever-contract-advisor-main
npm install
npm run build
# Deploy the /dist folder to any static host:
# - Vercel
# - Netlify
# - GitHub Pages
# - Azure Static Web Apps
```

#### Option C: Integrate with Main Site
- Build the app and copy `/dist` contents to repository root
- Update `staticwebapp.config.json` to route to calculator
- Configure Azure Static Web Apps deployment

## 🔐 Security & Privacy

The app operates **entirely client-side**:
- No data is sent to external servers
- All calculations happen in the browser
- Monthly data remains on user's device
- No authentication required for calculator functionality

## 📝 Future Enhancements

Potential improvements:
- **Data Import**: CSV/Excel file upload for monthly data
- **Historical Charts**: Visualize demand patterns over time
- **Multi-Scenario Analysis**: Compare multiple optimization strategies
- **Export Reports**: PDF generation with recommendations
- **Real IGPM Integration**: Fetch actual inflation indices
- **Advanced Tariff Models**: Support for different utility pricing structures

## 🎓 Technical Concepts

### Quantile-Based Risk Assessment
Uses statistical quantiles to determine appropriate contracting levels:
- 95th percentile (5% risk) = contract covers 95% of historical peaks
- More conservative = higher quantile = larger contract

### Present Value Calculation
Applies inflation correction to future savings:
- IGPM factors adjust future cash flows to present value
- More accurate ROI calculations for contract changes

### Grid Search Optimization
Exhaustive search through discrete candidate values:
- Tests all combinations of (demand, timing)
- Guaranteed to find optimal solution within search space
- Computationally efficient for typical dataset sizes

## 📚 References

- **Tariff Structure**: Based on Brazilian electricity regulations (ANEEL)
- **IGPM Index**: Brazil's General Market Price Index for inflation
- **Demand Contracting**: Commercial/industrial electricity rate structures

---

**Note**: This documentation reflects the application as of November 2025. For the latest version, refer to the [Lovable Project](https://lovable.dev/projects/f85cee55-0079-485e-87ef-98fe5e3c159b) or the GitHub repository.
