// Importar a biblioteca http do k6
import http from 'k6/http';

// Exportar as opções de configuração do teste
export let options = {
    stages: [
        { duration: '30s', target: 20 }, // Simular 20 usuários por 30 segundos
        { duration: '1m', target: 10 },  // Escalar para baixo para 10 usuários e manter por 1 minuto
        { duration: '10s', target: 1 },  // Escalonar para baixo para 0 usuários
    ],
};

// Função de execução principal
export default function () {
    // Realizar uma requisição GET para o seu site
    http.get('https://api.guilhermefreis.com/');
    http.get('https://api.guilhermefreis.com/contato');
    http.get('https://api.guilhermefreis.com/status');
    http.get('https://api.guilhermefreis.com/chamada');
    // http.get('https://api.guilhermefreis.com/error');
}