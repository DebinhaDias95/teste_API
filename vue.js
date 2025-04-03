<template>
  <div id="app">
    <h1>Busca de Operadoras</h1>
    Campo de pesquisa 
    <input 
      v-model="query" 
      @input="search" 
      placeholder="Pesquisar operadora" 
    
     </div>
     Lista de operadoras retornadas 
    <ul v-if="operadoras.length > 0">
      <li v-for="operadora in operadoras" :key="operadora.id">
        <strong>{{ operadora.nome }}</strong><br />
        CNPJ: {{ operadora.cnpj }}<br />
        Endereço: {{ operadora.endereco }}<br />
        Telefone: {{ operadora.telefone }}
      </li>
    </ul>
    
    <!-- Caso não haja resultados -->
    <p v-else>Sem resultados.</p>
  </div>
</template>

<script>
// Importando o Axios para fazer requisições HTTP
import axios from 'axios';

export default {
  data() {
    return {
      query: '',         // Armazenará o texto digitado pelo usuário
      operadoras: []     // Lista de operadoras que será preenchida com os dados da API
    };
  },
  methods: {
    async search() {
      // Verifica se a consulta não está vazia
      if (this.query) {
        try {
          // Fazendo a requisição GET para a API Flask
          const response = await axios.get(`/search?query=${this.query}`);
          
          // Atualiza a lista de operadoras com os dados retornados pela API
          this.operadoras = response.data;
        } catch (error) {
          // Exibe um erro caso a requisição falhe
          console.error("Erro ao fazer a requisição:", error);
        }
      } else {
        // Se o campo de pesquisa estiver vazio, limpa os resultados
        this.operadoras = [];
      }
    }
  }
};
</script>

<style scoped>
/* Estilos para a página (opcional) */
#app {
  font-family: Arial, sans-serif;
  padding: 20px;
}

input {
  padding: 10px;
  font-size: 16px;
  width: 300px;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

strong {
  font-size: 18px;
}

p {
  color: red;
}
</style>
