<script setup lang="ts">
import TicTacToeBoard from  './components/TicTacToeBoard.vue';
</script>

<template>
  <header>
  </header>

  <main class="h-100">
  	
	  <div class="d-flex h-100">
		  <div class="m-auto" :style="{width: '25em', height:'25em'}">
		  	  <TicTacToeBoard />
		  </div>
	  </div>
  
  </main>
</template>

