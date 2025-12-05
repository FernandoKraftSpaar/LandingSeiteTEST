import * as fs from "fs";

/**
 * Interface representando uma linha do CSV com tipagem forte.
 */
interface StatusEntry {
  date: string;     // Exemplo: "01/2015"
  status: number;   // Exemplo: 111.00
}

/**
 * Função para ler um CSV com colunas 'Date' e 'Status', separados por espaços ou tabulação.
 * @param content Conteúdo do CSV como string
 * @returns Array de StatusEntry
 */
function readStatusCSV(content: string): StatusEntry[] {
  // Remove espaços extras, quebra linhas, ignora cabeçalho/células vazias
  const lines = content.trim().split(/\r?\n/).slice(1);
  return lines.map(line => {
    const [date, status] = line.trim().split(/\s+/);
    return {
      date,
      status: Number(String(status).replace(",", "."))
    };
  });
}

/**
 * Função para potencialidades: média, min, max, variação, primeira e última, etc.
 * @param entries Array de StatusEntry
 */
function analyzePotentials(entries: StatusEntry[]) {
  const statuses = entries.map(e => e.status);
  const total = statuses.length;
  const sum = statuses.reduce((acc, v) => acc + v, 0);
  const avg = sum / total;
  const min = Math.min(...statuses);
  const max = Math.max(...statuses);
  const first = statuses[0];
  const last = statuses[statuses.length - 1];

  // Mudança percentual do início ao fim
  const percentChange = ((last - first) / first) * 100;

  return {
    total,
    avg: Number(avg.toFixed(2)),
    min,
    max,
    first,
    last,
    percentChange: Number(percentChange.toFixed(2))
  };
}

// Exemplo de uso
const sample = `
 Date  Status
01/2015\t 111,00 
02/2015\t 95,00 
03/2015\t 95,00 
04/2015\t 95,00 
05/2015\t 95,00 
06/2015\t 95,00 
07/2015\t 95,00 
08/2015\t 95,00 
09/2015\t 95,00 
`;

const entries = readStatusCSV(sample);
console.log("Entradas lidas:", entries);
console.log("Potencialidades:", analyzePotentials(entries));
