/**
 * Configurações e lógica para gráficos de estatísticas
 * Arquivo separado para melhor organização e reutilização
 */

// Configurações globais e constantes
const CHART_CONFIG = {
    colors: {
        primary: '#FFD700',
        secondary: '#FFA500',
        accent1: '#FF6347',
        accent2: '#FF4500',
        text: '#f0f0f0',
        border: 'rgba(255, 215, 0, 0.2)',
        grid: 'rgba(255, 215, 0, 0.1)'
    },
    commonOptions: {
        responsive: true,
        maintainAspectRatio: false
    },
    scales: {
        y: {
            beginAtZero: true,
            grid: { color: 'rgba(255, 215, 0, 0.1)' },
            ticks: { color: '#f0f0f0' }
        },
        x: {
            grid: { color: 'rgba(255, 215, 0, 0.1)' },
            ticks: { color: '#f0f0f0' }
        }
    },
    legend: {
        labels: {
            color: '#f0f0f0',
            font: { size: 12 }
        }
    }
};

/**
 * Cria configurações de gráfico reutilizáveis
 * @param {string} type - Tipo do gráfico
 * @param {Object} data - Dados do gráfico
 * @param {Object} customOptions - Opções customizadas
 * @returns {Object} Configuração completa do gráfico
 */
function createChartConfig(type, data, customOptions = {}) {
    return {
        type: type,
        data: data,
        options: {
            ...CHART_CONFIG.commonOptions,
            ...customOptions
        }
    };
}

/**
 * Cria configurações de scales reutilizáveis
 * @param {boolean} showLegend - Se deve mostrar a legenda
 * @param {string} legendPosition - Posição da legenda
 * @returns {Object} Configuração de scales e plugins
 */
function createScalesConfig(showLegend = true, legendPosition = 'bottom') {
    return {
        scales: CHART_CONFIG.scales,
        plugins: {
            legend: showLegend ? {
                ...CHART_CONFIG.legend,
                position: legendPosition,
                display: showLegend
            } : { display: false }
        }
    };
}

/**
 * Verifica se o Chart.js está disponível
 * @returns {boolean} True se Chart.js estiver disponível
 */
function isChartJsAvailable() {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js não foi carregado corretamente');
        return false;
    }
    return true;
}

/**
 * Configura as configurações globais do Chart.js
 */
function setupChartDefaults() {
    Chart.defaults.color = CHART_CONFIG.colors.text;
    Chart.defaults.borderColor = CHART_CONFIG.colors.border;
}

/**
 * Cria o gráfico de distribuição por idade
 * @param {Array} data - Dados das faixas etárias
 */
function createIdadeChart(data) {
    const canvas = document.getElementById('idadeChart');
    if (!canvas) return;

    const config = createChartConfig('doughnut', {
        labels: ['18-22 anos', '23-27 anos', '28-32 anos', '33+ anos'],
        datasets: [{
            data: data,
            backgroundColor: [
                CHART_CONFIG.colors.primary,
                CHART_CONFIG.colors.secondary,
                CHART_CONFIG.colors.accent1,
                CHART_CONFIG.colors.accent2
            ],
            borderWidth: 2,
            borderColor: '#000000'
        }]
    }, createScalesConfig(true, 'bottom'));
    
    const idadeChart = new Chart(canvas.getContext('2d'), config);
}

/**
 * Cria o gráfico de comparação de métricas
 * @param {Object} estatisticas - Dados das estatísticas
 */
function createMetricasChart(estatisticas) {
    const canvas = document.getElementById('metricasChart');
    if (!canvas) return;

    const config = createChartConfig('bar', {
        labels: ['Idade (anos)', 'Altura (cm)', 'Peso (kg)', 'Jogos'],
        datasets: [{
            label: 'Média',
            data: [
                estatisticas.media_idade || 0,
                estatisticas.media_altura * 100 || 0,
                estatisticas.media_peso || 0,
                (estatisticas.max_jogos + estatisticas.min_jogos) / 2 || 0
            ],
            backgroundColor: 'rgba(255, 215, 0, 0.8)',
            borderColor: CHART_CONFIG.colors.primary,
            borderWidth: 2
        }]
    }, createScalesConfig(false));
    
    const metricasChart = new Chart(canvas.getContext('2d'), config);
}

/**
 * Cria o gráfico de evolução de jogos
 * @param {Array} nomesAtletas - Nomes dos atletas
 * @param {Array} totalJogos - Total de jogos por atleta
 * @param {Array} jogosTitular - Jogos como titular por atleta
 */
function createJogosChart(nomesAtletas, totalJogos, jogosTitular) {
    const canvas = document.getElementById('jogosChart');
    if (!canvas) return;

    const config = createChartConfig('line', {
        labels: nomesAtletas,
        datasets: [{
            label: 'Total de Jogos',
            data: totalJogos,
            borderColor: CHART_CONFIG.colors.primary,
            backgroundColor: 'rgba(255, 215, 0, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
        }, {
            label: 'Jogos como Titular',
            data: jogosTitular,
            borderColor: CHART_CONFIG.colors.secondary,
            backgroundColor: 'rgba(255, 165, 0, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
        }]
    }, createScalesConfig(true, 'top'));
    
    const jogosChart = new Chart(canvas.getContext('2d'), config);
}

/**
 * Inicializa todos os gráficos com os dados fornecidos
 * @param {Object} chartData - Dados para os gráficos
 */
function initializeCharts(chartData) {
    if (!isChartJsAvailable()) {
        alert('Chart.js não foi carregado corretamente. Verifique sua conexão ou tente recarregar a página.');
        return;
    }

    setupChartDefaults();

    // Criar todos os gráficos
    createIdadeChart(chartData.faixasEtarias);
    createMetricasChart(chartData.estatisticas);
    createJogosChart(chartData.nomesAtletas, chartData.totalJogos, chartData.jogosTitular);
} 