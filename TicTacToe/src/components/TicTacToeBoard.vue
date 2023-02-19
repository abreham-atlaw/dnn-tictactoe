<script lang="ts">

	import { defineComponent } from "vue";
	import axios from "axios";	

	const SERVER_ADDRESS = "http://127.0.0.1:5000";
	const MOVE_URL = `${SERVER_ADDRESS}/move`;

	export default defineComponent({
		
		data() {
			
			return {
				state: [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
				currentPlayer: 0,
				aiPlayer: 1,
			}
	
		},

		computed: {
			
			gameOver(): boolean{
				if(this.winner != -1){
					return true;
				}
				for(let i=0; i<3; i++){
					for(let j=0; j<3; j++){
						if(this.state[i][j] === -1){
							return false;
						}
					}
				}
				return true;
			},

			winner(){
				for(let i=0; i<3; i++){
					
					if(this.state[i][0] === this.state[i][1] && this.state[i][0] === this.state[i][2] && this.state[i][0] != -1){
						return this.state[i][0];
					}
					if(this.state[0][i] === this.state[1][i] && this.state[0][i] === this.state[2][i] && this.state[0][i] != -1){
						return this.state[0][i];
					}

				}
				if(((this.state[0][0] == this.state[1][1] && this.state[1][1] == this.state[2][2]) || (this.state[0][2] == this.state[1][1] && this.state[1][1] == this.state[2][0])) && this.state[1][1]){
					return this.state[1][1];
				}
				return -1;
			}

		},

		methods: {
			
			labelValue(value: int){
				
				return [" ", "O", "X"][value+1];
			},
			
			reset(){
				this.state = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]];
				this.currentPlayer = 0
			},

			move(y: int, x: int){
				if(this.gameOver || this.state[y][x] != -1){
					return;
				}
				this.state[y][x] = this.currentPlayer;
				this.currentPlayer = (this.currentPlayer+1)%2;
			},

			switchAiPlayer(){
				this.aiPlayer = (this.aiPlayer + 1) % 2;
				this.reset();
			},

			makeAiMove(){
				axios.post(MOVE_URL, {
					state: this.state
				})
				.then((response) => {
					this.move(response.data[0], response.data[1]);
				})
				.catch((error) => {
					console.log(error);
				})
			},

	
		},

		watch: {

			currentPlayer(newValue){
				if(newValue == this.aiPlayer){
					this.makeAiMove();
				}
			},
			aiPlayer(newValue){
				if(newValue == this.currentPlayer){
					this.makeAiMove();
				}
			},

		}


	});



</script>

<template>
	
	<div class="row h-100">
		<div class="col-12 h-100">
			<div v-for="(row, i) in state" class="row" :style="{height: '33%'}">
				<div v-for="(cell, j) in row" class="col-4 border border-primary h-100 d-flex" @click="() => {move(i, j)}">
					<div class="m-auto">
						{{ labelValue(cell) }}
					</div>
				</div>
			</div>
		</div>
		<div class="col-12 d-flex mt-5">
			<div class="m-auto">
				<button class="btn btn-success mx-3" @click="reset()">
					Reset
				</button>
				<button class="btn btn-primary mx-3" @click="switchAiPlayer()">
					Switch AI Player
				</button>
			</div>
		</div>
	</div>

</template>
